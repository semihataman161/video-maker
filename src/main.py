import sys

from src.services.timer_service_cache import TimerServiceCache
from src.utils.file_utils import create_directories, reserve_next_file_paths
from src.utils.chunk_utils import parse_chunks
from src.constants import (
    CHUNKS, LANGUAGE, WORDS_PER_CAPTION, WORDS_PER_SCREEN,
    AUDIO_DIR, SCENES_DIR, THUMBNAILS_DIR, FONTS_DIR,
    ASSETS_IMAGES_DIR, ASSETS_VIDEOS_DIR, CHANNEL_NAME
)

create_directories([AUDIO_DIR, SCENES_DIR, THUMBNAILS_DIR])
timer_cache = TimerServiceCache()


@timer_cache.track("🎙 Creating Audio")
def step_create_audio():
    from src.services.audio_service import AudioService

    AudioService(
        chunks=parse_chunks(CHUNKS),
        language=LANGUAGE,
        should_include_music=True
    ).run()


@timer_cache.track("📝 Generating SRT")
def step_generate_srt():
    from src.services.subtitle_service.srt import SubtitleSrtService

    SubtitleSrtService(words_per_caption=WORDS_PER_CAPTION).run()


@timer_cache.track("🎨 Creating Images")
def step_create_images():
    from src.services.image_service import ImageService
    from src.services.image_service.prompt import PromptService

    prompt_service = PromptService()
    image_service = ImageService()

    prompts = prompt_service.build_scene_prompts()
    prompt_count = len(prompts)
    output_paths = reserve_next_file_paths(SCENES_DIR, prompt_count)
    seeds = [3887616371] * prompt_count
    image_service.generate_batch(prompts=prompts, output_paths=output_paths, seeds=seeds)


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


@timer_cache.track("✨ Creating Thumbnails")
def step_create_thumbnails():
    from src.services.image_service.prompt import PromptService
    from src.services.image_service import ImageService

    prompt_service = PromptService()
    thumbnails = prompt_service.get_thumbnails()

    image_service = ImageService()

    prompts = prompt_service.build_thumbnail_prompts()
    prompt_count = len(prompts)
    output_paths = [THUMBNAILS_DIR / f"{thumbnail['id']}.png" for thumbnail in thumbnails]
    seeds = [3887616371] * prompt_count
    image_service.generate_batch(prompts=prompts, output_paths=output_paths, seeds=seeds)


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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = sys.argv[1]

        if task == "audio":
            step_create_audio()

        elif task == "srt":
            step_generate_srt()

        elif task == "images":
            step_create_images()

        elif task == "video":
            step_create_video()
            timer_cache.summary()

        elif task == "thumbnails":
            step_create_thumbnails()

        elif task == "text-on-thumbnails":
            step_create_text_on_thumbnails()

        else:
            print(f"❌ Unknown command: {task}")
    else:
        print("❌ Please specify a task: 'audio', 'srt', 'images' or 'video'")
