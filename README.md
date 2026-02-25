# video-maker

1. make setup
2. make run

Script Prompt:
```
You are a storyteller writing a calm, comforting life-lesson story for adults.

The story is written in English.

It is designed to be read aloud slowly as a YouTube voice-over.

Use simple, clear, modern English.

Use short paragraphs.

Use mostly short sentences.

The tone is gentle, calm, and reassuring.

This story is allowed to teach a clear life lesson directly.

The lesson should feel warm and human, not preachy.

STORY STYLE:

– Traditional storytelling tone
– Easy to follow when heard once
– Calm and reflective
– No complex vocabulary
– No poetic language
– No symbolism or hidden meaning

STORY ELEMENTS:

– One named young adult main character
– One wise older character (elder, teacher, guide)
– A quiet village or nature setting
– A journey or visit
– One simple task given by the wise character
– The task clearly demonstrates the lesson

STRUCTURE (FOLLOW THIS ORDER):

Introduce the main character and their inner struggle.

Show how this struggle affects daily life.

Introduce the wise character and their background.

The main character asks for help.

The wise character gives a simple task.

Describe the task step by step.

The wise character explains the meaning of the task clearly.

The main character understands and changes.

End calmly with peace and closure.

Do not rush the story.

Write like a calm narrator speaking gently to the listener.

Write only the story script.
```

Image Consistency Prompt:
```
Now analyze the story you just wrote.
Your task is to generate structured visual metadata for AI image generation.
The goal is to create consistent, cinematic, high-quality images based on the story.
IMPORTANT RULES:
– Output ONLY valid JSON.
– Do NOT include explanations.
– Do NOT include markdown.
– Do NOT include any text outside the JSON.
– Ensure character consistency across all scenes.
– Keep all visual descriptions realistic (no fantasy elements).
– Maintain a calm, cinematic, natural atmosphere.
--------------------------------------
REQUIREMENTS:
1) CHARACTERS
Extract all named characters.
For each character, generate:
- name
- age
- gender
- physical appearance (detailed and consistent)
- clothing style (consistent across scenes unless story changes it)
- overall vibe (calm, thoughtful, kind, etc.)
- a single master_visual_prompt (a portrait-style cinematic reference description)
The physical description must remain consistent across all scenes.
--------------------------------------
2) ENVIRONMENT
Generate a single consistent environment description including:
- location type
- country or cultural setting (if implied)
- season
- weather style
- architecture style
- natural elements
- overall cinematic atmosphere
This environment must remain visually consistent across scenes unless the story clearly changes it.
--------------------------------------
3) VISUAL_STYLE
Generate a global visual style including:
- photography style (e.g., cinematic film still)
- camera lens type (e.g., 35mm, 50mm)
- lighting style
- color grading
- realism level
- rendering quality keywords
This style must apply to every image.
--------------------------------------
4) SCENE BREAKDOWN
Create EXACTLY 12 scenes.
Each scene must include:
- scene_number
- short_title
- visual_description (clear, purely visual, no internal thoughts)
- main_characters_in_scene (list of character names)
- camera_shot_type (wide shot, medium shot, close-up, etc.)
- camera_angle (eye-level, slightly low angle, etc.)
- time_of_day
- emotional_tone (visual, not abstract)
- key_objects (important physical objects visible in the scene)
Scenes must:
– Follow the story structure in order.
– Be visually distinct.
– Be realistic and physically drawable.
– Avoid abstract concepts.
– Avoid symbolic visuals.
– Avoid narration text.
--------------------------------------
5) OUTPUT FORMAT
Return ONLY this JSON structure:
{
  "characters": [...],
  "environment": {...},
  "visual_style": {...},
  "scenes": [...]
}
```