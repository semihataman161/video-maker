import sys

from src.services.timer_service_cache import TimerServiceCache
from src.utils.file_utils import create_directories
from src.utils.chunk_utils import parse_chunks
from src.constants import (
    CHUNKS, LANGUAGE, WORDS_PER_CAPTION, WORDS_PER_SCREEN,
    AUDIO_DIR, ORIGINAL_IMAGES_DIR, FONTS_DIR,
    ASSETS_IMAGES_DIR, CHANNEL_NAME
)

create_directories([AUDIO_DIR, ORIGINAL_IMAGES_DIR])
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

    prompt = '''
    A cinematic illustrated storyboard frame.

    Daniel, a 30-year-old man with medium-length dark brown wavy hair, light stubble, expressive brown eyes, wearing a navy blue henley sweater over a light gray undershirt, sits at a wooden table inside a small coastal cottage.

    He carefully pours fine sand into a large transparent glass jar. Small stones are scattered on the table beside a cloth pouch. Behind him, a bright harbor window reveals calm water, fishing boats, stone docks and distant seaside buildings.

    Warm natural daylight enters through the window and softly illuminates the scene.

    Style: premium storybook illustration, painterly digital art, subtle brushwork, clean contours, realistic anatomy, emotional facial expression, cinematic lighting, animated feature film concept art, visual novel illustration, high-end editorial artwork, cozy atmosphere, soft shadows, detailed glass reflections, narrative-focused composition.

    Medium shot, eye-level camera, shallow depth of field, highly consistent character design, professional storyboard quality, beautiful environmental storytelling.
    '''

    ImageService().generate_batch(prompts=[prompt] * 5)


@timer_cache.track("🎬 Creating Video")
def step_create_video():
    from src.services.watermark_service import WatermarkConfig, WatermarkService
    from src.services.subtitle_service.render import SubtitleRenderConfig, SubtitleRenderService
    from src.services.effect_service import EffectService
    from src.services.outro_service import OutroService
    from src.services.video_service import VideoService

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
        outro_service=outro_service
    ).run()


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

        else:
            print(f"❌ Unknown command: {task}")
    else:
        print("❌ Please specify a task: 'audio', 'srt', 'images' or 'video'")
