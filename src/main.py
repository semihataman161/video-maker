from src.services import AudioService, VideoService, TimerService, SubtitleService, SubtitleConfig
from src.utils.directory_utils import create_directories
from src.utils.chunk_utils import parse_chunks
from src.utils.image_utils import crop_images
from src.utils.timeline_utils import get_timeline
from src.constants import CHUNKS, TARGET_IMAGE_SIZE, OUTPUT_DIR, AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR, \
    FONTS_DIR

create_directories([AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR])

timer = TimerService()
timer.measure("🎙 Creating Audio", lambda: AudioService(parse_chunks(CHUNKS)).run())
timer.measure(
    "✂️ Cropping Images",
    lambda: crop_images(
        input_dir=ORIGINAL_IMAGES_DIR,
        output_dir=CROPPED_IMAGES_DIR,
        left_pct=0,
        top_pct=0,
        right_pct=0.06,
        bottom_pct=0,
    )
)
subtitle_config = SubtitleConfig(
    font=str(FONTS_DIR / "Montserrat-Bold.ttf"),
    fontsize=55,
    color="white",
    stroke_color="black",
    stroke_width=3,
    position="bottom",
    margin=200,
    wrap_width=32,
)
subtitle_service = SubtitleService(
    timeline=get_timeline(),
    video_size=TARGET_IMAGE_SIZE,
    config=subtitle_config,
)
timer.measure("🎬 Creating Video", lambda: VideoService(subtitle_service=subtitle_service).run())
timer.summary()

print(f"✅ DONE → {OUTPUT_DIR}/product.mp4")
