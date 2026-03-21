from services import AudioService, ImageService, VideoService
from constants import SCRIPT, VISUAL_PLAN

print("🎙 Creating Audio...")
AudioService(SCRIPT).run()

print("🎨 Creating Images...")
ImageService(VISUAL_PLAN).run()

print("🎬 Creating Video...")
VideoService().run()

print("✅ DONE → output/product.mp4")
