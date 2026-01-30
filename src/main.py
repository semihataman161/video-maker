from services import ScriptService, AudioService, ImageService, VideoService, SubtitleService

print("🧠 Creating Script, and ✂️ Chunks...")
ScriptService().run()

print("🎙 Creating Audio...")
AudioService().run()

print("🎨 Creating Images...")
ImageService().run()

print("🎬 Creating Video...")
VideoService().run()

print("📝 Creating Subtitles...")
SubtitleService().run()

print("✅ DONE → output/product.mp4")
