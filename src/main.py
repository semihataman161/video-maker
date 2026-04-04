from src.services import AudioService, VideoService, TimerService
from src.constants import SCRIPT

timer = TimerService()

timer.measure("🎙 Creating Audio", lambda: AudioService(SCRIPT).run())
timer.measure("🎬 Creating Video", lambda: VideoService().run())

timer.summary()

print("✅ DONE → output/product.mp4")
