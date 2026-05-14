from src.services import AudioService, VideoService, TimerService, SubtitleService, SubtitleConfig, EffectService
from src.utils.file_utils import create_directories
from src.utils.chunk_utils import parse_chunks
from src.utils.image_utils import crop_image, crop_images
from src.utils.timeline_utils import get_timeline
from src.constants import CHUNKS, TARGET_IMAGE_SIZE, OUTPUT_DIR, AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR, \
    FONTS_DIR

# Crop Thumbnail
crop_image(
    image_path=ORIGINAL_IMAGES_DIR / "thumbnail.png",
    output_path=CROPPED_IMAGES_DIR / "thumbnail.png",
    left_pct=0,
    top_pct=0,
    right_pct=0.06,
    bottom_pct=0,
)

create_directories([AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR])

timer = TimerService()
# Creating Audio
timer.measure("🎙 Creating Audio", lambda: AudioService(parse_chunks(CHUNKS)).run())

# Cropping Images
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
# Creating Video
subtitle_config = SubtitleConfig(
    font=str(FONTS_DIR / "Montserrat-Bold.ttf"),
    fontsize=55,
    color="white",
    active_color="yellow",
    stroke_color="black",
    stroke_width=3,
    position="bottom",
    vertical_margin=200,
    words_per_chunk=4,
    word_spacing=10
)
subtitle_service = SubtitleService(
    timeline=get_timeline(),
    video_size=TARGET_IMAGE_SIZE,
    config=subtitle_config,
)
effect_service = EffectService(mode="random")
video_service = VideoService(
    subtitle_service=subtitle_service,
    effect_service=effect_service
)
timer.measure("🎬 Creating Video", lambda: video_service.run())
timer.summary()

print(f"✅ DONE → {OUTPUT_DIR}/product.mp4")
