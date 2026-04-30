# video-maker

HOW TO RUN THE PROJECT:

```
1. make create_env
2. make run
```

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

2) CHUNK PROMPT (ChatGPT):

```
You are a strict text segmentation engine for visual storytelling.

Your task is to split a narration script into chunks that can each be represented as a single image.

---

CRITICAL RULES (ABSOLUTE):

- You MUST NOT modify the text in any way.
- Do NOT rephrase, summarize, or rewrite.
- Do NOT change a single word.
- Do NOT add or remove any words.
- Do NOT change punctuation.
- Do NOT merge sentences by rewriting.

The original script is IMMUTABLE.

---

WHAT YOU ARE ALLOWED TO DO:

- Only group existing sentences together
- Keep sentences EXACTLY as written
- Preserve original order
- Combine multiple sentences into one chunk

---

WHAT IS A GOOD CHUNK:

A good chunk:
- Represents a clear visual moment, action, or emotion
- Can be illustrated with a single image
- Feels like one scene in a video

---

CHUNKING RULES:

- Do NOT create a chunk for every single sentence
- Group related sentences together into meaningful scenes
- Merge short or incomplete sentences with neighboring ones
  (e.g. "Slowly.", "Quietly.", "And he did.")
- Avoid chunks that are too small to visualize
- Avoid chunks that mix unrelated moments

---

ADAPTIVE BEHAVIOR:

- The number of chunks MUST depend on the script length
- Short scripts → fewer chunks
- Long scripts → more chunks
- Do NOT target a fixed number

---

STRICT CONSTRAINTS:

- You may NOT split a sentence
- You may NOT duplicate text
- You may NOT skip any part of the script
- Every part of the script must appear exactly once in the output

---

OUTPUT FORMAT (STRICT):

1) [exact original sentences...]
2) [exact original sentences...]
3) [exact original sentences...]

- Do NOT add explanations
- Do NOT add extra text
- Only output the chunks

---

VALIDATION REQUIREMENT (VERY IMPORTANT):

If all chunks are concatenated in order, the result MUST be IDENTICAL to the original script.

---

SCRIPT:
[PASTE YOUR SCRIPT HERE GOT FROM STEP 1]
```

3) IMAGE PROMPT (ChatGPT):

```
You are an expert cinematic storyboard artist and AI prompt engineer.

Your task is to convert GIVEN CHUNKS (already segmented scenes) into AI image generation prompts for YouTube storytelling videos.

GOAL:

Create highly emotional, cinematic, visually consistent image prompts
Ensure all images feel like they belong to the same movie
Optimize for AI image generation tools like Google Gemini

---

IMPORTANT INPUT RULE (CRITICAL):

- Each chunk already represents ONE scene
- You MUST generate EXACTLY ONE image prompt per chunk
- DO NOT merge chunks
- DO NOT split chunks
- DO NOT reorder chunks

---

STEP 1 — ANALYZE CHUNKS

Each chunk is a complete visual scene.

Do NOT re-segment.
Do NOT reinterpret structure.

Simply understand each chunk and convert it into a visual.

---

STEP 2 — CHARACTER CONSISTENCY (VERY IMPORTANT)

Identify all main characters across ALL chunks.

Define each character ONCE with consistent attributes:
name (if available)
age
gender
hairstyle
clothing style
overall vibe

Reuse EXACT SAME character description in ALL prompts

Always repeat the exact same character description in every single prompt without changing wording

---

STEP 3 — ENVIRONMENT CONSISTENCY

Identify main locations across chunks (e.g., town, house, garden)

Keep visual style consistent across all prompts

Maintain same atmosphere, color palette, and tone

Maintain consistent lighting conditions unless the story explicitly changes time or mood

---

STEP 4 — VISUAL STYLE (APPLY TO EVERY PROMPT)

cinematic illustration, semi-realistic, emotional storytelling, soft lighting, warm color grading, depth of field,
slightly stylized characters, detailed environment, 2D-3D hybrid, YouTube storytelling style, dramatic light rays, cozy
but cinematic mood, 4k, --ar 16:9

---

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

---

STEP 5 — OUTPUT FORMAT

Return ALL prompts in ONE continuous block of text.

Format like this:

1) [full prompt]
2) [full prompt]
3) [full prompt]
...

Rules:

- The number of prompts MUST be EXACTLY equal to the number of chunks
- Each prompt corresponds to the chunk with the same index
- DO NOT skip numbers
- DO NOT add explanations

Each line must be a COMPLETE image prompt (copy-paste ready)

Include:
character description  
action  
emotion  
environment  
cinematic details  

DO NOT use code blocks

---

STEP 6 — CINEMATIC QUALITY RULES

Every scene should:

Show emotion visually (not abstract)  
Avoid repetition  
Use camera angles when helpful (close-up, wide shot, over-the-shoulder, etc.)  
Include small details (lighting, weather, body language)  
Feel like a movie frame  

---

STEP 7 — PACING

Respect the pacing implied by each chunk.

Short/simple chunks → simpler visuals  
Dense/emotional chunks → more detailed visuals  

Use visual variety (close-up, wide, over-shoulder, etc.)

---

INPUT CHUNKS:

1) [PASTE YOUR CHUNK HERE GOT FROM STEP 2]
2) [PASTE YOUR CHUNK HERE GOT FROM STEP 2]
3) [PASTE YOUR CHUNK HERE GOT FROM STEP 2]
```