from src.utils.file_utils import try_read_json
from .constants import DATA_DIR


class PromptService:
    def __init__(self):
        self.bible = try_read_json(DATA_DIR / "project_bible.json")
        self.scenes = try_read_json(DATA_DIR / "scene_metadata.json").get("scenes", [])

    def __build_scene(self, scene: dict) -> str:
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

    def build_scenes(self):
        return [
            self.__build_scene(scene)
            for scene in self.scenes
        ]
