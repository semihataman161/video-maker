from src.services import AudioService, VideoService, TimerService
from src.utils.directory_utils import create_directories
from src.utils.chunk_utils import parse_chunks
from src.utils.image_utils import crop_images
from src.constants import CHUNKS, OUTPUT_DIR, AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR

create_directories([AUDIO_DIR, ORIGINAL_IMAGES_DIR, CROPPED_IMAGES_DIR])

timer = TimerService()
timer.measure("🎙 Creating Audio", lambda: AudioService(parse_chunks(CHUNKS)).run())
timer.measure("✂️ Cropping Images", lambda: crop_images(
    input_dir=ORIGINAL_IMAGES_DIR,
    output_dir=CROPPED_IMAGES_DIR,
    left_pct=0,
    top_pct=0,
    right_pct=0.06,
    bottom_pct=0
))
timer.measure("🎬 Creating Video", lambda: VideoService().run())
timer.summary()

print(f"✅ DONE → {OUTPUT_DIR}/product.mp4")
