import random
import time
import gc
from pathlib import Path
import mlx.core as mx
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein

from src.utils.file_utils import get_filename, get_parent_directory, safe_read_json, save_json
from src.utils.resolution_utils import get_size_by_resolution
from src.constants import IMAGE_RESOLUTION
from .constants import STEPS, GUIDANCE, QUANTIZE, CHUNK_SIZE, COOLDOWN_SECONDS


class ImageService:
    def __init__(self):
        self.size = get_size_by_resolution(IMAGE_RESOLUTION)
        self.width = self.size[0]
        self.height = self.size[1]

        self.__load_model()

    def __load_model(self):
        print(f"🖼️ Loading FLUX.2 Klein 4B (quantize={QUANTIZE})...")
        self.model = Flux2Klein(
            model_config=ModelConfig.flux2_klein_4b(),
            quantize=QUANTIZE
        )

    @staticmethod
    def __save_image_data(prompt: str, image_path: Path | str, seed: int):
        parent_dir = get_parent_directory(image_path)
        file_name = get_filename(image_path)
        json_path = parent_dir / "data.json"

        data = safe_read_json(json_path, default_value=[])

        data.append({
            "id": file_name,
            "seed": seed,
            "prompt": prompt
        })

        save_json(json_path, data)

    def generate(
            self,
            prompt: str,
            output_path: Path | str,
            seed: int | None = None,
    ):
        output_path = Path(output_path)
        final_seed = seed if seed is not None else random.randint(0, 2 ** 32 - 1)

        self.__save_image_data(prompt, output_path, final_seed)

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

    def generate_batch(self, prompts: list[str], output_paths: list[Path | str], seeds: list[int] | None = None):
        for i, prompt in enumerate(prompts):
            print(f"Batch progress: {i + 1}/{len(prompts)}")
            seed = seeds[i] if seeds and i < len(seeds) else None
            self.generate(prompt=prompt, output_path=output_paths[i], seed=seed)

            if (i + 1) % CHUNK_SIZE == 0 and (i + 1) != len(prompts):
                gc.collect()
                mx.clear_cache()

                print(f"\n🔥 Protecting thermal limits... Cooling down M4 chip.")
                print(f"⏳ Waiting for {COOLDOWN_SECONDS} seconds...\n")
                time.sleep(COOLDOWN_SECONDS)

    def generate_variations(self, prompt: str, count: int = 4):
        seeds = [random.randint(0, 2 ** 32 - 1) for _ in range(count)]
        self.generate_batch(prompts=[prompt] * count, seeds=seeds)
