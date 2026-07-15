import random
import time
import gc
from pathlib import Path
import mlx.core as mx
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein
from mflux.models.flux2.variants.edit.flux2_klein_edit import Flux2KleinEdit

from src.utils.file_utils import get_filename, get_parent_directory, safe_read_json, save_json, try_validate_path
from src.utils.resolution_utils import get_size_by_resolution
from src.constants import IMAGE_RESOLUTION
from .constants import STEPS, GUIDANCE, QUANTIZE, CHUNK_SIZE, COOLDOWN_SECONDS

References = list[list[Path | str]]


class ImageService:
    def __init__(self, with_reference: bool):
        self.with_reference = with_reference

        self.size = get_size_by_resolution(IMAGE_RESOLUTION)
        self.width = self.size[0]
        self.height = self.size[1]

        self.model = None
        self.__load_model()

    def __load_model(self):
        cls = Flux2KleinEdit if self.with_reference else Flux2Klein

        print(f"🖼️  Loading {cls.__name__} (quantize={QUANTIZE}, with_reference={self.with_reference})...")

        self.model = cls(
            model_config=ModelConfig.flux2_klein_4b(),
            quantize=QUANTIZE,
        )

    @staticmethod
    def __save_image_data(
            prompt: str,
            image_path: Path | str,
            seed: int,
            refs: list[Path] | None = None,
    ):
        parent_dir = get_parent_directory(image_path)
        file_name = get_filename(image_path)
        json_path = parent_dir / "data.json"

        data = safe_read_json(json_path, default_value=[])

        data.append({
            "id": file_name,
            "seed": seed,
            "prompt": prompt,
            "refs": [str(r) for r in refs] if refs else None,
        })

        save_json(json_path, data)

    @staticmethod
    def __cooldown(index: int, total: int):
        if (index + 1) % CHUNK_SIZE == 0 and (index + 1) != total:
            gc.collect()
            mx.clear_cache()
            print("\n🔥 Protecting thermal limits... Cooling down M4 chip.")
            print(f"⏳ Waiting for {COOLDOWN_SECONDS} seconds...\n")
            time.sleep(COOLDOWN_SECONDS)

    def __resolve_refs(self, ref_image_paths: list[Path | str] | None) -> list[Path] | None:
        if not self.with_reference:
            return None

        if not ref_image_paths:
            return None

        refs = [Path(path) for path in ref_image_paths]
        for ref in refs:
            try_validate_path(ref)
        return refs

    def generate(
            self,
            prompt: str,
            output_path: Path | str,
            ref_image_paths: list[Path | str] | None = None,
            seed: int | None = None,
    ):
        output_path = Path(output_path)
        final_seed = seed if seed is not None else random.randint(0, 2 ** 32 - 1)

        refs = self.__resolve_refs(ref_image_paths)

        self.__save_image_data(prompt, output_path, final_seed, refs)

        ref_label = ", ".join(ref.name for ref in refs) if refs else "none"
        print(
            f"Generating: {self.width}x{self.height} | seed={final_seed} | "
            f"steps={STEPS} | refs=[{ref_label}]"
        )

        kwargs = {
            "prompt": prompt,
            "seed": final_seed,
            "num_inference_steps": STEPS,
            "width": self.width,
            "height": self.height,
            "guidance": GUIDANCE,
        }

        if refs:
            kwargs["image_paths"] = refs

        image = self.model.generate_image(**kwargs)
        image.save(path=output_path)
        print(f"✅ Image saved to: {output_path}")

        return output_path

    def generate_batch(
            self,
            prompts: list[str],
            output_paths: list[Path | str],
            references: References | None = None,
            seeds: list[int] | None = None,
    ):
        for i, prompt in enumerate(prompts):
            print(f"\n📸 {i + 1}/{len(prompts)}")

            self.generate(
                prompt=prompt,
                output_path=output_paths[i],
                ref_image_paths=references[i] if references else None,
                seed=seeds[i] if seeds and i < len(seeds) else None,
            )

            self.__cooldown(i, len(prompts))

    def generate_variations(
            self,
            prompt: str,
            output_paths: list[Path | str],
            count: int = 4,
            ref_image_paths: list[Path | str] | None = None,
    ):
        for i in range(count):
            print(f"\n📸 Variation {i + 1}/{count}")

            self.generate(
                prompt=prompt,
                output_path=output_paths[i],
                ref_image_paths=ref_image_paths
            )

            self.__cooldown(i, count)
