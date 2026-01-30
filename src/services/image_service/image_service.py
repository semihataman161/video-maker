from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline


class ImageService:
    MODEL_ID = "runwayml/stable-diffusion-v1-5"

    def __init__(
            self,
            chunks_dir: str = "output/chunks",
            images_dir: str = "output/images",
            device: str = "cpu",
    ):
        self.chunks_dir = Path(chunks_dir)
        self.images_dir = Path(images_dir)
        self.device = device

    def __summarize_scene(self, text: str) -> str:
        sentences = text.split(".")
        important = sentences[:2]
        clean = " ".join(important)
        return clean[:300]

    def __create_prompts(self) -> None:
        self.images_dir.mkdir(parents=True, exist_ok=True)

        for i, chunk in enumerate(sorted(self.chunks_dir.glob("*.txt"))):
            text = chunk.read_text()

            prompt = (
                    "cinematic film still, ultra realistic, dramatic lighting, "
                    "35mm photography, shallow depth of field, high detail, "
                    "moody atmosphere, dark tones, "
                    "scene description: "
                    + self.__summarize_scene(text)
            )

            prompt_path = self.images_dir / f"prompt_{i:03}.txt"
            prompt_path.write_text(prompt)

    def __create_images(self) -> None:
        pipe = StableDiffusionPipeline.from_pretrained(
            self.MODEL_ID,
            torch_dtype=torch.float32,
            safety_checker=None,
        )
        pipe = pipe.to(self.device)
        pipe.enable_attention_slicing()

        for prompt_file in sorted(self.images_dir.glob("prompt_*.txt")):
            prompt = prompt_file.read_text().strip()

            if not prompt:
                continue

            image = pipe(
                prompt=prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
            ).images[0]

            image.save(prompt_file.with_suffix(".jpg"))

    def run(self) -> None:
        self.__create_prompts()
        self.__create_images()
