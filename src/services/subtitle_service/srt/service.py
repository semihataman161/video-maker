from src.utils.timeline_utils import chunk_timeline_words
from src.constants import OUTPUT_DIR


class SubtitleSrtService:
    def __init__(self, words_per_caption: int):
        self.chunks = chunk_timeline_words(words_per_caption)
        self.output_path = OUTPUT_DIR / "subtitles.srt"

    @staticmethod
    def __format_srt_time(seconds: float):
        total_millis = int(round(seconds * 1000))
        hours = total_millis // 3600000
        minutes = (total_millis % 3600000) // 60000
        secs = (total_millis % 60000) // 1000
        millis = total_millis % 1000
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def run(self):
        srt_content = []
        for index, chunk in enumerate(self.chunks, start=1):
            start_time = self.__format_srt_time(float(chunk[0]["start"]))
            end_time = self.__format_srt_time(float(chunk[-1]["end"]))
            text = " ".join([w["word"] for w in chunk])
            srt_content.append(f"{index}\n{start_time} --> {end_time}\n{text}\n")

        self.output_path.write_text("\n".join(srt_content), encoding="utf-8")
        print(f"   📝 SRT file perfectly synced and saved to: {self.output_path}")
