from src.services import AudioService, VideoService, TimerService
from src.utils.chunk_utils import parse
from src.constants import CHUNKS

parsed_chunks = parse(CHUNKS)

timer = TimerService()

timer.measure("🎙 Creating Audio", lambda: AudioService(parsed_chunks).run())
timer.measure("🎬 Creating Video", lambda: VideoService().run())

timer.summary()

print("✅ DONE → output/product.mp4")
