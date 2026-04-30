from src.services import AudioService, VideoService, TimerService
from src.utils.chunk_parser import parse_chunks

timer = TimerService()

# 👇 ChatGPT CHUNK OUTPUT
RAW_CHUNKS = """
1) Liam was twenty-eight years old. He lived in a small mountain town.
2) For the past year, he had felt stuck. Every day felt the same.
3) One cold afternoon, Liam walked past the community garden.
"""

chunks = parse_chunks(RAW_CHUNKS)

timer.measure("🎙 Creating Audio", lambda: AudioService(chunks).run())
timer.measure("🎬 Creating Video", lambda: VideoService().run())

timer.summary()

print("✅ DONE → output/product.mp4")
