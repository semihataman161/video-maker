import random
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein

from src.utils.file_utils import validate_path, get_next_filename
from src.utils.resolution_utils import get_resolution
from src.constants import IMAGE_RESOLUTION, ORIGINAL_IMAGES_DIR
from .constants import STEPS, GUIDANCE, QUANTIZE


class ImageService:
    def __init__(self):
        validate_path(ORIGINAL_IMAGES_DIR)

        self.resolution = get_resolution(IMAGE_RESOLUTION)
        self.width = self.resolution[0]
        self.height = self.resolution[1]

        self.__load_model()

    def __load_model(self):
        print(f"🖼️ Loading FLUX.2 Klein 4B (quantize={QUANTIZE})...")
        self.model = Flux2Klein(
            model_config=ModelConfig.flux2_klein_4b(),
            quantize=QUANTIZE
        )

    def generate(self, prompt: str, seed: int | None = None):
        final_seed = seed if seed is not None else random.randint(0, 2 ** 32 - 1)
        print(f"Generating image: {self.width}x{self.height} | seed={final_seed} | steps={STEPS}")

        image = self.model.generate_image(
            prompt=prompt,
            seed=final_seed,
            num_inference_steps=STEPS,
            width=self.width,
            height=self.height,
            guidance=GUIDANCE
        )

        output_path = get_next_filename(ORIGINAL_IMAGES_DIR)
        image.save(path=output_path)
        print(f"Image saved to: {output_path}")

    def generate_batch(self, prompts: list[str], seeds: list[int] | None = None):
        for i, prompt in enumerate(prompts):
            print(f"Batch progress: {i + 1}/{len(prompts)}")
            seed = seeds[i] if seeds and i < len(seeds) else None
            self.generate(prompt=prompt, seed=seed)

    def generate_variations(self, prompt: str, count: int = 4):
        seeds = [random.randint(0, 2 ** 32 - 1) for _ in range(count)]
        self.generate_batch(prompts=[prompt] * count, seeds=seeds)
