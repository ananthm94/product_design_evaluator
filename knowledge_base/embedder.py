import numpy as np
import torch
from PIL import Image
import open_clip
from config.settings import CLIP_MODEL_NAME, CLIP_PRETRAINED


_model = None
_preprocess = None
_tokenizer = None


def _load_model():
    global _model, _preprocess, _tokenizer
    if _model is None:
        _model, _, _preprocess = open_clip.create_model_and_transforms(
            CLIP_MODEL_NAME, pretrained=CLIP_PRETRAINED
        )
        _tokenizer = open_clip.get_tokenizer(CLIP_MODEL_NAME)
        _model.eval()
    return _model, _preprocess, _tokenizer


def embed_image(image: Image.Image) -> list[float]:
    model, preprocess, _ = _load_model()
    image_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        features = model.encode_image(image_tensor)
        features /= features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy().flatten().tolist()


def embed_text(text: str) -> list[float]:
    model, _, tokenizer = _load_model()
    tokens = tokenizer([text])
    with torch.no_grad():
        features = model.encode_text(tokens)
        features /= features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy().flatten().tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    model, _, tokenizer = _load_model()
    tokens = tokenizer(texts)
    with torch.no_grad():
        features = model.encode_text(tokens)
        features /= features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy().tolist()


def embed_images(images: list[Image.Image]) -> list[list[float]]:
    model, preprocess, _ = _load_model()
    tensors = torch.stack([preprocess(img) for img in images])
    with torch.no_grad():
        features = model.encode_image(tensors)
        features /= features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy().tolist()
