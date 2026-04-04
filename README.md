# video-maker

1. make setup
2. make run

1) SCRIPT PROMPT (Claude Sonnet 4.5):

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

2) IMAGE PROMPT (ChatGPT):

```
You are an expert cinematic storyboard artist and AI prompt engineer.

Your task is to convert a given narration script into scene-by-scene AI image generation prompts for YouTube
storytelling videos.

GOAL:

Create highly emotional, cinematic, visually consistent image prompts
Ensure all images feel like they belong to the same movie
Optimize for AI image generation tools like Google Gemini

STEP 1 — ANALYZE STORY

Break the script into logical visual scenes
Each scene should represent a clear moment, action, or emotion
Aim for 1 scene every 6–10 seconds of narration

STEP 2 — CHARACTER CONSISTENCY (VERY IMPORTANT)

Identify all main characters
Define each character ONCE with consistent attributes:
name (if available)
age
gender
hairstyle
clothing style
overall vibe
Reuse EXACT SAME character description in ALL prompts
Always repeat the exact same character description in every single prompt without changing wording

STEP 3 — ENVIRONMENT CONSISTENCY

Identify main locations (e.g., town, house, garden)
Keep visual style consistent across scenes
Maintain same atmosphere, color palette, and tone
Maintain consistent lighting conditions unless the story explicitly changes time or mood

STEP 4 — VISUAL STYLE (APPLY TO EVERY PROMPT)
cinematic illustration, semi-realistic, emotional storytelling, soft lighting, warm color grading, depth of field,
slightly stylized characters, detailed environment, 2D-3D hybrid, YouTube storytelling style, dramatic light rays, cozy
but cinematic mood, 4k, --ar 16:9

STEP 4.5 — CHANNEL STYLE MODIFIER

CHANNEL STYLE:
Focus on calm, introspective, emotionally grounded storytelling for adults.
Use soft, natural lighting (morning light, golden hour, overcast daylight).
Prefer muted and warm color palettes (earth tones, soft greens, browns, warm neutrals).
Avoid overly vibrant or cartoonish visuals.

Characters should have subtle, realistic facial expressions (thoughtful, quiet, reflective).
Body language should feel natural and minimal (small gestures, stillness, slow movement).

Scenes should feel peaceful, slow-paced, and atmospheric.
Include environmental storytelling (empty spaces, nature, weather, light through windows, silence).

Use cinematic camera styles:

close-ups for emotions
wide shots for loneliness or reflection
over-the-shoulder shots for conversations

Avoid action-heavy or dramatic compositions.
Avoid exaggerated expressions.

Overall mood:
calm, reflective, slightly melancholic but hopeful.
Like a quiet independent film about personal growth.

Always blend the channel style with the base visual style in every prompt.

STEP 5 — OUTPUT FORMAT

Return ALL prompts in ONE continuous block of text.

Format like this:

[full prompt]
[full prompt]
[full prompt]
...

Rules:

Each line must be a COMPLETE image prompt (copy-paste ready)
Include:
character description
action
emotion
environment
cinematic details
DO NOT use code blocks
DO NOT add explanations
DO NOT skip numbers

STEP 6 — CINEMATIC QUALITY RULES

Every scene should:

Show emotion visually (not abstract)
Avoid repetition
Use camera angles when helpful (close-up, wide shot, over-the-shoulder, etc.)
Include small details (lighting, weather, body language)
Feel like a movie frame

STEP 7 — PACING

Faster scenes for action moments
Slower, detailed scenes for emotional moments
Use visual variety (close-up, wide, over-shoulder, etc.)

SCRIPT:
[PASTE YOUR SCRIPT HERE GOT FROM STEP 1]
```