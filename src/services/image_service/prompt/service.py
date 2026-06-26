from src.utils.file_utils import try_read_json
from .constants import DATA_DIR


class PromptService:
    def __init__(self):
        self.bible = try_read_json(DATA_DIR / "project_bible.json")
        self.scenes = try_read_json(DATA_DIR / "scene_metadata.json")["scenes"]

    def build(self, scene: dict) -> str:
        # ======================================================
        # VISUAL STYLE
        # ======================================================
        parts = [self.bible["visual_style"]]

        # ======================================================
        # SCENE
        # ======================================================

        if scene.get("scene_setting"):
            parts.append(f"{scene['scene_setting'].capitalize()}.")

        if scene.get("time_of_day"):
            parts.append(f"{scene['time_of_day'].capitalize()}.")

        if scene.get("weather"):
            parts.append(f"Visible weather: {scene['weather']}.")

        # ======================================================
        # CHARACTERS
        # ======================================================

        characters = sorted(
            scene.get("characters") or [],
            key=lambda c: c["role"] != "primary"
        )

        for character_scene in characters:
            character = self.bible["characters"][character_scene["id"]]

            appearance = character["appearance"]
            clothing = character["default_clothing"]

            sentence = []

            sentence.append(
                f"{character['name']} is a "
                f"{appearance['age']} "
                f"{appearance['gender']}"
            )

            if appearance.get("ethnicity"):
                sentence.append(appearance["ethnicity"])

            if appearance.get("height"):
                sentence.append(appearance["height"])

            if appearance.get("build"):
                sentence.append(appearance["build"])

            visual = []

            if appearance.get("skin"):
                visual.append(f"{appearance['skin']} skin")

            if appearance.get("face_shape"):
                visual.append(f"{appearance['face_shape']} face")

            if appearance.get("eyes"):
                visual.append(appearance["eyes"])

            if appearance.get("hair"):
                visual.append(appearance["hair"])

            if appearance.get("facial_hair"):
                visual.append(appearance["facial_hair"])

            if visual:
                sentence.append("with " + ", ".join(visual))

            if appearance.get("posture"):
                sentence.append(
                    f"and a {appearance['posture']} posture"
                )

            sentence.append(".")

            clothing_parts = [
                clothing.get("upper"),
                clothing.get("lower"),
                clothing.get("footwear"),
            ]

            clothing_parts = [
                item for item in clothing_parts if item
            ]

            if clothing_parts:
                sentence.append(
                    "Wearing " +
                    ", ".join(clothing_parts) +
                    "."
                )

            if clothing.get("outerwear"):
                sentence.append(
                    f"Outerwear: {clothing['outerwear']}."
                )

            accessories = clothing.get("accessories") or []

            if accessories:
                sentence.append(
                    "Accessories: "
                    + ", ".join(accessories)
                    + "."
                )

            sentence.append(
                f"{character['name']} is {character_scene['action']}."
            )

            if character_scene.get("pose"):
                sentence.append(
                    f"Body posture: {character_scene['pose']}."
                )

            if character_scene.get("gaze"):
                sentence.append(
                    f"Gaze: {character_scene['gaze']}."
                )

            if character_scene.get("expression"):
                sentence.append(
                    f"Facial expression: {character_scene['expression']}."
                )

            parts.append(" ".join(sentence))

        # ======================================================
        # OBJECTS
        # ======================================================

        for object_id in scene.get("objects") or []:

            obj = self.bible["objects"][object_id]

            appearance = obj.get("appearance")

            if appearance:
                parts.append(
                    f"Visible object: {appearance}."
                )

        # ======================================================
        # BACKGROUND
        # ======================================================

        if scene.get("background"):
            parts.append(
                f"Background: {scene['background']}."
            )

        # ======================================================
        # LOCATION
        # ======================================================

        location = self.bible["locations"][scene["location"]]

        if location.get("visual_identity"):
            parts.append(location["visual_identity"] + ".")

        background_elements = location.get("background_elements") or []

        if background_elements:
            parts.append(
                "Background elements: "
                + ", ".join(background_elements)
                + "."
            )

        # ======================================================
        # CAMERA
        # ======================================================

        camera = scene.get("camera", {})

        camera_parts = []

        if camera.get("shot_size"):
            camera_parts.append(camera["shot_size"])

        if camera.get("angle"):
            camera_parts.append(camera["angle"])

        if camera.get("focus"):
            camera_parts.append(
                f"focused on {camera['focus']}"
            )

        if camera_parts:
            parts.append(
                "Camera: " +
                ", ".join(camera_parts) +
                "."
            )

        return " ".join(
            part.strip()
            for part in parts
            if part
        )

    def build_all(self):
        return [
            self.build(scene)
            for scene in self.scenes
        ]
