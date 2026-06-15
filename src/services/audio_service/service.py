import os
import re
import subprocess
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model
from mlx_audio.stt import load
from pydub import AudioSegment
from pathlib import Path

from src.utils.file_utils import validate_path, validate_paths
from src.utils.timeline_utils import save_timeline
from src.utils.chunk_utils import split_sentences
from src.constants import AUDIO_DIR, MUSICS_DIR
from .constants import TTS_MODEL, ALIGNMENT_MODEL, CHUNK_PAUSE, SENTENCE_PAUSE, OUTRO_PAUSE, SAMPLE_RATE, SPEAKERS_DIR

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


class AudioService:
    def __init__(self, chunks: list[str], language: str, should_include_music: bool):
        self.chunks = chunks
        self.language = language
        self.should_include_music = should_include_music

        if should_include_music:
            validate_path(MUSICS_DIR)

        speaker_dir = SPEAKERS_DIR / language
        self.speaker_wav = speaker_dir / "index.wav"
        self.ref_text_path = speaker_dir / "index.txt"

        validate_paths([self.speaker_wav, self.ref_text_path])

        self.speaker_wav = self.__prepare_reference_audio()
        self.ref_text = self.ref_text_path.read_text(encoding="utf-8").strip()

        print("🔊 Loading Qwen3-TTS (MLX)...")
        self.tts_model = load_model(TTS_MODEL)

        print("🗣️ Loading Qwen3-ForcedAligner...")
        self.alignment_model = load(ALIGNMENT_MODEL)

    def __prepare_reference_audio(self):
        ref_path = Path(self.speaker_wav)
        file_name = f"{ref_path.stem}_24k_mono.wav"
        converted_path = ref_path.parent / file_name

        if converted_path.exists():
            print(f"[{converted_path}] is already in the required format. Skipping conversion.")
            return str(converted_path)

        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(ref_path),
                "-ac", "1",
                "-ar", str(SAMPLE_RATE),
                "-sample_fmt", "s16",
                str(converted_path),
            ],
            capture_output=True,
            check=True,
        )

        return converted_path

    def __generate_sentence_audio(self, sentence: str) -> np.ndarray:
        results = list(self.tts_model.generate(
            text=sentence,
            ref_audio=str(self.speaker_wav),
            ref_text=self.ref_text,
            temperature=0.8,
        ))

        all_audio = [
            np.array(r.audio, dtype=np.float32)
            for r in results
            if r.audio is not None
        ]

        if not all_audio:
            raise RuntimeError(f"Audio data is empty: {sentence[:50]}...")

        return np.concatenate(all_audio) if len(all_audio) > 1 else all_audio[0]

    def __generate_audio_file(self, index: int, text: str):
        temp_path = AUDIO_DIR / f"chunk_{index}.wav"

        sentences = split_sentences(text)
        silence = np.zeros(int(SAMPLE_RATE * SENTENCE_PAUSE), dtype=np.float32)

        audio_parts = []
        for sentence in sentences:
            audio_parts.append(self.__generate_sentence_audio(sentence))
            audio_parts.append(silence)

        if audio_parts:
            audio_parts.pop()

        audio_array = np.concatenate(audio_parts)
        sf.write(str(temp_path), audio_array, SAMPLE_RATE)
        return temp_path

    @staticmethod
    def __load_audio_segment(path: Path) -> tuple[AudioSegment, float]:
        segment = AudioSegment.from_wav(path)
        return segment, len(segment) / 1000

    @staticmethod
    def __reattach_punctuation(aligned_words: list[dict], original_text: str):
        original_tokens = original_text.split()

        def strip_punct(token: str):
            return re.sub(r"[^\w']", "", token).lower()

        stripped_originals = [strip_punct(t) for t in original_tokens]

        match_idx = 0
        for word_entry in aligned_words:
            aligned_clean = strip_punct(word_entry["word"])

            while match_idx < len(stripped_originals):
                if stripped_originals[match_idx] == aligned_clean:
                    word_entry["word"] = original_tokens[match_idx]
                    match_idx += 1
                    break
                match_idx += 1

        return aligned_words

    def __align_words(self, audio_path: Path, text: str, offset: float):
        words = []

        result = self.alignment_model.generate(str(audio_path), text=text, language=self.language)

        for item in result:
            words.append({
                "word": item.text.strip(),
                "start": float(item.start_time) + offset,
                "end": float(item.end_time) + offset,
            })

        words = self.__reattach_punctuation(words, text)
        return words

    def __process_chunk(self, index: int, chunk: str, combined: AudioSegment, current_time: float, total_chunks: int):
        temp_path = self.__generate_audio_file(index, chunk)
        segment, duration = self.__load_audio_segment(temp_path)

        words = self.__align_words(temp_path, chunk, current_time)

        current_pause = CHUNK_PAUSE

        if index == total_chunks - 1 and OUTRO_PAUSE > 0:
            current_pause = OUTRO_PAUSE

        timeline_entry = {
            "index": index,
            "text": chunk,
            "start": current_time,
            "end": current_time + duration,
            "duration": duration,
            "pause": current_pause,
            "words": words,
        }

        silence = AudioSegment.silent(duration=int(current_pause * 1000))
        combined = combined + segment + silence
        return combined, timeline_entry, current_time + duration + current_pause

    def __build_dynamic_playlist(self, total_chunks: int) -> list[dict]:
        p1 = max(1, int(total_chunks * 0.10))
        p2 = max(p1 + 1, int(total_chunks * 0.35))
        p3 = max(p2 + 1, int(total_chunks * 0.60))
        p4 = max(p3 + 1, int(total_chunks * 0.85))

        return [
            {
                "path": MUSICS_DIR / "1.wav",
                "start_chunk": 1,
                "end_chunk": p1,
                "gain": -14
            },
            {
                "path": MUSICS_DIR / "2.wav",
                "start_chunk": p1 + 1,
                "end_chunk": p2,
                "gain": -12
            },
            {
                "path": MUSICS_DIR / "3.wav",
                "start_chunk": p2 + 1,
                "end_chunk": p3,
                "gain": -26
            },
            {
                "path": MUSICS_DIR / "4.wav",
                "start_chunk": p3 + 1,
                "end_chunk": p4,
                "gain": -18
            },
            {
                "path": MUSICS_DIR / "5.wav",
                "start_chunk": p4 + 1,
                "end_chunk": total_chunks,
                "gain": -16
            }
        ]

    def __apply_background_music(self, voiceover: AudioSegment, timeline: list[dict]):
        total_chunks = len(self.chunks)
        playlist = self.__build_dynamic_playlist(total_chunks)

        if not playlist or not timeline:
            return voiceover

        music_bed = AudioSegment.silent(duration=len(voiceover))
        timeline_map = {entry["index"]: entry for entry in timeline}

        for music_info in playlist:
            music_path = Path(music_info["path"])
            validate_path(str(music_path))

            start_chunk = music_info["start_chunk"]
            end_chunk = music_info["end_chunk"]

            if start_chunk not in timeline_map:
                raise ValueError(f"Target start_chunk '{start_chunk}' does not exist in the timeline mapping.")

            start_ms = int(timeline_map[start_chunk]["start"] * 1000)

            if end_chunk in timeline_map:
                end_ms = int(timeline_map[end_chunk]["end"] * 1000)
            else:
                max_chunk = max(timeline_map.keys())
                end_ms = int(timeline_map[max_chunk]["end"] * 1000)

            duration_needed = end_ms - start_ms

            if start_ms + duration_needed > len(voiceover):
                duration_needed = len(voiceover) - start_ms

            track = AudioSegment.from_file(music_path)
            track = track + music_info.get("gain", -22)

            if len(track) < duration_needed:
                loop_count = int(duration_needed / len(track)) + 1
                track = track * loop_count

            track = track[:duration_needed]
            track = track.fade_in(1500).fade_out(1500)
            music_bed = music_bed.overlay(track, position=start_ms)

        music_bed = music_bed.fade_out(2000)
        return voiceover.overlay(music_bed)

    def run(self):
        combined = AudioSegment.empty()
        timeline = []
        current_time = 0

        total = len(self.chunks)
        for i, chunk in enumerate(self.chunks, start=1):
            print(f"   ⏳ Chunk {i}/{total}: {chunk[:50]}...")
            combined, entry, current_time = self.__process_chunk(i, chunk, combined, current_time, total)
            timeline.append(entry)
            print(f"   ✅ Chunk {i}/{total} done")

        if self.should_include_music:
            print("\n   🎵 Applying background music to the final audio...")
            final_audio = self.__apply_background_music(combined, timeline)
            print("   ✅ Background music has been applied to the final audio.")
        else:
            final_audio = combined

        final_path = AUDIO_DIR / "merged.wav"
        final_audio.export(final_path, format="wav")
        save_timeline(timeline)
