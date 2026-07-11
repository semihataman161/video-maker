from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


@dataclass
class ImageTextOverlayConfig:
    font_path: Path
    text_color: tuple = (255, 255, 255, 255)
    stroke_color: tuple = (0, 0, 0, 255)
    stroke_width_ratio: int = 14
    shadow_color: tuple = (0, 0, 0, 180)
    shadow_offset_ratio: float = 0.045
    shadow_blur_radius: int = 10
    glow_enabled: bool = False
    glow_color: tuple = (255, 210, 140, 110)
    glow_blur_radius: int = 24
    glow_passes: int = 1
    margin_ratio: float = 0.06
    line_spacing_ratio: float = 0.05
    max_font_size: int = 220
    min_font_size: int = 40


class ImageTextOverlayService:
    def __init__(self, config: ImageTextOverlayConfig):
        self.config = config

    def __resolve_text_box(self, area: str, width: int, height: int,
                           area_fill_ratio: float) -> dict:
        """Translate a named area into pixel boundaries."""
        margin = int(width * self.config.margin_ratio)
        area = area.lower()

        if "left" in area:
            x_start, x_end = margin, width // 2 - margin
        elif "right" in area:
            x_start, x_end = width // 2 + margin, width - margin
        else:  # full width
            x_start, x_end = margin, width - margin

        usable_width = x_end - x_start

        return {
            "x_start": x_start,
            "x_end": x_end,
            "max_width": int(usable_width * area_fill_ratio),
            "max_height": int(height * 0.7),
            "margin": margin,
        }

    def __fit_font_and_lines(self, draw, text: str, max_width: int, max_height: int):
        """Find the largest font size where wrapped text fits the target box."""
        words = text.split()

        for font_size in range(self.config.max_font_size, self.config.min_font_size, -8):
            font = ImageFont.truetype(str(self.config.font_path), font_size)

            # Greedy word wrap
            lines, current = [], []
            for word in words:
                candidate = " ".join(current + [word])
                if draw.textlength(candidate, font=font) <= max_width:
                    current.append(word)
                else:
                    if current:
                        lines.append(" ".join(current))
                    current = [word]
            if current:
                lines.append(" ".join(current))

            line_height = font_size + int(font_size * self.config.line_spacing_ratio)
            total_height = line_height * len(lines)

            longest = max(draw.textlength(line, font=font) for line in lines)

            if total_height <= max_height and longest <= max_width:
                return font, lines, line_height

        # Fallback: smallest allowed size, single line
        font = ImageFont.truetype(str(self.config.font_path), self.config.min_font_size)
        line_height = self.config.min_font_size + int(
            self.config.min_font_size * self.config.line_spacing_ratio
        )
        return font, [text], line_height

    def __render_layers(self, size, lines, font, line_height,
                        box: dict, vertical_align: str):
        """Render drop shadow, optional glow and text as separate RGBA layers."""
        text_layer = Image.new("RGBA", size, (0, 0, 0, 0))
        shadow_layer = Image.new("RGBA", size, (0, 0, 0, 0))
        glow_layer = Image.new("RGBA", size, (0, 0, 0, 0))

        text_draw = ImageDraw.Draw(text_layer)
        shadow_draw = ImageDraw.Draw(shadow_layer)
        glow_draw = ImageDraw.Draw(glow_layer)

        img_height = size[1]

        # Visual (ink) metrics instead of em-box math:
        # top gap of the first line and bottom of the last line
        first_bbox = font.getbbox(lines[0])
        last_bbox = font.getbbox(lines[-1])

        top_offset = first_bbox[1]  # empty headroom above glyphs
        visual_height = (len(lines) - 1) * line_height + (last_bbox[3] - top_offset)

        if vertical_align == "top":
            y = box["margin"] - top_offset
        elif vertical_align == "bottom":
            y = img_height - visual_height - box["margin"] - top_offset
        else:  # center
            y = (img_height - visual_height) // 2 - top_offset

        stroke_width = max(3, font.size // self.config.stroke_width_ratio)
        shadow_offset = int(font.size * self.config.shadow_offset_ratio)
        usable_width = box["x_end"] - box["x_start"]

        for line in lines:
            line_width = text_draw.textlength(line, font=font)
            x = box["x_start"] + (usable_width - line_width) // 2

            # 1. Drop shadow (offset copy, stroke included so edges are shadowed too)
            shadow_draw.text(
                (x + shadow_offset, y + shadow_offset), line, font=font,
                fill=self.config.shadow_color,
                stroke_width=stroke_width,
                stroke_fill=self.config.shadow_color
            )

            # 2. Optional glow (thin, soft)
            if self.config.glow_enabled:
                glow_draw.text(
                    (x, y), line, font=font,
                    fill=self.config.glow_color,
                    stroke_width=stroke_width,
                    stroke_fill=self.config.glow_color
                )

            # 3. Actual text: white with thick black stroke
            text_draw.text(
                (x, y), line, font=font,
                fill=self.config.text_color,
                stroke_width=stroke_width,
                stroke_fill=self.config.stroke_color
            )

            y += line_height

        shadow_layer = shadow_layer.filter(
            ImageFilter.GaussianBlur(self.config.shadow_blur_radius)
        )

        if self.config.glow_enabled:
            blurred_glow = glow_layer.filter(
                ImageFilter.GaussianBlur(self.config.glow_blur_radius)
            )
            for _ in range(self.config.glow_passes - 1):
                blurred_glow = Image.alpha_composite(
                    blurred_glow,
                    glow_layer.filter(ImageFilter.GaussianBlur(self.config.glow_blur_radius))
                )
            glow_layer = blurred_glow

        return shadow_layer, glow_layer, text_layer

    def run(
            self,
            image_path: Path,
            text: str,
            output_path: Path,
            area: str = "left half",
            vertical_align: str = "center",
            uppercase: bool = True,
            area_fill_ratio: float = 0.9,
    ):
        image = Image.open(image_path).convert("RGBA")
        width, height = image.size

        box = self.__resolve_text_box(area, width, height, area_fill_ratio)

        draw = ImageDraw.Draw(image)
        font, lines, line_height = self.__fit_font_and_lines(
            draw,
            text.upper() if uppercase else text,
            box["max_width"],
            box["max_height"],
        )

        shadow_layer, glow_layer, text_layer = self.__render_layers(
            image.size, lines, font, line_height, box, vertical_align
        )

        composed = Image.alpha_composite(image, shadow_layer)
        composed = Image.alpha_composite(composed, glow_layer)
        composed = Image.alpha_composite(composed, text_layer)

        composed.convert("RGB").save(output_path)
