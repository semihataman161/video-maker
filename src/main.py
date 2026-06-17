from src.services import (
    TimerService, AudioService, SubtitleRenderConfig,
    SubtitleRenderService, SubtitleSrtService,
    WatermarkConfig, WatermarkService, EffectService,
    OutroService, VideoService
)
from src.utils.file_utils import create_directories
from src.utils.chunk_utils import parse_chunks
from src.utils.image_utils import crop_images
from src.constants import (
    CHUNKS, LANGUAGE, WORDS_PER_CAPTION, WORDS_PER_SCREEN,
    AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR,
    FONTS_DIR, ASSETS_IMAGES_DIR, CHANNEL_NAME
)

create_directories([AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR])
timer = TimerService()


@timer.track("🎙 Creating Audio")
def step_create_audio():
    AudioService(
        chunks=parse_chunks(CHUNKS),
        language=LANGUAGE,
        should_include_music=True
    ).run()


@timer.track("✂️ Cropping Images")
def step_crop_images():
    crop_images(
        input_dir=ORIGINAL_IMAGES_DIR,
        output_dir=CROPPED_IMAGES_DIR,
        left_pct=0,
        top_pct=0,
        right_pct=0.06,
        bottom_pct=0,
    )


@timer.track("📝 Generating SRT")
def step_generate_srt():
    SubtitleSrtService(words_per_caption=WORDS_PER_CAPTION).run()


@timer.track("🎬 Creating Video")
def step_create_video():
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
    step_create_audio()
    step_crop_images()
    step_generate_srt()
    step_create_video()

    timer.summary()
