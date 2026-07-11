from src.utils.file_utils import try_read_json
from .constants import DATA_DIR


class PromptService:
    def __init__(self):
        self.bible = try_read_json(DATA_DIR / "project_bible.json")
        self.scenes = try_read_json(DATA_DIR / "scene_metadata.json").get("scenes", [])
        self.thumbnails = try_read_json(DATA_DIR / "thumbnail_metadata.json").get("thumbnails", [])

    def get_bible(self):
        return self.bible

    def get_scenes(self):
        return self.scenes

    def get_thumbnails(self):
        return self.thumbnails

    def __build_scene_prompt(self, scene: dict) -> str:
        parts = []

        # ======================================================
        # 1. VISUAL STYLE
        # ======================================================
        visual_style = self.bible.get("visual_style")

        if visual_style:
            parts.append(f"{visual_style.strip('.')}.")

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
        characters = sorted(scene.get("characters", []), key=lambda c: c.get("role") != "primary")

        # Spatial anchors to prevent concept bleeding between multiple characters
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

            # B. Identity Blend
            char_name = character.get("name", "The character")
            char_sentence.append(f"{char_name}, {character['identity_blend']},")

            # C. Clothing & Accessories
            clothing = character.get("default_clothing", {})
            clothes = [clothing.get("upper"), clothing.get("lower"), clothing.get("footwear"),
                       clothing.get("outerwear")]
            clothes = [c for c in clothes if c]

            if clothes:
                acc = clothing.get("accessories", [])
                acc_str = f", accessorized with {', '.join(acc)}" if acc else ""
                char_sentence.append(f"wearing {', '.join(clothes)}{acc_str}.")

            # D. Action, Pose, Expression and Gaze
            action = character_scene.get("action", "standing")
            pose = character_scene.get("pose", "relaxed")
            expr = character_scene.get("expression", "neutral")
            gaze = character_scene.get("gaze", "forward")

            action_str = f"He is {action} in a {pose} posture, showing a {expr} expression and looking {gaze}."
            char_sentence.append(action_str)

            # Combine character sentences and clean up formatting
            parts.append(" ".join(char_sentence).replace(" ,", ","))

        # ======================================================
        # 5. OBJECTS
        # ======================================================
        for object_id in scene.get("objects", []):
            obj = self.bible["objects"].get(object_id)

            if obj and obj.get("appearance"):
                parts.append(f"Nearby object: {obj['appearance'].strip('.')}.")

        # Join all parts smoothly
        final_prompt = " ".join(part.strip() for part in parts if part)
        final_prompt = final_prompt.replace(".,", ",").replace("..", ".")

        return final_prompt

    def build_scene_prompts(self):
        return [
            self.__build_scene_prompt(scene)
            for scene in self.scenes
        ]

    def __build_thumbnail_prompt(self, thumbnail: dict) -> str:
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

        char_entries = []

        primary = thumbnail.get("primary_character")

        if primary:
            char_entries.append((
                primary,
                composition.get("primary_subject_position"),
                composition.get("primary_subject_depth")
            ))

        for secondary in thumbnail.get("secondary_characters", []):
            char_entries.append((
                secondary,
                composition.get("secondary_subject_position"),
                composition.get("secondary_subject_depth")
            ))

        for character_scene, position, depth in char_entries:
            character = self.bible["characters"][character_scene["id"]]
            char_sentence = []

            # A. Spatial Anchoring (position + depth from composition)
            anchor_parts = [p for p in [position, depth] if p]

            if anchor_parts:
                char_sentence.append(f"Positioned at the {', in the '.join(anchor_parts)} of the frame,")

            # B. Identity Blend
            char_name = character.get("name", "The character")
            char_sentence.append(f"{char_name}, {character['identity_blend']},")

            # C. Clothing (close-up: only visible upper-body items)
            clothing = character.get("default_clothing", {})
            clothes = [clothing.get("upper"), clothing.get("outerwear")]
            clothes = [c for c in clothes if c]

            if clothes:
                char_sentence.append(f"wearing {', '.join(clothes)}.")

            # D. Action, Pose, Expression and Gaze
            action = character_scene.get("action", "standing")
            pose = character_scene.get("pose", "relaxed")
            expr = character_scene.get("expression", "neutral")
            gaze = character_scene.get("gaze", "forward")

            action_str = f"He is {action} in a {pose} posture, with {expr}, looking {gaze}."
            char_sentence.append(action_str)

            # Combine character sentences and clean up formatting
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

        # Join all parts smoothly
        final_prompt = " ".join(part.strip() for part in parts if part)
        final_prompt = final_prompt.replace(".,", ",").replace("..", ".")

        return final_prompt

    def build_thumbnail_prompts(self):
        return [
            self.__build_thumbnail_prompt(thumbnail)
            for thumbnail in self.thumbnails
        ]
