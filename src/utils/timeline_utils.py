import json
from typing import Any

from src.constants import AUDIO_DIR

timeline_path = AUDIO_DIR / "timeline.json"


def save_timeline(timeline: list[dict]):
    with open(timeline_path, "w") as file:
        json.dump(timeline, file, indent=2)

    print(f"📝 Timeline saved → {timeline_path}")


def get_timeline() -> list[dict[str, Any]]:
    if not timeline_path.exists():
        raise ValueError(f"Timeline file not found: {timeline_path}")

    with open(timeline_path) as file:
        timeline = json.load(file)

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
