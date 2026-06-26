from src.constants import AUDIO_DIR
from .file_utils import try_read_json, save_json

timeline_path = AUDIO_DIR / "timeline.json"


def save_timeline(timeline: dict | list):
    save_json(timeline_path, timeline)
    print(f"📝 Timeline saved → {timeline_path}")


def get_timeline():
    timeline = try_read_json(timeline_path)

    if not timeline:
        raise RuntimeError("Timeline is empty!")

    return timeline


def get_total_duration(timeline):
    return max(
        float(scene["end"]) + float(scene["pause"])
        for scene in timeline
    )


def chunk_timeline_words(chunk_size: int):
    timeline = get_timeline()
    all_chunks = []

    for scene in timeline:
        words = scene.get("words", [])
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            if chunk:
                all_chunks.append(chunk)
    return all_chunks
