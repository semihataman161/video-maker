from pathlib import Path

from src.utils.file_utils import try_read_json
from .constants import DATA_DIR


class PromptService:
    def __init__(self, characters: dict[str, Path] | None = None):
        self.characters = characters or {}

        self.bible = try_read_json(DATA_DIR / "project_bible.json")
        self.scenes = try_read_json(DATA_DIR / "scene_metadata.json").get("scenes", [])
        self.thumbnails = try_read_json(DATA_DIR / "thumbnail_metadata.json").get("thumbnails", [])

    def get_bible(self):
        return self.bible

    def get_scenes(self):
        return self.scenes

    def get_thumbnails(self):
        return self.thumbnails

    def get_scene_character_ids(self, scene: dict) -> list[str]:
        return [character["id"] for character in self.__ordered_scene_characters(scene)]

    def get_thumbnail_character_ids(self, thumbnail: dict) -> list[str]:
        return [character[0]["id"] for character in self.__ordered_thumbnail_characters(thumbnail)]

    def __get_character_ids(self) -> list[str]:
        return list(self.bible.get("characters", {}).keys())

    @staticmethod
    def __ordered_scene_characters(scene: dict) -> list[dict]:
        return sorted(scene.get("characters", []), key=lambda character: character.get("role") != "primary")

    @staticmethod
    def __ordered_thumbnail_characters(thumbnail: dict) -> list[tuple[dict, str | None, str | None]]:
        composition = thumbnail.get("composition", {})
        entries = []

        primary = thumbnail.get("primary_character")

        if primary:
            entries.append((
                primary,
                composition.get("primary_subject_position"),
                composition.get("primary_subject_depth"),
            ))

        for secondary in thumbnail.get("secondary_characters", []):
            entries.append((
                secondary,
                composition.get("secondary_subject_position"),
                composition.get("secondary_subject_depth"),
            ))

        return entries

    @staticmethod
    def __resolve_references(character_ids: list[str], characters: dict[str, Path]) -> list[Path]:
        missing = [cid for cid in character_ids if cid not in characters]

        if missing:
            raise ValueError(f"Missing character: {missing}")

        return [characters[cid] for cid in character_ids]

    @staticmethod
    def __clothing_sentence(character: dict, upper_body_only: bool = False) -> str | None:
        clothing = character.get("default_clothing", {})

        keys = ("upper", "outerwear") if upper_body_only else ("upper", "lower", "footwear", "outerwear")
        clothes = [clothing.get(key) for key in keys]
        clothes = [cloth for cloth in clothes if cloth]

        if not clothes:
            return None

        if upper_body_only:
            return f"wearing {', '.join(clothes)}."

        acc = clothing.get("accessories", [])
        acc_str = f", accessorized with {', '.join(acc)}" if acc else ""

        return f"wearing {', '.join(clothes)}{acc_str}."

    @staticmethod
    def __reference_instruction(count: int):
        refs = " and ".join(f"Picture {i}" for i in range(1, count + 1))
        plural = count > 1

        return (
            f"{refs} {'are' if plural else 'is'} character reference image"
            f"{'s' if plural else ''}. Reproduce the referenced character"
            f"{'s' if plural else ''} in a completely new scene, keeping "
            f"{'their' if plural else 'the'} face, hair, and clothing exactly identical "
            f"to the reference. Do not copy the reference pose, composition, or background."
        )

    def __identity_sentence(self, character: dict, index: int):
        char_name = character.get("name", "The character")
        descriptor = character.get("scene_descriptor") or character["identity_blend"]
        return f"{char_name} (Picture {index + 1}), {descriptor},"

    @staticmethod
    def __clean(parts: list[str]):
        final = " ".join(p.strip() for p in parts if p)
        return final.replace(".,", ",").replace("..", ".")

    def __build_character_prompt(self, character_id: str):
        character = self.bible["characters"][character_id]
        parts = []

        visual_style = self.bible.get("visual_style")

        if visual_style:
            parts.append(f"{visual_style.strip('.')}.")

        parts.append("Full-body character reference sheet. Camera: full shot, head to feet, eye level.")

        char_name = character.get("name", "The character")
        parts.append(f"{char_name}, {character['identity_blend'].strip('.')}.")

        clothing = self.__clothing_sentence(character)

        if clothing:
            parts.append(clothing.capitalize())

        parts.append(
            "Standing upright, facing the camera, neutral expression, looking forward. "
            "Plain neutral grey background, soft even lighting, face clearly visible, "
            "single subject, no other people in the frame."
        )

        return self.__clean(parts)

    def build_character_prompts(self) -> dict[str, str]:
        return {
            character_id: self.__build_character_prompt(character_id)
            for character_id in self.__get_character_ids()
        }

    def __build_scene_prompt(self, scene: dict):
        parts = []

        # ======================================================
        # 1. VISUAL STYLE
        # ======================================================
        visual_style = self.bible.get("visual_style")

        if visual_style:
            parts.append(f"{visual_style.strip('.')}.")

        # ======================================================
        # 1.5 REFERENCE INSTRUCTION
        # ======================================================
        characters = self.__ordered_scene_characters(scene)

        if characters:
            parts.append(self.__reference_instruction(len(characters)))

        # ======================================================
        # 2. CAMERA
        # ======================================================
        camera = scene.get("camera", {})
        cam_parts = [c for c in [camera.get("shot_size"), camera.get("angle")] if c]

        if camera.get("focus"):
            cam_parts.append(f"focused on {camera['focus']}")

        if cam_parts:
            parts.append(f"Camera: {', '.join(cam_parts)}.")

        # ======================================================
        # 3. SETTING & ENVIRONMENT
        # ======================================================
        env_parts = []

        if scene.get("scene_setting"):
            env_parts.append(scene["scene_setting"])

        if scene.get("time_of_day"):
            env_parts.append(scene["time_of_day"])

        if scene.get("weather"):
            env_parts.append(f"{scene['weather']} weather")

        if env_parts:
            parts.append(f"Setting is a {', '.join(env_parts).lower()}.")

        location_id = scene.get("location")

        if location_id and location_id in self.bible.get("locations", {}):
            location = self.bible["locations"][location_id]

            if location.get("visual_identity"):
                parts.append(f"{location['visual_identity'].strip('.')}.")

            if location.get("background_elements"):
                parts.append(f"Background features {', '.join(location['background_elements'])}.")

        if scene.get("background"):
            parts.append(f"The scene takes place with {scene['background'].lower().strip('.')}.")

        # ======================================================
        # 4. CHARACTERS
        # ======================================================
        default_positions = ["On the left", "On the right", "In the center"]

        for idx, character_scene in enumerate(characters):
            character = self.bible["characters"][character_scene["id"]]
            char_sentence = []

            # A. Spatial Anchoring
            pos = character_scene.get("position")

            if not pos and len(characters) > 1:
                pos = default_positions[idx % len(default_positions)]

            if pos:
                char_sentence.append(f"{pos},")

            # B. Identity
            char_sentence.append(self.__identity_sentence(character, idx))

            # C. Clothing & Accessories
            clothing = self.__clothing_sentence(character)

            if clothing:
                char_sentence.append(clothing)

            # D. Action, Pose, Expression and Gaze
            action = character_scene.get("action", "standing")
            pose = character_scene.get("pose", "relaxed")
            expr = character_scene.get("expression", "neutral")
            gaze = character_scene.get("gaze", "forward")

            char_sentence.append(
                f"He is {action} in a {pose} posture, showing a {expr} expression and looking {gaze}."
            )

            parts.append(" ".join(char_sentence).replace(" ,", ","))

        # ======================================================
        # 5. OBJECTS
        # ======================================================
        for object_id in scene.get("objects", []):
            obj = self.bible["objects"].get(object_id)

            if obj and obj.get("appearance"):
                parts.append(f"Nearby object: {obj['appearance'].strip('.')}.")

        return self.__clean(parts)

    def build_scene_prompts(self):
        return [self.__build_scene_prompt(scene) for scene in self.scenes]

    def build_scene_references(self) -> list[list[Path]]:
        return [
            self.__resolve_references(self.get_scene_character_ids(scene), self.characters)
            for scene in self.scenes
        ]

    def __build_thumbnail_prompt(self, thumbnail: dict):
        parts = []

        # ======================================================
        # 1. VISUAL STYLE
        # ======================================================
        visual_style = self.bible.get("visual_style")

        if visual_style:
            parts.append(f"{visual_style.strip('.')}.")

        parts.append(
            "YouTube thumbnail composition, extreme facial emphasis, "
            "face fills nearly half of the frame, dramatic saturated colors, "
            "strong glowing rim light, simplified minimal background."
        )

        # ======================================================
        # 1.5 REFERENCE INSTRUCTION
        # ======================================================
        char_entries = self.__ordered_thumbnail_characters(thumbnail)

        if char_entries:
            parts.append(self.__reference_instruction(len(char_entries)))

        # ======================================================
        # 2. CAMERA
        # ======================================================
        camera = thumbnail.get("camera", {})
        cam_parts = [c for c in [camera.get("shot_size"), camera.get("angle")] if c]

        if camera.get("focus"):
            cam_parts.append(f"focused on {camera['focus']}")

        if cam_parts:
            parts.append(f"Camera: {', '.join(cam_parts)}.")

        # ======================================================
        # 3. LOCATION
        # ======================================================
        location_id = thumbnail.get("location")

        if location_id and location_id in self.bible.get("locations", {}):
            location = self.bible["locations"][location_id]

            if location.get("visual_identity"):
                parts.append(f"{location['visual_identity'].strip('.')}.")

        # ======================================================
        # 4. CHARACTERS (primary first, then secondaries)
        # ======================================================
        composition = thumbnail.get("composition", {})

        for idx, (character_scene, position, depth) in enumerate(char_entries):
            character = self.bible["characters"][character_scene["id"]]
            char_sentence = []

            # A. Spatial Anchoring
            anchor_parts = [p for p in [position, depth] if p]

            if anchor_parts:
                char_sentence.append(f"Positioned at the {', in the '.join(anchor_parts)} of the frame,")

            # B. Identity
            char_sentence.append(self.__identity_sentence(character, idx))

            # C. Clothing (close-up: sadece üst gövde)
            clothing = self.__clothing_sentence(character, upper_body_only=True)

            if clothing:
                char_sentence.append(clothing)

            # D. Action, Pose, Expression and Gaze
            action = character_scene.get("action", "standing")
            pose = character_scene.get("pose", "relaxed")
            expr = character_scene.get("expression", "neutral")
            gaze = character_scene.get("gaze", "forward")

            char_sentence.append(
                f"He is {action} in a {pose} posture, with {expr}, looking {gaze}."
            )

            parts.append(" ".join(char_sentence).replace(" ,", ","))

        # ======================================================
        # 5. COMPOSITION
        # ======================================================
        comp_parts = []

        if composition.get("subject_scale"):
            comp_parts.append(f"the main subject occupies a {composition['subject_scale']} portion of the frame")

        if composition.get("text_safe_area"):
            comp_parts.append(f"clean empty negative space in the {composition['text_safe_area']} of the frame")

        if composition.get("background_complexity"):
            comp_parts.append(f"{composition['background_complexity']} background complexity")

        if comp_parts:
            parts.append(f"Composition: {', '.join(comp_parts)}.")

        # ======================================================
        # 6. LIGHTING
        # ======================================================
        lighting = thumbnail.get("lighting", {})
        light_parts = []

        if lighting.get("style"):
            light_parts.append(lighting["style"])

        if lighting.get("direction"):
            light_parts.append(lighting["direction"])

        if lighting.get("contrast"):
            light_parts.append(f"{lighting['contrast']} contrast")

        if lighting.get("rim_light"):
            light_parts.append(lighting["rim_light"])

        if light_parts:
            parts.append(f"Lighting: {', '.join(light_parts)}.")

        # ======================================================
        # 7. COLOR SCHEME
        # ======================================================
        color_scheme = thumbnail.get("color_scheme", {})
        color_parts = []

        if color_scheme.get("dominant_colors"):
            color_parts.append(f"dominant colors of {', '.join(color_scheme['dominant_colors'])}")

        if color_scheme.get("accent_colors"):
            color_parts.append(f"accent colors of {', '.join(color_scheme['accent_colors'])}")

        if color_scheme.get("contrast"):
            color_parts.append(f"{color_scheme['contrast']} color contrast")

        if color_parts:
            parts.append(f"Color palette: {', '.join(color_parts)}.")

        # ======================================================
        # 8. EFFECTS
        # ======================================================
        effects = thumbnail.get("effects", {})
        effect_parts = []

        if effects.get("subject_separation"):
            effect_parts.append(f"{effects['subject_separation']} subject separation from the background")

        if effects.get("background_blur"):
            effect_parts.append(f"{effects['background_blur']} background blur")

        if effects.get("volumetric_light"):
            effect_parts.append(f"volumetric light with {effects['volumetric_light']}")

        if effect_parts:
            parts.append(f"Effects: {', '.join(effect_parts)}.")

        # ======================================================
        # 9. OBJECTS
        # ======================================================
        for object_id in thumbnail.get("objects", []):
            obj = self.bible["objects"].get(object_id)

            if obj and obj.get("appearance"):
                parts.append(f"Nearby object: {obj['appearance'].strip('.')}.")

        return self.__clean(parts)

    def build_thumbnail_prompts(self):
        return [self.__build_thumbnail_prompt(t) for t in self.thumbnails]

    def build_thumbnail_references(self) -> list[list[Path]]:
        return [
            self.__resolve_references(self.get_thumbnail_character_ids(thumbnail), self.characters)
            for thumbnail in self.thumbnails
        ]
