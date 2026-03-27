import torch


def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def get_dtype(device: str):
    if device in ("cuda", "mps"):
        return torch.float16
    return torch.float32
