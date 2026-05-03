from src.services import AudioService, VideoService, TimerService
from src.utils.chunk_utils import parse_chunks
from src.utils.image_utils import crop_images
from src.constants import CHUNKS

timer = TimerService()

timer.measure("🎙 Creating Audio", lambda: AudioService(parse_chunks(CHUNKS)).run())
timer.measure("✂️ Cropping Images", lambda: crop_images(
    input_dir="output/images/original",
    output_dir="output/images/cropped",
    left_pct=0,
    top_pct=0,
    right_pct=0.06,
    bottom_pct=0
))
timer.measure("🎬 Creating Video", lambda: VideoService().run())

timer.summary()

print("✅ DONE → output/product.mp4")
