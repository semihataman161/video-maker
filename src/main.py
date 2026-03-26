from services import AudioService, ImageService, VideoService, TimerService
from constants import SCRIPT, VISUAL_PLAN

timer = TimerService()

timer.measure("🎙 Creating Audio", lambda: AudioService(SCRIPT).run())
timer.measure("🎨 Creating Images", lambda: ImageService(VISUAL_PLAN).run())
timer.measure("🎬 Creating Video", lambda: VideoService().run())

timer.summary()

print("✅ DONE → output/product.mp4")
