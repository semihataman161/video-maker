from services import OllamaService, ScriptService, AudioService, ImageService, VideoService, \
    SubtitleService

print("🧠 Creating Script, and ✂️ Chunks...")
OLLAMA_MODEL = "llama3.1:8b"
ai_service = OllamaService(OLLAMA_MODEL)
ScriptService(ai_service).run()

print("🎙 Creating Audio...")
AudioService().run()

print("🎨 Creating Images...")
ImageService().run()

print("🎬 Creating Video...")
VideoService().run()

print("📝 Creating Subtitles...")
SubtitleService().run()

print("✅ DONE → output/product.mp4")
