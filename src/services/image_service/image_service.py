from pathlib import Path
import torch
import gc
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

from ..constants import OUTPUT_DIR
from src.utils.device_utils import get_device, get_dtype


class ImageService:
    MODEL_ID = "nitrosocke/Ghibli-Diffusion"

    NEGATIVE_PROMPT = """
    worst quality, low quality, jpeg artifacts,
    text, watermark, logo,
    blurry, bad anatomy,
    extra fingers, extra limbs,
    distorted face,
    3d render, realistic, photo,
    noise, grain
    """

    def __init__(self, visual_plan: dict):
        self.visual_plan = visual_plan

        self.images_dir = Path(OUTPUT_DIR / "images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.portraits_dir = Path(OUTPUT_DIR / "portraits")
        self.portraits_dir.mkdir(parents=True, exist_ok=True)

        # ✅ NEW DEVICE CONFIG
        self.device = get_device()
        self.dtype = get_dtype(self.device)
        print(f"🔥 Loading Model ({self.MODEL_ID}) on {self.device} ({self.dtype})")

        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.MODEL_ID,
            torch_dtype=self.dtype,
            safety_checker=None,
            device_map=None,
        )

        # Scheduler
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )

        # Manual device placement
        self.pipe.unet.to(self.device)
        self.pipe.vae.to(self.device)
        self.pipe.text_encoder.to(self.device)

        # Memory optimizations
        self.pipe.enable_attention_slicing("max")
        self.pipe.enable_vae_slicing()

        try:
            self.pipe.enable_xformers_memory_efficient_attention()
        except Exception:
            pass

    def __build_style_block(self):
        return """
        (best quality, masterpiece),
        studio ghibli style,
        soft lighting, pastel colors,
        cinematic, detailed
        """

    def __build_scene_prompt(self, scene):
        return f"""
        {self.__build_style_block()}

        {scene['visual_description']},
        {scene['camera_shot_type']},
        {scene['camera_angle']},
        {scene['time_of_day']},
        {scene['emotional_tone']},

        cinematic lighting, depth
        """

    def __cleanup(self):
        gc.collect()

        if self.device == "cuda":
            torch.cuda.empty_cache()
        elif self.device == "mps":
            torch.mps.empty_cache()

    def run(self):
        # ----------------- PORTRAITS -----------------
        for character in self.visual_plan["characters"]:
            prompt = f"""
            {self.__build_style_block()},
            {character['master_visual_prompt']}
            """

            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.NEGATIVE_PROMPT,
                num_inference_steps=12,
                guidance_scale=6,
                width=512,
                height=768,
            ).images[0]

            image.save(self.portraits_dir / f"{character['name']}.jpg")

            del image
            self.__cleanup()

        # ----------------- SCENES -----------------
        for scene in self.visual_plan["scenes"]:
            prompt = self.__build_scene_prompt(scene)

            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.NEGATIVE_PROMPT,
                num_inference_steps=12,
                guidance_scale=6,
                width=768,
                height=512,
            ).images[0]

            filename = f"scene_{scene['scene_number']:03}.jpg"
            image.save(self.images_dir / filename)

            del image
            self.__cleanup()
