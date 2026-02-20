from services import AudioService, ImageService, VideoService
from constants import SCRIPT

print("🎙 Creating Audio...")
AudioService(SCRIPT).run()

'''
print("🎨 Creating Images...")
ImageService().run()

print("🎬 Creating Video...")
VideoService().run()

print("✅ DONE → output/product.mp4")
'''
