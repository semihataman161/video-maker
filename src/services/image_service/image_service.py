from pathlib import Path
import torch
import gc
from diffusers import StableDiffusionPipeline

from ..constants import OUTPUT_DIR


class ImageService:
    MODEL_ID = "Lykon/anylora-Anime-Mix"

    NEGATIVE_PROMPT = """
    text, watermark, logo, blurry, low resolution, bad anatomy,
    extra fingers, extra limbs, distorted face, realistic, photography,
    3d render, doll, plastic, grain, noise
    """

    def __init__(self, visual_plan: dict):
        self.visual_plan = visual_plan

        self.images_dir = Path(OUTPUT_DIR / "images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.portraits_dir = Path(OUTPUT_DIR / "portraits")
        self.portraits_dir.mkdir(parents=True, exist_ok=True)

        # ---------------- DEVICE CONFIG ----------------
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "mps" else torch.float32

        print(f"🔥 Loading Anime Model ({self.MODEL_ID}) on {self.device} with {self.dtype}...")

        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.MODEL_ID,
            torch_dtype=self.dtype,
            safety_checker=None,
        )

        self.pipe = self.pipe.to(self.device)

        # Memory optimization
        self.pipe.enable_attention_slicing("max")
        self.pipe.enable_vae_slicing()

    # -------------------------------------------------

    def __build_character_block(self):
        blocks = []
        for c in self.visual_plan["characters"]:
            blocks.append(
                f"1 {c['gender']}, {c['age']} year old, {c['name']}, "
                f"{c['physical_appearance']}, "
                f"{c['clothing_style']}"
            )
        return ", ".join(blocks)

    def __build_environment_block(self):
        env = self.visual_plan["environment"]

        return f"""
        {env['location_type']},
        {env['architecture_style']},
        {env['natural_elements']},
        {env['weather_style']},
        {env['overall_atmosphere']}
        """

    def __build_style_block(self):
        return """
        masterpiece, high quality, highres, anime style, 
        illustrative, painterly, vibrant colors, soft lighting,
        detailed background, clean lines
        """

    def __build_scene_prompt(self, scene):
        return f"""
        {self.__build_style_block()}
        {self.__build_environment_block()}
        {self.__build_character_block()}

        Scene: {scene['visual_description']}
        Camera shot: {scene['camera_shot_type']}
        Camera angle: {scene['camera_angle']}
        Time of day: {scene['time_of_day']}
        Emotional tone: {scene['emotional_tone']}

        (Ghibli style:0.8), (Makoto Shinkai style:0.8), digital illustration,
        detailed scenery, atmospheric, cinematic lighting
        """

    # -------------------------------------------------

    def __cleanup(self):
        gc.collect()
        if self.device == "mps":
            torch.mps.empty_cache()

    # -------------------------------------------------

    def run(self):
        # ----------------- PORTRAITS -----------------
        for character in self.visual_plan["characters"]:
            generator = torch.Generator(device=self.device).manual_seed(42)

            image = self.pipe(
                prompt=f"{self.__build_style_block()}, {character['master_visual_prompt']}",
                negative_prompt=self.NEGATIVE_PROMPT,
                num_inference_steps=20,
                guidance_scale=7.5,
                width=512,
                height=768,
                generator=generator,
            ).images[0]

            image.save(self.portraits_dir / f"{character['name']}.jpg")

            del image
            self.__cleanup()

        # ----------------- SCENES -----------------
        for scene in self.visual_plan["scenes"]:
            generator = torch.Generator(device=self.device).manual_seed(42)

            prompt = self.__build_scene_prompt(scene)

            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.NEGATIVE_PROMPT,
                num_inference_steps=20,
                guidance_scale=7.5,
                width=768,
                height=512,
                generator=generator,
            ).images[0]

            filename = f"scene_{scene['scene_number']:03}.jpg"
            image.save(self.images_dir / filename)

            del image
            self.__cleanup()
