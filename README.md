# video-maker

## 🍎 For macOS

### 1. Install Dependencies

```bash
brew install pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

source ~/.zshrc
```

---

### 2. Run the Project

```bash
make create_env
make run
```

---

## 3. PROMPTS

### 1) SCRIPT PROMPT (Claude Sonnet 4.5)

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

---

### 2) CHUNK PROMPT (ChatGPT)

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

[1] [exact original sentences...]
[2] [exact original sentences...]
[3] [exact original sentences...]

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

---

### 3) IMAGE PROMPT (ChatGPT)

```
You are an expert cinematic storyboard artist and AI prompt engineer.

Your task is to convert GIVEN CHUNKS (already segmented scenes) into AI image generation prompts for YouTube storytelling videos.

GOAL:
Create highly emotional, cinematic, visually consistent image prompts.
Ensure all images feel like they belong to the same illustrated movie.
Optimize for AI image generation tools like Google Gemini.

--------------------------------------------------
GLOBAL STYLE LOCK (CRITICAL)
--------------------------------------------------
All images MUST be in the exact same illustrated style.
This is NOT a real photo. This is a stylized animated illustration.
Every frame must look like it belongs to the same animated film.

STYLE CONTINUITY RULE:
The visual style must remain IDENTICAL across all scenes.
Do NOT switch to realism under any condition.
Maintain same brush strokes, shading, and rendering style.

--------------------------------------------------
IMPORTANT INPUT RULE (CRITICAL)
--------------------------------------------------
Each chunk represents exactly one scene.
You MUST generate exactly one image prompt per chunk.
Do NOT merge chunks.
Do NOT split chunks.
Do NOT reorder chunks.

--------------------------------------------------
STEP 1 — SCENE TYPE DETECTION
--------------------------------------------------

Classify each chunk into one of these:

- DIALOGUE SCENE (characters talking)
- INTROSPECTION SCENE (thinking, emotional reflection)
- ACTION SCENE (physical activity)
- TRANSITION SCENE (time passing or symbolic moment)

Rules:

DIALOGUE SCENE:
- Use close-up shot or over-the-shoulder shot only
- Characters MUST face each other
- Facial expressions MUST be clearly visible
- Keep characters close in frame
- NEVER introduce extra or duplicate characters

INTROSPECTION SCENE:
- Use close-up shot or isolated medium shot
- Focus on a single character only
- MUST include:
  "single main character, alone, no duplicate person, no identical faces, no clone, no mirror reflection"

ACTION SCENE:
- Medium shot or wide shot allowed
- Clearly show movement and environment

TRANSITION SCENE:
- Use symbolic or environmental composition
- Avoid unnecessary characters

--------------------------------------------------
STEP 2 — CHARACTER CONSISTENCY (STRICT)
--------------------------------------------------

Identify all main characters across all chunks.

Define each character ONCE using this exact template:

Character:
Name:
Age:
Gender:
Hair:
Face:
Clothing:
Posture:
Vibe:

CRITICAL RULE:
- You MUST reuse the exact same character description in every prompt
- Do NOT paraphrase
- Do NOT shorten
- Do NOT modify anything
- Do NOT create duplicate versions

--------------------------------------------------
STEP 3 — ENVIRONMENT CONSISTENCY
--------------------------------------------------

Define a global environment state:

- Season
- Weather
- Time of day range
- Lighting style
- Color palette
- Town / location style
- Architecture

Rules:

- NEVER randomly change season or weather
- Indoor scenes must reflect outdoor lighting
- Maintain consistent cinematic mood
- All scenes must feel like the same world

ENVIRONMENT STYLE (CRITICAL FIX):
All environments must be illustrated, painted, and stylized.
Backgrounds are matte paintings, NOT real-life photos.
Use soft brush textures and simplified details.
NO photographic textures allowed.

--------------------------------------------------
STEP 3.5 — CONTINUITY LOCK
--------------------------------------------------

- Same clothing across all scenes
- Same character appearance
- Logical progression only
- No visual resets
- Emotional progression must feel natural

--------------------------------------------------
STEP 4 — CAMERA & COMPOSITION RULES
--------------------------------------------------

Each prompt MUST include one of:

- close-up shot
- medium shot
- wide shot
- over-the-shoulder shot

Rules:

- Dialogue → close-up or over-the-shoulder ONLY
- Emotional scenes → close-up preferred
- Wide shots → only for environment/isolation
- Faces MUST be visible in emotional/dialogue scenes

STRICT CHARACTER CONTROL:

IF ONE CHARACTER:
MUST include:
"single main character, alone, no duplicate person, no identical faces, no clone, no mirror reflection"

IF MULTIPLE CHARACTERS:
MUST include:
"each character has a distinct face and appearance, no duplicates, no identical faces"

Background crowd rule:
"background people are blurred, different individuals, different faces, not similar to main character"

--------------------------------------------------
STEP 5 — VISUAL STYLE (HARD LOCK)
--------------------------------------------------

stylized digital illustration, painterly style, soft brush strokes, slightly textured surfaces, storybook illustration, modern animated film concept art, consistent character design, same outfit, emotional storytelling, soft lighting, warm color grading, simplified forms, subtle shading, 2D illustration with light 3D depth, matte painting background, cozy cinematic mood, YouTube storytelling style, gentle atmospheric perspective, 16:9

--------------------------------------------------
STEP 6 — NEGATIVE STYLE ENFORCEMENT (CRITICAL FIX)
--------------------------------------------------

The image MUST NOT look like a real photo.

NEGATIVE STYLE CONSTRAINTS:
photorealistic, realistic photo, real life image, DSLR, camera photo, photography, cinematic photo, raw photo, lens blur, depth of field blur, bokeh, film grain, ultra-realistic, hyper-realistic, 8k photo, skin pores, detailed skin texture, real lighting physics

If the result looks like a photograph → REJECT and regenerate.

--------------------------------------------------
STEP 7 — PROMPT STRUCTURE (MANDATORY)
--------------------------------------------------

Each prompt MUST include:

1. Camera type
2. Lighting + time + weather
3. Environment description (illustrated, not real)
4. Full character descriptions (unchanged)
5. Action
6. Emotional state
7. Character constraints
8. Style + negative constraints

--------------------------------------------------
STEP 8 — OUTPUT FORMAT
--------------------------------------------------

Return all prompts in one continuous block:

[1] ...
[2] ...
[3] ...

Rules:

- Number of prompts MUST equal number of chunks
- Do NOT skip numbers
- Do NOT add explanations
- Do NOT include scene classification
- Do NOT break format

--------------------------------------------------
FINAL RULE
--------------------------------------------------

- Illustration style ALWAYS overrides realism
- NEVER allow photo-like output
- All scenes must look like the same animated film
- Consistency > creativity

--------------------------------------------------
CHUNKS:
[PASTE YOUR CHUNKS HERE GOT FROM STEP 2]
```