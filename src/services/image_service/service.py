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
    def __init__(self):
        self.size = get_size_by_resolution(IMAGE_RESOLUTION)
        self.width = self.size[0]
        self.height = self.size[1]

        self.base_model = None
        self.edit_model = None

    def __get_model(self, use_reference: bool):
        if use_reference:
            if self.edit_model is None:
                print(f"🖼️  Loading Flux2KleinEdit (quantize={QUANTIZE})...")
                self.edit_model = Flux2KleinEdit(
                    model_config=ModelConfig.flux2_klein_4b(),
                    quantize=QUANTIZE,
                )
            return self.edit_model

        if self.base_model is None:
            print(f"🖼️  Loading Flux2Klein (quantize={QUANTIZE})...")
            self.base_model = Flux2Klein(
                model_config=ModelConfig.flux2_klein_4b(),
                quantize=QUANTIZE,
            )
        return self.base_model

    def __unload(self, which: str):
        if which == "edit":
            self.edit_model = None
        else:
            self.base_model = None
        gc.collect()
        mx.clear_cache()

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

    @staticmethod
    def __resolve_refs(ref_image_paths: list[Path | str] | None) -> list[Path] | None:
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
        use_reference = bool(refs)

        self.__save_image_data(prompt, output_path, final_seed, refs)

        ref_label = ", ".join(ref.name for ref in refs) if refs else "none"
        model_label = "edit" if use_reference else "base"
        print(
            f"Generating [{model_label}]: {self.width}x{self.height} | seed={final_seed} | "
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

        if use_reference:
            kwargs["image_paths"] = refs

        model = self.__get_model(use_reference)
        image = model.generate_image(**kwargs)
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
        items = []
        for i, prompt in enumerate(prompts):
            raw_refs = references[i] if references else None
            seed = seeds[i] if seeds and i < len(seeds) else None
            use_reference = bool(self.__resolve_refs(raw_refs))
            items.append((prompt, output_paths[i], raw_refs, seed, use_reference))

        without_refs = [it for it in items if not it[4]]
        with_refs = [it for it in items if it[4]]

        print(f"\n🧩 {len(without_refs)} sahne referanssız (base), "
              f"{len(with_refs)} sahne referanslı (edit)")

        for group_name, group in (("base", without_refs), ("edit", with_refs)):
            if not group:
                continue

            for j, (prompt, out_path, raw_refs, seed, _) in enumerate(group):
                print(f"\n📸 [{group_name}] {j + 1}/{len(group)}")
                self.generate(
                    prompt=prompt,
                    output_path=out_path,
                    ref_image_paths=raw_refs,
                    seed=seed,
                )
                self.__cooldown(j, len(group))

            self.__unload(group_name)

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
