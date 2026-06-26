import random
import time
import gc
import mlx.core as mx
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein

from src.utils.file_utils import (
    try_validate_path, get_next_file_path,
    get_filename, safe_read_json, save_json
)
from src.utils.resolution_utils import get_resolution
from src.constants import IMAGE_RESOLUTION, ORIGINAL_IMAGES_DIR
from .constants import STEPS, GUIDANCE, QUANTIZE, CHUNK_SIZE, COOLDOWN_SECONDS


class ImageService:
    def __init__(self):
        try_validate_path(ORIGINAL_IMAGES_DIR)

        self.resolution = get_resolution(IMAGE_RESOLUTION)
        self.width = self.resolution[0]
        self.height = self.resolution[1]

        self.json_path = ORIGINAL_IMAGES_DIR / "image_data.json"

        self.__load_model()

    def __load_model(self):
        print(f"🖼️ Loading FLUX.2 Klein 4B (quantize={QUANTIZE})...")
        self.model = Flux2Klein(
            model_config=ModelConfig.flux2_klein_4b(),
            quantize=QUANTIZE
        )

    def __save_metadata(self, scene_id: str, seed: int, prompt: str):
        data = safe_read_json(self.json_path, default_value=[])

        data.append({
            "id": scene_id,
            "seed": seed,
            "prompt": prompt
        })

        save_json(self.json_path, data)

    def generate(self, prompt: str, seed: int | None = None):
        output_path = get_next_file_path(ORIGINAL_IMAGES_DIR)
        final_seed = seed if seed is not None else random.randint(0, 2 ** 32 - 1)

        file_name = get_filename(output_path)
        self.__save_metadata(file_name, final_seed, prompt)

        print(f"Generating image: {self.width}x{self.height} | seed={final_seed} | steps={STEPS}")

        image = self.model.generate_image(
            prompt=prompt,
            seed=final_seed,
            num_inference_steps=STEPS,
            width=self.width,
            height=self.height,
            guidance=GUIDANCE
        )

        image.save(path=output_path)
        print(f"Image saved to: {output_path}")

    def generate_batch(self, prompts: list[str], seeds: list[int] | None = None):
        for i, prompt in enumerate(prompts):
            print(f"Batch progress: {i + 1}/{len(prompts)}")
            seed = seeds[i] if seeds and i < len(seeds) else None
            self.generate(prompt=prompt, seed=seed)

            gc.collect()
            mx.clear_cache()

            if (i + 1) % CHUNK_SIZE == 0 and (i + 1) != len(prompts):
                print(f"\n🔥 Protecting thermal limits... Cooling down M4 chip.")
                print(f"⏳ Waiting for {COOLDOWN_SECONDS} seconds...\n")
                time.sleep(COOLDOWN_SECONDS)

    def generate_variations(self, prompt: str, count: int = 4):
        seeds = [random.randint(0, 2 ** 32 - 1) for _ in range(count)]
        self.generate_batch(prompts=[prompt] * count, seeds=seeds)
