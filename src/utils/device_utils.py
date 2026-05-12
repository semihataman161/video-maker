import torch


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def get_dtype(device: str):
    if device == "cuda":
        return torch.float16
    return torch.float32
