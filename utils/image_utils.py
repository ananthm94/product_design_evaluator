import base64
import io
from PIL import Image
from config.settings import MAX_IMAGE_SIZE


def resize_image(image: Image.Image, max_size: int = MAX_IMAGE_SIZE) -> Image.Image:
    if max(image.size) <= max_size:
        return image
    ratio = max_size / max(image.size)
    new_size = (int(image.width * ratio), int(image.height * ratio))
    return image.resize(new_size, Image.LANCZOS)


def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def image_to_data_url(image: Image.Image, format: str = "PNG") -> str:
    b64 = image_to_base64(image, format)
    mime = f"image/{format.lower()}"
    return f"data:{mime};base64,{b64}"


def load_and_resize(path: str) -> Image.Image:
    img = Image.open(path).convert("RGB")
    return resize_image(img)
