import os
from PIL import Image


def crop_image(
        image_path: str,
        output_path: str,
        left_pct: float,
        top_pct: float,
        right_pct: float,
        bottom_pct: float
):
    with Image.open(image_path) as img:
        width, height = img.size

        left = int(width * left_pct)
        top = int(height * top_pct)
        right = int(width * (1 - right_pct))
        bottom = int(height * (1 - bottom_pct))

        cropped = img.crop((left, top, right, bottom))
        cropped.save(output_path)

    return output_path


def crop_images(
        input_dir: str,
        output_dir: str,
        left_pct: float,
        top_pct: float,
        right_pct: float,
        bottom_pct: float
):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            crop_image(
                input_path,
                output_path,
                left_pct,
                top_pct,
                right_pct,
                bottom_pct
            )
