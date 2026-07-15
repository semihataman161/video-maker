import re
import sys
from pathlib import Path

from src.services.timer_service_cache import TimerServiceCache
from src.utils.file_utils import (
    create_directories, reserve_next_file_paths, create_directory,
    is_path_exist, try_validate_path, try_read_json, save_json
)
from src.utils.chunk_utils import parse_chunks
from src.constants import (
    CHUNKS, LANGUAGE, WORDS_PER_CAPTION, WORDS_PER_SCREEN,
    AUDIO_DIR, CHARACTERS_DIR, SCENES_DIR, THUMBNAILS_DIR,
    FONTS_DIR, ASSETS_IMAGES_DIR, ASSETS_VIDEOS_DIR, CHANNEL_NAME
)

create_directories([AUDIO_DIR, CHARACTERS_DIR, SCENES_DIR, THUMBNAILS_DIR])
CASTING_JSON = CHARACTERS_DIR / "casting.json"

timer_cache = TimerServiceCache()


def parse_scene_indices(raw: str) -> list[int]:
    text = raw.strip().strip("[]").strip()

    if not text:
        raise ValueError('No scene index given. Example: make edit-scenes SCENES="[12, 15, 21]"')

    return [int(part) for part in re.split(r"[,\s]+", text) if part]


def load_characters() -> dict[str, Path]:
    casting = try_read_json(CASTING_JSON)
    characters: dict[str, Path] = {}

    for character_id, chosen in casting.items():
        if not chosen:
            raise ValueError(
                f"No selection has been made for '{character_id}'. Please fill out the {CASTING_JSON} file."
            )

        path = CHARACTERS_DIR / character_id / chosen
        try_validate_path(path)
        characters[character_id] = path

    return characters


def print_characters(characters: dict[str, Path]):
    print("🎭 Characters:")

    for character_id, path in characters.items():
        print(f"   {character_id:12} -> {path.name}")


@timer_cache.track("🎭 Creating Characters")
def step_create_characters():
    from src.services.image_service import ImageService
    from src.services.image_service.prompt import PromptService

    prompt_service = PromptService()
    image_service = ImageService()

    characters = prompt_service.build_character_prompts()
    character_count = 6

    for character_id, prompt in characters.items():
        out_dir = CHARACTERS_DIR / character_id
        create_directory(out_dir)

        print(f"\n=== Creating: {character_id} ===")

        image_service.generate_variations(
            prompt=prompt,
            output_paths=[out_dir / f"{i + 1}.png" for i in range(character_count)],
            count=character_count,
        )

    if not is_path_exist(CASTING_JSON):
        save_json(CASTING_JSON, {cid: None for cid in characters})

    print("\n" + "=" * 60)
    print("⏸  YOUR TURN")
    print(f"   1. Open: {CHARACTERS_DIR}")
    print("   2. For each character, choose the most NEUTRAL and CLEAREST portrait")
    print("      (not the best-looking one — this will anchor all scenes)")
    print(f"   3. Update {CASTING_JSON} with:")
    print('        { "john": "1.png", "edmund": "2.png" }')
    print("   4. Then run: make create-scenes")
    print("=" * 60)


@timer_cache.track("🎙 Creating Audio")
def step_create_audio():
    from src.services.audio_service import AudioService

    AudioService(
        chunks=parse_chunks(CHUNKS),
        language=LANGUAGE,
        should_include_music=True
    ).run()


@timer_cache.track("📝 Creating SRT")
def step_create_srt():
    from src.services.subtitle_service.srt import SubtitleSrtService

    SubtitleSrtService(words_per_caption=WORDS_PER_CAPTION).run()


@timer_cache.track("🎨 Creating Scenes")
def step_create_scenes():
    from src.services.image_service import ImageService
    from src.services.image_service.prompt import PromptService

    characters = load_characters()
    print_characters(characters)

    prompt_service = PromptService(characters)
    image_service = ImageService()

    prompts = prompt_service.build_scene_prompts()
    references = prompt_service.build_scene_references()
    output_paths = reserve_next_file_paths(SCENES_DIR, len(prompts))

    image_service.generate_batch(
        prompts=prompts,
        output_paths=output_paths,
        references=references,
    )


@timer_cache.track("🛠️ Editing Scene")
def step_edit_scenes(scene_indices: list[int], count):
    from src.services.image_service import ImageService
    from src.services.image_service.prompt import PromptService

    characters = load_characters()
    print_characters(characters)

    prompt_service = PromptService(characters)
    image_service = ImageService()

    prompts = prompt_service.build_scene_prompts()
    references = prompt_service.build_scene_references()

    for scene_index in scene_indices:
        if not 1 <= scene_index <= len(prompts):
            raise IndexError(
                f"Invalid scene index: {scene_index} (valid range: 1-{len(prompts)})"
            )

    print(f"\n🛠️  Editing scenes: {scene_indices} ({count} variations each)")

    for scene_index in scene_indices:
        position = scene_index - 1
        output_paths = reserve_next_file_paths(SCENES_DIR, count)

        print(f"\n=== Scene {scene_index} ===")

        image_service.generate_variations(
            prompt=prompts[position],
            output_paths=output_paths,
            count=count,
            ref_image_paths=references[position],
        )


