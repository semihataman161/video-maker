TTS_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit"
ALIGNMENT_MODEL = "mlx-community/Qwen3-ForcedAligner-0.6B-8bit"

CHUNK_PAUSE = 0.4
SENTENCE_PAUSE = 0.3
OUTRO_PAUSE = 1.0
SAMPLE_RATE = 24000

from src.utils.file_utils import get_parent_directory

SPEAKERS_DIR = get_parent_directory(__file__) / "speakers"