@timer_cache.track("✨ Creating Thumbnails")
def step_create_thumbnails():
    from src.services.image_service import ImageService
    from src.services.image_service.prompt import PromptService

    characters = load_characters()
    print_characters(characters)

    prompt_service = PromptService(characters)
    image_service = ImageService()

    thumbnails = prompt_service.get_thumbnails()

    prompts = prompt_service.build_thumbnail_prompts()
    references = prompt_service.build_thumbnail_references()
    output_paths = [THUMBNAILS_DIR / f"{thumbnail['id']}.png" for thumbnail in thumbnails]

    image_service.generate_batch(
        prompts=prompts,
        output_paths=output_paths,
        references=references,
    )


@timer_cache.track("✍️ Creating Text on Thumbnails")
def step_create_text_on_thumbnails():
    from src.services.image_service.prompt import PromptService
    from src.services.image_text_overlay_service import ImageTextOverlayConfig, ImageTextOverlayService

    prompt_service = PromptService()
    thumbnails = prompt_service.get_thumbnails()

    text_overlay_config = ImageTextOverlayConfig(font_path=FONTS_DIR / "Anton-Regular.ttf")
    text_overlay_service = ImageTextOverlayService(text_overlay_config)

    for thumbnail in thumbnails:
        text_overlay_service.run(
            image_path=THUMBNAILS_DIR / f"{thumbnail['id']}.png",
            text=thumbnail["title_text"],
            output_path=THUMBNAILS_DIR / f"{thumbnail['id']}_final.png",
            area=thumbnail.get("composition", {}).get("text_safe_area", "left half"),
        )


@timer_cache.track("🎬 Creating Video")
def step_create_video():
    from src.services.overlay_video_service import OverlayVideoService
    from src.services.watermark_service import WatermarkConfig, WatermarkService
    from src.services.subtitle_service.render import SubtitleRenderConfig, SubtitleRenderService
    from src.services.effect_service import EffectService
    from src.services.outro_service import OutroService
    from src.services.video_service import VideoService

    overlay_video_service = OverlayVideoService(
        video_path=str(ASSETS_VIDEOS_DIR / "overlay.mp4"),
        mode="light_overlay"
    )

    watermark_config = WatermarkConfig(
        channel_name=CHANNEL_NAME,
        font=str(FONTS_DIR / "Montserrat-Bold.ttf"),
        fontsize=45,
        logo_path=str(ASSETS_IMAGES_DIR / "logo.png"),
        logo_width=100,
        logo_height=100,
        color="white",
        opacity=1,
        margin=40
    )
    watermark_service = WatermarkService(
        config=watermark_config,
    )

    subtitle_render_config = SubtitleRenderConfig(
        font=str(FONTS_DIR / "Montserrat-Bold.ttf"),
        fontsize=55,
        color="white",
        active_color="yellow",
        stroke_color="black",
        stroke_width=3,
        position="bottom",
        vertical_margin=200,
        word_spacing=10
    )
    subtitle_render_service = SubtitleRenderService(
        config=subtitle_render_config,
        words_per_screen=WORDS_PER_SCREEN,
    )

    effect_service = EffectService(mode="random")

    outro_service = OutroService(
        image_path=str(ASSETS_IMAGES_DIR / "outro.png"),
        image_size=(599, 417),
        bg_color=(15, 15, 15)
    )

    VideoService(
        overlays=[watermark_service, subtitle_render_service],
        effect_service=effect_service,
        outro_service=outro_service,
        overlay_video_service=overlay_video_service,
    ).run()


TASKS = {
    "create-audio": step_create_audio,
    "create-srt": step_create_srt,
    "create-characters": step_create_characters,
    "create-scenes": step_create_scenes,
    "edit-scenes": step_edit_scenes,
    "create-video": step_create_video,
    "create-thumbnails": step_create_thumbnails,
    "create-text-on-thumbnails": step_create_text_on_thumbnails,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ No task specified.")
        print(f"Available tasks: {' | '.join(TASKS)}")
        sys.exit(1)

    task = sys.argv[1]

    if task not in TASKS:
        print(f"❌ Invalid task: {task}")
        print(f"Available tasks: {' | '.join(TASKS)}")
        sys.exit(1)

    if task == "edit-scenes":
        raw_scenes = sys.argv[2] if len(sys.argv) > 2 else ""
        raw_count = sys.argv[3] if len(sys.argv) > 3 else ""

        scene_indices = parse_scene_indices(raw_scenes)
        count = int(raw_count)

        TASKS[task](scene_indices=scene_indices, count=count)
    else:
        TASKS[task]()

    if task == "create-video":
        timer_cache.summary()
