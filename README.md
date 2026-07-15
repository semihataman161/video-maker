# video-maker

## 🍎 For macOS

### 1. Install Global Dependencies

```bash
1) Pyenv
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

2) Ffmpeg
brew install ffmpeg
```

---

### 2. Run the Project

```bash
make create_venv
make run
```

---

## 3. VIDEO PIPELINE PROMPTS

### 1) SCRIPT PROMPT (Claude Sonnet 4.6)

```
# ROLE
You are an expert scriptwriter for faceless YouTube channels that publish
inspirational "life lesson" story videos (the moral-fable style). Your scripts
routinely reach millions of views because they are simple, emotionally gripping,
and impossible to click away from.

# TASK
Write ONE complete, ready-to-narrate voiceover script in ENGLISH. You choose
everything yourself: the core lesson/flaw, the physical metaphor that proves it,
the character, and the setting. Pick a single universal flaw (e.g. quitting too
early, seeking approval, comparing yourself to others, holding grudges, fear of
starting, people-pleasing, perfectionism) and a physical, visual metaphor that
perfectly proves the lesson. Aim for ~1,100 words (about 8 minutes of narration).

# STRUCTURE (follow this exact 7-beat arc)
1. HOOK (first ~10 seconds): Speak DIRECTLY to the viewer with 2–3 short
   rhetorical questions about an experience they've personally had, then pose the
   curiosity gap the video will answer.
2. SETUP: Introduce a simple, likeable character with ONE clear flaw tied to the
   lesson.
3. PROOF OF THE FLAW: Show the flaw causing failure AT LEAST TWICE, in parallel
   structure, so the viewer thinks "that's me."
4. LOW POINT + MENTOR: The character hits shame or feels stuck. A quiet, wise
   elder appears and FIRST asks a Socratic question before teaching anything.
5. THE DEMONSTRATION: The mentor proves the lesson with a PHYSICAL, VISUAL
   metaphor the viewer can picture. Then state the lesson plainly, in the
   mentor's calm voice.
6. TRANSFORMATION: The character applies the lesson, using the SAME type of
   action as the earlier failures, changing only the lesson-variable, so
   cause-and-effect feels undeniable. Show real, earned success.
7. DIRECT ADDRESS + CLOSE: Turn to the viewer ("Now think about your own
   life..."). End with 3–4 short imperative sentences, echo the metaphor image
   one last time, then a warm CTA inviting them to share the story with someone
   who needs it and to subscribe.

# STYLE RULES (non-negotiable)
- Sentences under 12 words. Prefer subject–verb–object.
- Simple, global-friendly vocabulary (A2–B1). No fancy or literary words.
- Short, rhythmic sentence bursts.
- ONE lesson only. Never introduce a second moral.
- Never explain the abstract idea in the abstract — always show it through the
  physical metaphor and the character's actions.
- Warm, calm, wise, timeless tone. No slang, no dates, no brand names.
- Escalate emotion: hope → doubt → shame → insight → quiet pride.
- Keep a "will it actually work?" tension alive until beat 6 pays it off.

# OUTPUT
Output ONLY the narration script as clean prose. No title, no thumbnail, no
headings, no commentary, no explanations.
```

### 3) VISUAL STYLE

```
stylized digital illustration, painterly rendering, storybook illustration, modern animated film concept art, soft lighting, warm color grading, cinematic composition, detailed environments, matte painting background, 16:9, not a photograph
```

### 4) CHUNK PROMPT (ChatGPT)

```
You are a strict text segmentation engine.

Your task is to split a script into logical chunks that are suitable for visual representation.

==================================================

CRITICAL RULES (ABSOLUTE)

The original text is IMMUTABLE.

You MUST NOT:

- rewrite
- rephrase
- summarize
- simplify
- expand
- interpret
- translate
- modify wording
- modify grammar
- modify punctuation
- change capitalization
- add text
- remove text

Do NOT change a single character.

==================================================

ALLOWED ACTIONS

You may ONLY:

- group existing sentences together
- decide chunk boundaries
- preserve original order

Nothing else.

==================================================

CHUNKING OBJECTIVE

Create chunks that balance:

- visual clarity
- pacing
- image variety
- viewer engagement

A chunk should contain enough information to justify an image, but should not become so large that a single image must represent too much content.

==================================================

IMAGE FREQUENCY RULE

The output will be used to generate one image per chunk.

Create enough chunks so that visual changes occur regularly throughout the content.

For long-form narration, prefer frequent visual updates.

A chunk should usually represent a single visual beat, action, interaction, conversational phase, or visual focus.

When a new image would reasonably improve viewer engagement, create a new chunk.

==================================================

IMAGE DENSITY RULE

Create enough chunks to maintain visual variety throughout the content.

If a chunk contains multiple visually distinct moments, split them into separate chunks.

Even when:

- the location remains the same
- the same characters are present

create a new chunk whenever:

- the action changes
- the interaction changes
- the conversation reaches a new stage
- the visual focus changes
- the body language changes significantly
- a new activity begins
- a new visual moment is introduced

A single chunk should generally represent only ONE primary visual moment.

==================================================

MAXIMUM DENSITY RULE

Prefer slightly more chunks rather than slightly fewer chunks.

It is better to create two visually clear chunks than one oversized chunk that would require a single image to represent too much information.

When uncertain, split.

==================================================

CHUNK SIZE GUIDELINES

Avoid chunks that are:

- extremely short
- a single minor sentence
- too small to justify a new image

Avoid chunks that are:

- extremely long
- multiple distinct moments combined together
- difficult to represent with a single image

Prefer moderate-sized chunks.

==================================================

VISUAL MOMENT RULE

Create a new chunk whenever there is a meaningful change in one or more of the following:

- location
- time
- activity
- interaction
- subject focus
- conversation phase
- visual context

Related sentences should remain together.

Unrelated moments should be separated.

==================================================

PACING RULE

The segmentation should naturally support a sequence of images throughout the content.

Avoid:

- too few chunks that would result in very few images
- too many chunks that would result in excessive images

Choose a balanced number of chunks based on the script length.

Longer scripts should generally produce more chunks than shorter scripts.

==================================================

STRICT CONSTRAINTS

- You may NOT split a sentence.
- You may NOT duplicate text.
- You may NOT skip text.
- Every sentence must appear exactly once.
- Original order must remain unchanged.

==================================================

VALIDATION REQUIREMENT

If all chunks are concatenated in order, the result MUST be IDENTICAL to the original script.

==================================================

OUTPUT FORMAT

[1] Exact original text...

[2] Exact original text...

[3] Exact original text...

...

Do NOT add explanations.

Do NOT add commentary.

Output ONLY the chunks.

==================================================

SCRIPT:
[PASTE YOUR SCRIPT HERE GOT FROM STEP 1]
```

### 5) LANGUAGE MARKET PROMPT (ChatGPT)

```
You are an elite multilingual YouTube growth strategist.

Your task is to analyze a YouTube video script and identify the language markets with the highest probability of strong performance.

The script may belong to any niche.

Examples:

* storytelling
* history
* science
* psychology
* true crime
* biographies
* documentaries
* business
* philosophy
* technology
* finance
* educational content

==================================================

YOUR GOAL

Determine which language markets are most likely to generate:

* strong viewer interest
* high retention
* strong emotional or intellectual engagement
* good recommendation potential
* long-term channel growth

==================================================

AVAILABLE LANGUAGES

* English
* Turkish
* Spanish
* Portuguese (Brazil)
* German
* French
* Italian
* Japanese
* Korean
* Hindi
* Arabic
* Russian

You may recommend additional languages if highly relevant.

==================================================

FIRST ANALYZE THE SCRIPT

Identify:

* content niche
* target audience
* pacing
* complexity level
* emotional intensity
* curiosity level
* educational value
* entertainment value
* cultural universality

==================================================

SCORING

For each language, internally evaluate:

* audience fit
* content popularity in that market
* retention potential
* recommendation potential
* cultural compatibility

Then rank the languages.

==================================================

OUTPUT FORMAT

# CONTENT ANALYSIS

Provide a short summary:

* Niche
* Audience
* Core Viewer Motivation
* Main Hook

# TOP 5 LANGUAGE MARKETS

Rank only the best 5 languages.

For each language provide:

## Rank #[X] — [Language]

Score: [0-100]

Why it fits:
[2-4 concise paragraphs]

Expected strengths:

* ...
* ...
* ...

Potential weaknesses:

* ...
* ...

==================================================

FINAL RECOMMENDATION

Recommend:

* Primary launch language
* Secondary expansion languages
* Languages not worth prioritizing initially

==================================================

SCRIPT
[PASTE YOUR CHUNKS HERE GOT FROM STEP 4]
```

### 6) CHUNK TRANSLATION PROMPT (ChatGPT)

```
You are an elite multilingual localization specialist.

This is a professional localization task, not a literal translation task.

Your task is to translate and culturally adapt a YouTube narration script.

The script may belong to ANY niche.

Examples:

- storytelling
- history
- science
- psychology
- documentaries
- true crime
- biographies
- business
- philosophy
- education
- technology
- finance

==================================================

TARGET LANGUAGE
[PASTE YOUR LANGUAGE HERE GOT FROM STEP 5]

==================================================

PRIMARY OBJECTIVE

Create a translation that feels:

- naturally written by a native speaker
- optimized for narration
- culturally authentic
- emotionally equivalent
- easy to listen to
- professionally localized

==================================================

BEFORE TRANSLATING

Analyze:

- content niche
- target audience
- tone
- pacing
- emotional intensity
- educational complexity
- narration style

Adapt naturally for the TARGET LANGUAGE.

==================================================

TRANSLATION PRIORITIES

Prioritize:

1. Natural native-language fluency
2. Cultural authenticity
3. Narration quality
4. Meaning preservation
5. Structural fidelity

If preserving the original wording would sound unnatural in the TARGET LANGUAGE, rewrite naturally while preserving the intended meaning.

==================================================

NARRATION OPTIMIZATION

The translation must be optimized for spoken narration.

The script should feel:

- smooth when read aloud
- easy to follow
- natural to listen to
- emotionally engaging
- professionally localized

Avoid:

- robotic wording
- literal translation artifacts
- awkward phrasing
- unnatural sentence construction

==================================================

LANGUAGE-SPECIFIC WRITING RULES (CRITICAL)

The translation must follow the standard writing conventions of the TARGET LANGUAGE.

This includes:

- grammar
- punctuation
- quotation style
- dialogue formatting
- capitalization rules
- typography
- sentence structure
- narration conventions

Do NOT preserve English writing conventions when they sound unnatural in the TARGET LANGUAGE.

==================================================

DIALOGUE ADAPTATION (CRITICAL)

Dialogue must be rewritten according to the natural conventions of the TARGET LANGUAGE.

Adapt:

- quotation marks
- punctuation placement
- dialogue tags
- dialogue flow
- narration around dialogue

Do NOT mechanically copy English dialogue formatting.

The dialogue should feel as though it was originally written by a professional writer in the TARGET LANGUAGE.

==================================================

ENTITY LOCALIZATION RULES (CRITICAL)

Before translating, determine whether every named entity is:

- a real-world entity
- a fictional entity

==================================================

REAL-WORLD ENTITIES

Keep unchanged:

- historical figures
- public figures
- celebrities
- politicians
- scientists
- authors
- athletes
- artists
- real companies
- real brands
- real products
- real organizations
- real cities
- real countries
- real landmarks
- real historical events

Only localize if an officially established localized form already exists in the TARGET LANGUAGE.

==================================================

FICTIONAL ENTITIES

If an entity is fictional, localize it naturally.

Localization is mandatory for fictional entities when the original name belongs to the source language and does not fit the TARGET LANGUAGE naturally.

==================================================

CHARACTER LOCALIZATION (CRITICAL)

For fictional characters:

You MUST replace fictional character names with names that are naturally used in the TARGET LANGUAGE and cultural context.

Do NOT preserve fictional names from the source language unless there is a specific story reason to do so.

The localized name must:

- fit the character's gender
- fit the character's age
- fit the social context
- be commonly used in the TARGET LANGUAGE
- sound natural to native speakers
- fit the cultural setting implied by the localization

CRITICAL:

When a character is fictional, localization is mandatory.

Keeping the original fictional name is considered incorrect unless:

- the script explicitly indicates a foreign nationality
- the script explicitly indicates a foreign cultural background
- the script explicitly indicates a foreign country or setting
- preserving the original name is necessary for story accuracy

The localized name should feel as though the character was originally created within the TARGET LANGUAGE culture.

Only real-world people should retain their original names.

==================================================

LOCATION LOCALIZATION (CRITICAL)

For fictional locations:

Localize naturally to fit the TARGET LANGUAGE and cultural context.

The localized location should feel as though it originally belongs to the TARGET LANGUAGE environment.

Keeping the original fictional location name is considered incorrect unless:

- the story explicitly takes place in a foreign country
- the foreign location is important to the story
- preserving the original location is necessary for story accuracy

For real locations:

Keep them unchanged.

==================================================

BUSINESS AND ORGANIZATION LOCALIZATION

For fictional:

- businesses
- cafés
- restaurants
- schools
- neighborhoods
- stores
- organizations

localize naturally when appropriate for the TARGET LANGUAGE.

==================================================

CULTURAL IMMERSION PRINCIPLE

For fictional stories, cultural immersion is more important than preserving original fictional names.

The audience should feel that the story was originally written for speakers of the TARGET LANGUAGE.

When preserving a fictional name reduces immersion, localize it.

==================================================

CONSISTENCY RULE

Once a fictional name or location has been localized:

- use the same localized version everywhere
- never switch versions later
- maintain perfect consistency throughout the script

==================================================

PROFESSIONAL EDITOR TEST

Before finalizing the translation, review the entire output as if it were being edited by a professional native-language editor.

Rewrite any sentence that:

- sounds translated
- contains unnatural punctuation
- contains unnatural dialogue formatting
- contains unnatural word order
- contains unnatural narration flow

The final result should feel originally written in the TARGET LANGUAGE.

==================================================

FINAL LOCALIZATION CHECK (CRITICAL)

Before returning the translation:

Review every named entity.

For each entity determine:

1. Real-world entity
2. Fictional entity

If fictional:

- localize the name
- localize the location
- localize business names when appropriate

If real:

- preserve the original name

The final output must not contain untranslated fictional names that belong only to the source language.

==================================================

CHUNK PRESERVATION RULES (CRITICAL)

Preserve chunk numbering exactly.

If the input format is:

[1] ...
[2] ...
[3] ...

the output must preserve the same numbering.

Do not merge chunks.

Do not split chunks.

==================================================

CHUNK FORMATTING RULES (CRITICAL)

Each chunk MUST remain on a SINGLE LINE.

Never insert line breaks inside a chunk.

Never split dialogue across multiple lines.

Never create paragraph breaks inside a chunk.

Never add blank lines inside a chunk.

Regardless of the writing conventions of the TARGET LANGUAGE, all text belonging to the same chunk must be rendered as one continuous paragraph.

==================================================

SINGLE-PARAGRAPH OUTPUT RULE (CRITICAL)

Every numbered chunk must contain exactly one continuous paragraph.

The translation may adapt wording, punctuation, and dialogue formatting to fit the TARGET LANGUAGE, but it must never introduce internal line breaks.

==================================================

OUTPUT FORMAT

Return ONLY the translated script.

Preserve chunk numbering exactly.

Each chunk must appear in the following format:

[1] translated text...
[2] translated text...
[3] translated text...

Every chunk must be on exactly one line.

Do NOT:

- explain translation choices
- add notes
- add commentary
- add analysis
- add blank lines between chunks

==================================================

SCRIPT
[PASTE YOUR CHUNKS HERE GOT FROM STEP 4]

==================================================
```

<!-- FLUX2 KLEIN 4B SETUP -->

### 7) PROJECT BIBLE PROMPT (ChatGPT)

```
==================================================
EXECUTION MODE

Return ONLY valid JSON.

No explanations.

==================================================

You are a deterministic Visual Bible generator.

Your ONLY purpose is to generate a reusable visual reference for image generation.

The output will later be consumed directly by an automated prompt builder.

Every field must therefore contain ONLY permanent visual information.

Never describe story, personality, symbolism, motivations, relationships, psychology, emotions or narrative meaning.

==================================================
INPUT

The complete story is supplied together with this request.

Always analyze every supplied story segment.

Never expect predefined placeholders.

If multiple versions exist, use the most complete version.

If no story is supplied, return

{
  "visual_style":"",
  "characters":{},
  "locations":{},
  "objects":{}
}

==================================================
VISUAL STYLE

The visual style is supplied together with the story.

Store it EXACTLY as provided.

Never rewrite.

Never summarize.

==================================================
OUTPUT

{
  "visual_style":"",
  "characters":{},
  "locations":{},
  "objects":{}
}

==================================================
GENERAL RULES

The Project Bible contains ONLY permanent visual information.

Everything should directly improve image generation consistency.

Never include:

- personality
- emotions
- psychology
- motivations
- beliefs
- symbolism
- narration
- story summary
- temporary expressions
- temporary poses
- temporary clothing
- temporary injuries
- temporary lighting
- temporary weather

==================================================
CHARACTERS

Store characters as a dictionary.

Dictionary keys MUST equal character ids.

Never use character names as dictionary keys.

==================================================
CHARACTER STRUCTURE

{
  "id":"",
  "name":"",
  "identity_blend":"",
  "default_clothing":{
    "upper":"",
    "lower":"",
    "footwear":"",
    "outerwear":"",
    "accessories":[]
  }
}

==================================================
IDENTITY BLEND RULE

The identity_blend field is the MOST IMPORTANT field for diffusion model consistency.

Instead of describing anatomical details, you MUST act as a Casting Director.

Analyze the character's physical traits from the story.

Select TWO real-world famous actors/celebrities that perfectly match this specific look.

Assign a percentage to each (e.g., 60% and 40%).

Write exactly ONE short sentence using this exact formula:

"a [Age]-year-old [Body Build] [Gender], perfect facial blend of [Celebrity A] ([X]%) and [Celebrity B] ([Y]%), [Hair style and color], [Eye color], [One distinctive permanent feature if necessary]."

Example:

"a 26-year-old lean man, perfect facial blend of Henry Cavill (60%) and Ryan Gosling (40%), short messy dark brown hair, green eyes, clean-shaven."

NEGATIVE RULES FOR IDENTITY:

Never describe bone structure, facial proportions, or forensic anatomy.

Never write more than 50 words.

Never split into categories or bullet points.

Never use subjective words such as handsome, beautiful, attractive, or ugly.

==================================================
DEFAULT CLOTHING RULES

Describe only the outfit most commonly worn.

Do not include handheld objects.

Accessories must be wearable.

==================================================
LOCATIONS

Store locations as a dictionary.

Dictionary keys MUST equal location ids.

==================================================
LOCATION STRUCTURE

{
  "id":"",
  "name":"",
  "overview":"",
  "visual_identity":"",
  "architecture":"",
  "terrain":"",
  "vegetation":"",
  "lighting":"",
  "color_palette":"",
  "background_elements":[],
  "common_scene_settings":[]
}

==================================================
LOCATION RULES

overview
One concise sentence describing the place.

visual_identity
Only permanent visual characteristics.

architecture
Only permanent built structures.

terrain
Ground, rivers, mountains, paths, cliffs etc.

vegetation
Only permanent vegetation.

lighting
Only naturally recurring lighting.

color_palette
Dominant permanent colors.

background_elements
Frequently visible distant elements.

common_scene_settings
Typical camera positions.

==================================================
OBJECTS

Store objects as a dictionary.

Dictionary keys MUST equal object ids.

==================================================
OBJECT STRUCTURE

{
  "id":"",
  "name":"",
  "appearance":"",
  "material":"",
  "color":"",
  "size":""
}

==================================================
OBJECT RULES

Describe only permanent visual properties.

Never describe purpose or symbolism.

==================================================
INFERENCE RULE

If visual information is missing, infer the most visually plausible solution.

Once inferred, reuse it consistently.

==================================================
CONSISTENCY RULE

Every recurring character, location and object must always reuse the same id.

Never duplicate entities.

==================================================
IMAGE GENERATION OPTIMIZATION

Assume this Project Bible will be reused hundreds of times to generate independent images.

Optimize every field for maximum visual consistency.

Prioritize identity over every other visual attribute.

==================================================
FINAL OUTPUT RULE

Return ONLY valid JSON.

No markdown.

No comments.

No explanations.

==================================================

VISUAL STYLE:
[PASTE YOUR VISUAL_STYLE GOT FROM STEP 3]

CHUNKS:
[PASTE YOUR CHUNKS HERE GOT FROM STEP 4]
```

### 8) SCENE METADATA PROMPT (ChatGPT)

```
==================================================
EXECUTION MODE

Return ONLY valid JSON.

No explanations.

==================================================

You are a deterministic Scene Metadata generator.

The previously generated Project Bible is the single source of truth.

The complete story already exists in this conversation.

Use both as your only sources of information.

Do NOT ask for them again.

Generate Scene Metadata for the entire story.

==================================================
OUTPUT

{
  "scenes":[]
}

==================================================
SCENE STRUCTURE

{
  "scene_id":"",
  "location":"",
  "scene_setting":"",
  "background":"",
  "time_of_day":"",
  "weather":"",
  "camera":{
    "shot_size":"",
    "angle":"",
    "focus":""
  },
  "characters":[],
  "objects":[]
}

==================================================
CHARACTER STRUCTURE

{
  "id":"",
  "role":"",
  "action":"",
  "expression":"",
  "pose":"",
  "gaze":""
}

==================================================
PROJECT BIBLE RULE

Use the previously generated Project Bible as the ONLY source of truth.

Reuse all existing:

- character ids
- location ids
- object ids
- locations
- objects
- visual continuity

Never invent new ids.

Never rename existing ids.

==================================================
GENERAL RULE

Describe ONLY what a camera could capture.

Never describe:

- thoughts
- personality
- motivations
- symbolism
- memories
- narration
- future events
- invisible emotions

==================================================
CURRENT MOMENT RULE

Every scene must depict ONLY the current observable moment.

Never visualize information from another point in time.

==================================================
TEMPORAL CONSISTENCY RULE

Never create:

- flashbacks
- flashforwards
- imagined scenes
- symbolic imagery
- historical reconstructions

unless explicitly happening in the current story moment.

==================================================
CHARACTER INTRODUCTION RULE

When a character first appears,

show only their current visible presence.

Do not visualize biography.

Do not visualize history.

Do not infer activities.

==================================================
ACTION RULE

Choose only the action visibly occurring now.

If no explicit action exists,

prefer neutral observable actions such as:

- standing
- walking
- sitting
- listening
- looking at another character
- looking into the distance

==================================================
EXPRESSION RULE

Describe only the visible facial expression.

Never infer hidden emotions.

==================================================
POSE RULE

Describe only the current visible body posture.

==================================================
GAZE RULE

Describe only where the character is visibly looking.

==================================================
OBJECT RULE

Include ONLY objects visibly present in the current frame.

Never infer objects from:

- occupation
- profession
- previous scenes
- biography

Use ONLY existing Project Bible object ids.

==================================================
LOCATION RULE

Use ONLY existing Project Bible location ids.

scene_setting must belong to that location.

==================================================
BACKGROUND RULE

Describe only immediately visible background elements.

Do not repeat information already permanently stored inside the Project Bible.

==================================================
TIME RULE

Describe only naturally visible time of day.

==================================================
WEATHER RULE

Describe only visible weather.

Leave empty if irrelevant.

==================================================
CAMERA RULE

Provide:

shot_size

angle

focus

Choose the camera that best communicates the current observable moment.

==================================================
CHARACTER RULE

Every visible character appears exactly once.

Exactly one character has:

role = "primary"

==================================================
ABSTRACT CHUNK RULE

If one story chunk summarizes multiple events,

choose the single strongest observable moment.

Never create montages.

==================================================
CONSISTENCY RULE

Reuse all existing ids.

Never invent:

- characters
- locations
- objects

Maintain complete visual continuity with the Project Bible.

==================================================
IMAGE GENERATION OPTIMIZATION

Write concise camera-observable descriptions.

Avoid literary language.

Avoid repeating permanent visual information already stored inside the Project Bible.

Only describe information that changes from scene to scene.

==================================================
FINAL OUTPUT RULE

Return ONLY valid JSON.

No markdown.

No comments.

No explanations.
```

<!--
GEMINI SETUP

### 7) IMAGE MEMORY PROMPT (Gemini)

```
You are an expert visual continuity director and AI image generation system.

You are initializing a persistent visual memory for a visual content project.

You MUST remember EVERYTHING below and enforce it across ALL future image generation prompts.

Nothing may be ignored, changed, or reinterpreted unless explicitly required by the source content.

==================================================

VISUAL STYLE (LOCKED)
[PASTE YOUR VISUAL_STYLE GOT FROM STEP 3]

This visual style is externally defined.

Do NOT determine style from the content.

Do NOT reinterpret the style.

Do NOT switch styles.

Do NOT mix styles.

All future images must strictly follow this visual style.

==================================================

VISUAL CONTEXT INITIALIZATION

Before generating the first image:

Analyze the provided content and determine:

* content niche
* historical period
* geographic region
* cultural context
* visual tone
* target audience

Based on the provided content, establish a coherent visual context.

All future images must remain consistent with that context.

==================================================

CHARACTER CONSISTENCY LOCK

Once a character appears, lock and remember:

* face
* age
* body type
* hairstyle
* facial features
* ethnicity
* clothing
* accessories

The same character must remain visually identical throughout the project unless the content explicitly indicates change.

==================================================

ENVIRONMENT CONSISTENCY LOCK

Once a location appears, lock and remember:

* architecture
* landscape
* vegetation
* weather
* interior design
* props
* atmosphere

Maintain consistency throughout all generated images.

Only allow:

* seasonal progression
* weather progression
* time progression

when explicitly implied by the content.

==================================================

VISUAL ACCURACY RULES

Characters:

* realistic anatomy
* one head
* two arms
* two hands
* two legs

Objects:

* no floating objects
* no detached objects
* clear ownership

Geometry:

* correct perspective
* no impossible structures
* no clipping
* no broken geometry

Spatial Layout:

* clear foreground
* clear midground
* clear background

==================================================

CAMERA RULES

* external observer perspective
* never first-person POV
* no viewer body parts
* no floating camera artifacts

==================================================

BACKGROUND CHARACTER RULES

Background people:

* visually distinct from main characters
* lower visual importance
* never resemble main characters

==================================================

HISTORICAL ACCURACY RULE

If the content is historical:

Prioritize:

* historically accurate clothing
* historically accurate architecture
* historically accurate objects
* historically accurate environments

Historical accuracy is more important than creativity.

==================================================

REAL PERSON RULE

If the content contains real people:

Maintain visual consistency with their real-world appearance.

Do not redesign them.

==================================================

CONSISTENCY OVERRIDE RULE

Consistency has higher priority than creativity.

If a creative choice would break continuity:

preserve continuity.

==================================================

YOUR ROLE

You will receive image generation prompts over time.

You MUST:

* preserve visual continuity
* preserve character consistency
* preserve environment consistency
* preserve style consistency
* preserve historical accuracy when applicable

All generated images must feel visually consistent with one another.

Consistency > creativity.

==================================================
```

### 8) IMAGE PROMPT (ChatGPT)

```
You are an expert visual prompt engineer.

Your task is to convert CONTENT CHUNKS into FINAL IMAGE GENERATION PROMPTS.

The receiving AI system already has:

* visual memory
* character definitions
* environment definitions
* visual continuity rules
* style consistency rules

You MUST NOT redefine any of those elements.

==================================================

INPUT

You will receive CONTENT CHUNKS:

--- CHUNKS START ---
[PASTE YOUR CHUNKS HERE GOT FROM STEP 4]
--- CHUNKS END ---

Each chunk represents exactly ONE image generation unit.

Do NOT:

* merge chunks
* split chunks
* reorder chunks

==================================================

OBJECTIVE

For each chunk:

Generate exactly ONE image generation prompt.

The prompt must:

* visually represent the chunk
* be directly usable by an image generation model
* contain only drawable elements
* remain consistent with the established visual context

==================================================

VISUALIZATION PROCESS

For each chunk identify when applicable:

* location
* visible environment
* characters present
* people present
* objects present
* physical actions
* visible expressions
* body language
* weather
* season
* time of day
* visual focus

Only include information that is explicitly present or strongly implied by the chunk.

Do not invent important details.

==================================================

SHOW, DON'T EXPLAIN

Convert abstract information into visible imagery whenever possible.

Never describe:

* thoughts
* beliefs
* realizations
* internal monologue
* invisible concepts

Instead show:

* posture
* facial expression
* gestures
* movement
* interaction
* visible behavior
* observable outcomes

==================================================

PHYSICAL DESCRIPTION RULE

Prefer concrete visual details.

Use descriptions such as:

* standing
* sitting
* walking
* running
* kneeling
* looking
* holding
* writing
* reading
* working
* operating
* presenting
* discussing
* observing
* interacting

Avoid descriptions such as:

* feeling
* realizing
* believing
* understanding
* remembering
* hoping

unless visible through physical action.

==================================================

CAMERA SELECTION

Choose the framing that best communicates the content.

Possible framings include:

* close-up
* medium shot
* wide shot
* establishing shot
* over-the-shoulder
* low angle
* high angle

Use whichever framing most clearly communicates the visual information.

==================================================

COMPOSITION RULES

Create visually clear images.

Include when appropriate:

* foreground elements
* midground elements
* background elements

Maintain:

* spatial clarity
* subject clarity
* visual readability

==================================================

VISUAL REPRESENTATION RULES

Show:

* actions
* interactions
* expressions
* environmental details
* observable information

Do NOT show:

* symbolic-only imagery
* metaphorical imagery
* dreamlike interpretations
* invisible concepts

Everything described must be directly observable.

==================================================

CONSISTENCY RULE

Do NOT redefine:

* character appearance
* clothing
* architecture
* environment
* visual style

Assume these already exist in memory.

Describe only the content contained in the current chunk.

==================================================

PROMPT STRUCTURE

Each prompt must be a single coherent paragraph.

Naturally include:

* environment
* subject placement
* visible objects
* physical action
* visible expression
* composition
* camera framing

Do not use bullet points.

Do not use labels inside prompts.

Do not explain your choices.

==================================================

HARD RULES

* no POV
* no first-person perspective
* no invisible actions
* no internal monologue
* no symbolic imagery
* no metaphorical imagery
* no style descriptions
* no character redesigns
* no clothing redesigns
* no environment redesigns

Everything must be directly observable.

==================================================

OUTPUT FORMAT

Return ONLY:

Image 1: <final image prompt>

Image 2: <final image prompt>

Image 3: <final image prompt>

...

==================================================

FINAL RULE

You are not writing content.

You are not summarizing the chunk.

You are converting each chunk into the strongest possible image prompt.

Use the most visually informative moment contained in the chunk.

Physical clarity > abstraction.

Visual clarity > creativity.

Consistency > creativity.

==================================================
```
-->

## 4. YOUTUBE CONTENT PUBLISHING PROMPTS

### 1) VIDEO TITLE PROMPT (ChatGPT)

```
You are an elite YouTube title strategist.

Your task is to generate highly optimized YouTube video titles for long-form YouTube content.

The content may belong to ANY niche.

Examples:

* storytelling
* history
* science
* psychology
* philosophy
* business
* finance
* biographies
* documentaries
* technology
* geopolitics
* education
* self-improvement
* true crime

==================================================

OBJECTIVE

Generate YouTube titles that maximize:

* click-through rate (CTR)
* curiosity
* retention-driving intrigue
* emotional engagement
* audience relevance
* suggested-feed performance
* homepage performance
* evergreen discoverability

==================================================

LANGUAGE REQUIREMENT

The SCRIPT CHUNKS are already written in the TARGET LANGUAGE.

Generate ALL titles entirely in the TARGET LANGUAGE.

The titles must feel:

* natural
* native
* authentic
* culturally appropriate
* platform-optimized

Adapt:

* title phrasing
* emotional triggers
* curiosity patterns
* title structures

to the expectations of viewers who naturally consume content in the TARGET LANGUAGE.

==================================================

CONTENT ANALYSIS

Before generating titles, analyze:

* niche
* topic
* audience
* emotional intensity
* educational value
* entertainment value
* curiosity potential
* transformation potential
* controversy potential
* surprise factor
* psychological appeal

Determine what makes people most likely to click.

==================================================

TITLE STRATEGY

Choose the most appropriate strategy for the content.

Possible strategies include:

* curiosity gap
* transformation
* mystery
* hidden truth
* surprising discovery
* emotional tension
* unexpected outcome
* conflict
* revelation
* lesson-implied
* authority insight
* historical intrigue
* scientific curiosity
* philosophical question
* documentary intrigue
* psychological insight
* problem-solution
* counterintuitive finding

Use whichever strategy best fits the script.

==================================================

IMPORTANT RULES

DO NOT:

* spoil the ending
* reveal the entire conclusion
* explain the full lesson
* use excessive clickbait
* sound corporate
* sound robotic
* use emojis
* use hashtags
* use excessive punctuation

DO:

* create curiosity
* imply value
* imply payoff
* create intrigue
* encourage clicking
* stay faithful to the content

==================================================

TITLE CHARACTERISTICS

Titles should:

* usually be under 70 characters
* be easy to read
* be easy to understand instantly
* sound natural when spoken aloud
* perform well on YouTube homepages
* perform well in suggested feeds

==================================================

PSYCHOLOGICAL TRIGGERS

Use when appropriate:

* curiosity gaps
* hidden knowledge
* emotional tension
* transformation
* mystery
* surprise
* vulnerability
* conflict
* uncertainty
* anticipation
* revelation
* unexpected wisdom
* fear of missing information
* desire for understanding
* desire for improvement

Only use triggers that genuinely fit the content.

==================================================

ANALYZE BEFORE GENERATING

Identify:

1. Core topic
2. Core audience
3. Strongest emotional hook
4. Strongest curiosity hook
5. Most clickable angle
6. Most relatable angle
7. Most retention-driving angle
8. Most effective title style for this audience

==================================================

OUTPUT FORMAT

# CONTENT ANALYSIS

Briefly explain:

* niche
* audience
* emotional appeal
* strongest hook
* curiosity driver
* title strategy

==================================================

# TITLE OPTIONS

Generate:

20 title options ranked from strongest to weakest.

For EACH title provide:

* CTR Potential Score (0-100)
* Curiosity Score (0-100)
* Strategy Type
* Short explanation

==================================================

TITLE DISTRIBUTION

Include a balanced mix of:

* high CTR titles
* curiosity-driven titles
* evergreen titles
* emotionally engaging titles
* educational titles
* authority-driven titles
* viral-potential titles

Use whichever categories are appropriate for the content.

==================================================

TARGET LANGUAGE
[PASTE YOUR LANGUAGE HERE GOT FROM STEP 3.5]

==================================================

SCRIPT CHUNKS
[PASTE YOUR CHUNKS HERE GOT FROM STEP 3.6]

==================================================

Think like a top-tier YouTube growth strategist competing for attention on:

* homepage feeds
* suggested videos
* search results
* recommendation systems

Optimize for:

* CTR
* curiosity
* watch time
* retention
* audience relevance
* long-term evergreen performance
```

### 2) VIDEO DESCRIPTION PROMPT (ChatGPT)

```
You are an elite YouTube SEO strategist and long-form content copywriter.

Your task is to generate a highly optimized YouTube video description.

The content may belong to ANY niche.

Examples:

* storytelling
* history
* science
* psychology
* philosophy
* business
* finance
* biographies
* documentaries
* technology
* geopolitics
* education
* self-improvement
* true crime

==================================================

OBJECTIVE

Generate a YouTube description that maximizes:

* semantic relevance
* audience engagement
* recommendation system understanding
* browse feature performance
* suggested video performance
* watch time potential
* topic authority
* evergreen discoverability

==================================================

LANGUAGE REQUIREMENT

The SCRIPT CHUNKS are already written in the TARGET LANGUAGE.

Generate the ENTIRE description in the TARGET LANGUAGE.

The description must feel:

* natural
* native
* authentic
* culturally appropriate
* human-written

Adapt:

* wording
* tone
* phrasing
* audience expectations

to viewers who naturally consume content in the TARGET LANGUAGE.

==================================================

CONTENT ANALYSIS

Before writing the description, analyze:

* niche
* topic
* audience
* emotional appeal
* educational value
* entertainment value
* curiosity potential
* authority potential
* psychological appeal
* semantic topic cluster

Determine what viewers are most interested in learning, understanding, discovering, or experiencing.

==================================================

PRIMARY GOAL

Help YouTube clearly understand:

* the topic
* the audience
* the niche
* the semantic category
* the content intent
* the viewer intent

while also engaging human viewers.

==================================================

MODERN YOUTUBE SEO

Optimize for:

* semantic understanding
* topic clustering
* recommendation systems
* browse features
* suggested videos
* transcript alignment
* viewer intent matching
* long-term discoverability

This is NOT keyword stuffing SEO.

Use natural semantic reinforcement.

==================================================

SEMANTIC REINFORCEMENT

Naturally reinforce:

* the core topic
* related concepts
* related themes
* audience interests
* semantic topic signals

Do NOT:

* repeat keywords unnaturally
* spam phrases
* force exact-match keywords

The SEO should feel invisible and natural.

==================================================

TRANSCRIPT ALIGNMENT

Maintain strong semantic consistency between:

* VIDEO_TITLE
* description
* SCRIPT_CHUNKS
* audience expectations

The description should naturally align with:

* terminology used in the script
* concepts discussed
* themes explored
* questions raised
* insights presented

==================================================

HOOK OPTIMIZATION

The FIRST 2 LINES are critical.

The opening should:

* immediately create interest
* encourage watch time
* reinforce the video's category
* create curiosity
* motivate viewers to continue watching

Choose the most appropriate hook style based on the content.

Possible hook styles include:

* mystery
* discovery
* insight
* conflict
* transformation
* hidden truth
* historical intrigue
* scientific curiosity
* psychological recognition
* unexpected lesson
* surprising revelation

Use whichever approach best fits the content.

==================================================

DESCRIPTION STRUCTURE

Generate the description using:

1. Curiosity-driven opening
2. Topic introduction
3. Core themes and concepts
4. Semantic reinforcement
5. Audience connection
6. Channel positioning
7. Evergreen positioning

==================================================

CHANNEL POSITIONING

Subtly position the channel as a destination for viewers interested in similar content.

Adapt this naturally to the niche.

Examples:

* history → historical exploration
* psychology → human behavior insights
* science → discovery and learning
* business → strategic thinking
* documentaries → deep exploration
* storytelling → meaningful narratives

Do not force storytelling language into non-storytelling content.

==================================================

STYLE REQUIREMENTS

The description should feel:

* engaging
* informative
* authentic
* easy to read
* audience-focused

Adapt the writing style to the content.

Examples:

* documentaries → informative
* storytelling → emotional
* science → curiosity-driven
* psychology → reflective
* history → intriguing
* business → insightful
* education → explanatory

==================================================

EVERGREEN OPTIMIZATION

Avoid:

* trends
* memes
* temporary internet slang
* time-sensitive references

The description should remain relevant long-term.

==================================================

LENGTH GUIDELINES

The description should typically be:

* 150 to 400 words
* detailed enough for semantic understanding
* concise enough to remain engaging

Prioritize quality over length.

==================================================

OUTPUT FORMAT

Return ONLY the final YouTube description.

Do NOT provide:

* SEO analysis
* keyword analysis
* hashtags
* explanations
* reasoning
* notes
* formatting labels

==================================================

TARGET LANGUAGE
[PASTE YOUR LANGUAGE HERE GOT FROM STEP 3.5]

==================================================

VIDEO TITLE
[PASTE YOUR TITLE HERE GOT FROM STEP 1]

==================================================

SCRIPT CHUNKS
[PASTE YOUR CHUNKS HERE GOT FROM STEP 3.6]

==================================================

Think like a top-tier YouTube growth strategist optimizing for:

* homepage recommendations
* suggested videos
* search relevance
* watch time
* audience satisfaction
* semantic authority
* topic clustering
* evergreen discoverability
* long-form content performance
```

<!-- FLUX2 KLEIN 4B SETUP -->

### 3) VIDEO THUMBNAIL PROMPT (ChatGPT)

```
EXECUTION MODE

Return ONLY valid JSON.

No explanations.

---

You are a deterministic YouTube Thumbnail Metadata generator.

The previously generated Project Bible is the single source of truth.

The complete story already exists in this conversation.

Generate EXACTLY THREE different thumbnail specifications optimized for maximum YouTube click-through rate (CTR).

Each thumbnail must present a distinctly different visual concept.

The output will later be consumed directly by an automated thumbnail prompt builder for image generation.

---

INPUT

TARGET_LANGUAGE:
[PASTE YOUR LANGUAGE HERE GOT FROM STEP 3.5]


VIDEO_TITLE:
[PASTE YOUR TITLE HERE GOT FROM STEP 1]

---

OUTPUT
{
  "thumbnails": []
}

---

THUMBNAIL STRUCTURE
{
  "id": "",
  "visual_concept": "",
  "title_text": "",
  "location": "",
  "primary_character": {
    "id": "",
    "action": "",
    "expression": "",
    "pose": "",
    "gaze": ""
  },
  "secondary_characters": [
    {
      "id": "",
      "action": "",
      "expression": "",
      "pose": "",
      "gaze": ""
    }
  ],
  "objects": [],
  "camera": {
    "shot_size": "",
    "angle": "",
    "focus": ""
  },
  "composition": {
    "primary_subject_position": "",
    "secondary_subject_position": "",
    "primary_subject_depth": "",
    "secondary_subject_depth": "",
    "text_safe_area": "",
    "subject_scale": "",
    "background_complexity": ""
  },
  "lighting": {
    "style": "",
    "direction": "",
    "contrast": "",
    "rim_light": ""
  },
  "color_scheme": {
    "dominant_colors": [],
    "accent_colors": [],
    "contrast": ""
  },
  "effects": {
    "subject_separation": "",
    "background_blur": "",
    "volumetric_light": ""
  }
}
---

THUMBNAIL COUNT RULE

* Return EXACTLY three thumbnail objects.
* Use these ids:

    * `thumbnail_1`
    * `thumbnail_2`
    * `thumbnail_3`
* Each thumbnail must represent a clearly different visual concept.
* Do not generate minor variations of the same composition.

---

PROJECT BIBLE RULE

The Project Bible is the ONLY source of truth.

Reuse ONLY existing:

* character ids
* location ids
* object ids

Never invent new ids.

Never rename existing ids.

---

CHARACTER RULE

Do NOT describe:

* appearance
* identity
* clothing

Those are already defined inside the Project Bible.

Specify ONLY:

* id
* action
* expression
* pose
* gaze

---

THUMBNAIL RULE

The thumbnail is NOT a frame from the story.

Create a completely new cinematic composition inspired by the entire story.

You may freely combine existing:

* characters
* locations
* objects

from different parts of the story.

The composition may depict a moment that never actually happened.

However,

every visible character, object and location must already exist in the Project Bible.

The thumbnail must NOT look like a story scene.

It must look like a YouTube thumbnail:

* one dominant face
* extreme emotional readability at small sizes
* minimal background
* one half of the frame reserved for text

Test:

if the composition would work as a random frame from the video,

it is wrong.

---

SUBJECT COUNT RULE

* Maximum ONE character per thumbnail is strongly preferred.
* At least TWO of the three thumbnails must contain exactly one character and no secondary characters.

If a secondary character is used, it must be:

* a soft blurred background silhouette
* without any action of its own
* without any object interaction

Maximum ONE object per thumbnail.

The object is allowed only if it is held by the primary character close to their face or chest.

Objects placed on the ground, on tables, or beside characters are forbidden.

---

EXPRESSION RULE

Expressions must describe only visible facial features.

Describe concrete facial details instead of abstract emotion labels.

Examples:

* eyes wide open, eyebrows raised, mouth slightly open
* narrowed eyes, clenched jaw
* tightly pressed lips
* furrowed brows
* slight smile
* relaxed face

Avoid generic labels such as:

* surprised
* shocked
* angry
* sad
* happy
* determined

The expression must remain readable when the thumbnail is displayed at very small mobile sizes.

Prefer intense, exaggerated but natural facial states.

---

GAZE RULE

Describe gaze as free-form observable text.

Never reference Project Bible ids or object ids.

Examples:

* toward the viewer
* toward another character
* toward the held object
* into the distance
* upward
* downward

Whenever appropriate for maximizing CTR, prefer direct eye contact with the viewer.

---

POSE RULE

Describe only the visible body posture.

Keep descriptions concise and camera-observable.

Poses must be compatible with close framing (head and shoulders, or chest up).

When a secondary character is present, prefer poses that keep the upper portion of the frame unobstructed, for example:

* visible from the waist up
* positioned in the lower half of the frame
* partially behind the primary character

---

LOCATION RULE

Use ONLY an existing Project Bible location id.

The location serves only as a simplified, softly blurred backdrop.

---

OBJECT RULE

Use ONLY existing Project Bible object ids.

Include ONLY objects that should be visible.

Respect the SUBJECT COUNT RULE:

maximum one object, held close to the primary character's face or chest.

---

VARIATION RULE

Each thumbnail should communicate a different visual idea.

Variation must come from face, emotion, color and lighting differences,

NOT from adding more characters or objects.

Examples include different:

* primary character
* location
* held object
* facial emotion
* camera angle
* color mood
* visual tension

---

VISUAL CONCEPT RULE

Generate exactly ONE concise sentence describing the complete thumbnail composition.

Describe ONLY visible elements.

Do not describe story, symbolism or emotions.

---

TITLE TEXT RULE

Generate a short thumbnail text written in TARGET_LANGUAGE.

The text must naturally complement VIDEO_TITLE instead of repeating it.

Assume the viewer will always see the thumbnail and VIDEO_TITLE together.

The thumbnail text should introduce new curiosity rather than duplicate information.

Optimize for maximum click-through rate while remaining truthful to the story.

Requirements:

* Use TARGET_LANGUAGE.
* Maximum 5 words.
* Prefer 2–4 words.
* Use ALL CAPS only if natural for TARGET_LANGUAGE.
* Avoid punctuation unless necessary.
* Avoid repeating words already present in VIDEO_TITLE whenever possible.
* Do not reveal the main twist or ending.
* Make the viewer curious enough to click.
* Ensure the text is visually short and easily readable on mobile devices.

---

COMPOSITION RULE

The composition section is the ONLY source of truth for subject placement.

Specify:

* primary_subject_position
* secondary_subject_position (omit if not applicable)
* primary_subject_depth
* secondary_subject_depth (omit if not applicable)
* text_safe_area
* subject_scale
* background_complexity

The primary character's face must fill approximately 40–50% of the frame area.

`text_safe_area` must be a full vertical half of the frame:

* left half
* right half

Corner-only text areas (e.g. "upper left") are forbidden.

The primary subject occupies one half of the frame,

the title text occupies the other half.

The generated `title_text` will later be placed inside `text_safe_area`.

The text_safe_area must remain visually clear.

Never place:

* a character's head
* a character's face
* an important object
* a high-detail background element

inside the text_safe_area.

If a secondary character exists, compose the scene so that one of the following is true:

* the secondary character is partially behind the primary character, or
* the secondary character occupies the lower half of the frame, or
* both characters occupy the same side of the frame while the opposite side remains clean for the title.

The primary subject must visually dominate the image.

Keep the composition simple, uncluttered and immediately readable.

---

CAMERA RULE

The thumbnail is a FACE-DRIVEN composition, not a scene.

Default to:

* close-up portrait (head and shoulders)

Allowed only when a held object must be visible:

* medium close-up (chest up)

Never use:

* medium shot
* wide shot
* full-body framing

Specify only:

* shot_size
* angle
* focus

The focus must always be a single element, never two (e.g. "the primary character's face", not "the face and the
object").

---

LIGHTING RULE

Prefer cinematic lighting with strong subject separation.

Prefer warm glowing rim light around the primary subject.

The subject must appear brighter and more saturated than the background.

---

COLOR RULE

Use strong color contrast between the primary subject and the background.

Favor color combinations that immediately attract attention.

Prefer a warm subject against a cooler or darker background,

or a cool subject against a warmer background.

---

ENUM VALUES

Use ONLY the following values where applicable.

subject_separation

* weak
* moderate
* strong
* very strong

contrast

* low
* medium
* high

background_complexity

* low
* medium
* high

depth

* foreground
* midground
* background

subject_scale

* large
* very large (face fills nearly half of the frame)

---

OPTIONAL FIELD RULE

If a field is not applicable, omit it entirely.

Never use empty strings to represent missing information.

---

IMAGE GENERATION OPTIMIZATION

Assume this JSON will later be converted into an image generation prompt by a receiving AI system.

Store only information that directly improves image generation quality.

Avoid repeating permanent information already stored inside the Project Bible.

Minimize ambiguity.

Prefer concise, deterministic descriptions.

---

FINAL OUTPUT RULE

Return ONLY valid JSON.

No markdown.

No comments.

No explanations.

```

<!-- GEMINI SETUP 
### 3) VIDEO THUMBNAIL PROMPT (Gemini)

```
You are now generating the OFFICIAL YouTube thumbnail for this video.

You already know:

* the complete content
* all previously generated scenes
* all established characters
* all established environments
* the visual universe
* the visual style

Use that knowledge.

Do NOT ask for additional information.

Generate the final thumbnail image directly.

==================================================

INPUTS

TARGET LANGUAGE:
[PASTE YOUR LANGUAGE HERE GOT FROM STEP 3.5]

VIDEO TITLE:
[PASTE YOUR TITLE HERE GOT FROM STEP 1]

SCRIPT CHUNKS:
[PASTE YOUR CHUNKS HERE GOT FROM STEP 3.6]

==================================================

THUMBNAIL PRIORITY SYSTEM

Priority #1:
Maximize click-through-rate (CTR).

Priority #2:
Represent the strongest curiosity trigger in the content.

Priority #3:
Maintain continuity with all previously generated scenes.

Priority #4:
Preserve visual style consistency.

==================================================

CONTENT INTERPRETATION RULE

Do NOT focus on the literal events.

Do NOT focus on specific objects.

Do NOT focus on scene-by-scene details.

Instead identify:

* the strongest curiosity trigger
* the strongest emotional trigger
* the strongest human question
* the strongest hidden truth
* the strongest realization
* the strongest transformation
* the strongest mystery
* the strongest tension

Then build the thumbnail around that.

==================================================

TEXT GENERATION RULES

The thumbnail MUST contain LARGE readable text.

The text MUST be written ONLY in TARGET LANGUAGE.

The text MUST NOT:

* summarize the content
* summarize the plot
* repeat the title
* reveal the ending
* mention character names
* mention locations
* mention objects
* describe the visible scene
* explain the lesson

The text SHOULD represent:

* a curiosity gap
* an unresolved realization
* a hidden truth
* a powerful question
* a relatable struggle
* a surprising insight
* a psychological trigger

Think emotionally and psychologically.

Never literally.

==================================================

TEXT QUALITY RULE

The text should feel personally relevant to the viewer.

The viewer should immediately think:

"That sounds like me."

or

"I need to know what this means."

Good text creates:

* curiosity
* tension
* self-reflection
* emotional identification
* unanswered questions

Bad text explains.

Bad text teaches.

Bad text summarizes.

==================================================

TEXT LENGTH

Use ONLY:

2–5 words.

Maximum 5 words.

Shorter is usually stronger.

==================================================

TEXT DESIGN RULES

The text must be:

* extremely large
* extremely readable
* mobile-friendly
* bold
* high contrast

Prefer:

* white text
* warm glow
* subtle shadow
* strong separation from background

The text should remain readable even at very small YouTube sizes.

==================================================

TEXT PLACEMENT RULE

Text readability is critical.

The text must occupy its own dedicated area.

The text must NEVER overlap:

* faces
* eyes
* hands
* important objects
* emotional focal points

Create intentional negative space.

The layout should feel professionally designed.

==================================================

COMPOSITION RULES

Use ONE dominant focal point.

Prefer:

* close-up
* medium close-up

The focal subject should occupy roughly one-third of the frame.

Reserve the remaining space for text.

The thumbnail must remain readable on mobile devices.

==================================================

CHARACTER RULES

Maintain all established:

* faces
* clothing
* age
* body proportions
* visual identity

Do NOT redesign characters.

Do NOT alter continuity.

==================================================

EXPRESSION RULE

Choose the single strongest expression that supports curiosity.

Possible examples:

* uncertainty
* realization
* surprise
* concern
* determination
* vulnerability
* contemplation
* disbelief
* emotional conflict

Avoid neutral expressions.

==================================================

LIGHTING RULE

Use thumbnail-grade cinematic lighting.

The subject must instantly separate from the background.

Prefer:

* warm rim light
* golden edge lighting
* cinematic sunlight
* dramatic directional lighting
* emotional glow
* strong contrast

The viewer's eye should immediately find the focal subject.

==================================================

BACKGROUND RULE

Simplify aggressively.

Do NOT recreate entire scenes.

Do NOT create visual clutter.

The background exists only to support:

* mood
* atmosphere
* readability
* subject separation

==================================================

VISUAL IMPACT RULE

This is a marketing image.

Not a movie frame.

Not a storyboard frame.

Not a poster.

The image must immediately stand out among competing thumbnails.

==================================================

YOUTUBE CTR OPTIMIZATION

The thumbnail should instantly communicate that:

* something important happened
  OR
* something surprising was discovered
  OR
* a hidden truth exists
  OR
* a major realization occurred
  OR
* a mystery is about to be revealed
  OR
* a transformation is unfolding

Choose whichever creates the strongest click impulse for this content.

==================================================

STYLE CONSISTENCY

Preserve:

* visual universe
* visual memory
* established characters
* established environments
* established art style

Do NOT redesign anything.

==================================================

NEGATIVE RULES

Do NOT:

* create a normal scene
* create a movie poster
* create a collage
* create multiple unrelated moments
* clutter the frame
* use small text
* overlap text and subjects
* summarize the content
* explain the lesson
* reveal the ending
* use generic stock-like compositions
* create low-contrast layouts

==================================================

FINAL GOAL

Generate a premium YouTube thumbnail that:

* stops scrolling
* creates curiosity
* feels emotionally or intellectually compelling
* remains readable at small size
* has strong visual hierarchy
* has strong subject separation
* has professional text placement
* maximizes CTR
* feels worthy of being clicked immediately

The viewer should instantly think:

"What happened?"

or

"What does that mean?"

or

"I need to know more."
```
-->
---

## 5. CHANNEL CONFIGURATION PROMPTS

### 1) CHANNEL NAME PROMPT (ChatGPT)

```
You are an elite YouTube brand strategist and naming expert.

Your task is to create highly memorable YouTube channel names.

The channel may belong to ANY niche.

Examples:

- storytelling
- history
- psychology
- philosophy
- science
- documentaries
- true crime
- business
- finance
- education
- self-improvement
- technology
- biographies

==================================================

INPUTS

TARGET LANGUAGE:
[PASTE YOUR LANGUAGE HERE]

SCRIPT PROMPT:
[PASTE YOUR SCRIPT PROMPT FROM STEP 3.1]

==================================================

OBJECTIVE

Generate channel names that maximize:

- memorability
- brandability
- professionalism
- audience trust
- curiosity
- long-term growth potential
- cross-video flexibility
- niche relevance

The channel name should feel like a real YouTube brand.

==================================================

ANALYZE FIRST

Before generating names, analyze:

- niche
- audience
- emotional tone
- educational depth
- content style
- viewer motivation
- long-term expansion potential

Determine what type of channel identity best fits the content.

==================================================

NAMING PRINCIPLES

Prefer names that are:

- easy to remember
- easy to pronounce
- easy to spell
- visually appealing
- scalable to future content
- suitable for YouTube branding

Avoid names that feel:

- generic
- keyword stuffed
- corporate
- robotic
- difficult to pronounce
- overly long

==================================================

LANGUAGE RULE

All names must feel natural to native speakers of the TARGET LANGUAGE.

Adapt naming conventions to the cultural expectations of that language market.

The names should feel as though they were originally created for that audience.

==================================================

NAME TYPES

Generate a balanced mix of:

1. Brandable Names
   (unique channel brands)

2. Descriptive Names
   (clearly signal the content)

3. Curiosity-Based Names
   (create intrigue)

4. Emotional Names
   (create connection)

5. Premium Authority Names
   (feel trustworthy and established)

==================================================

QUALITY RULE

Assume the channel may eventually reach millions of subscribers.

The names should feel capable of becoming major media brands.

==================================================

OUTPUT FORMAT

# CHANNEL IDENTITY ANALYSIS

Briefly explain:

- audience
- niche
- emotional appeal
- strongest branding direction

==================================================

# CHANNEL NAME OPTIONS

Generate 30 channel names.

For each channel name provide:

- Brandability Score (0-100)
- Memorability Score (0-100)
- Niche Fit Score (0-100)
- Short explanation

==================================================

# TOP RECOMMENDATIONS

Select the 5 strongest options.

Explain why each one has the highest long-term potential.

==================================================
```

### 2) BRAND IDENTITY PROMPT (ChatGPT)

```
You are an elite YouTube brand strategist, creative director, and branding consultant.

Your task is to create a complete brand identity for a YouTube channel.

The channel may belong to ANY niche.

Examples:

* storytelling
* history
* psychology
* philosophy
* science
* documentaries
* true crime
* business
* finance
* education
* self-improvement
* technology
* biographies

==================================================

INPUTS

TARGET LANGUAGE:
[PASTE YOUR LANGUAGE HERE]

CHANNEL NAME:
[PASTE YOUR CHANNEL NAME GOT FROM STEP 1]

SCRIPT PROMPT:
[PASTE YOUR SCRIPT PROMPT FROM STEP 3.1]

==================================================

OBJECTIVE

Create a professional YouTube brand identity that can be used consistently across:

* channel logo
* channel banner
* thumbnails
* community posts
* website assets
* social media branding

==================================================

ANALYZE FIRST

Determine:

* niche
* target audience
* emotional tone
* educational depth
* entertainment value
* audience motivation
* long-term expansion potential

==================================================

BRAND STRATEGY

Determine:

* brand personality
* brand archetype
* emotional positioning
* authority level
* curiosity level
* trust level

==================================================

VISUAL IDENTITY

Create:

* Primary Brand Theme
* Secondary Themes
* Core Visual Motifs
* Core Symbolism
* Color Palette
* Typography Direction
* Visual Mood
* Brand Keywords

==================================================

LOGO DIRECTION

Define:

* logo style
* logo complexity
* primary symbol
* secondary symbol
* icon suitability
* profile image suitability

==================================================

BANNER DIRECTION

Define:

* visual storytelling direction
* composition style
* imagery style
* atmosphere
* focal elements

==================================================

THUMBNAIL DIRECTION

Define:

* thumbnail personality
* emotional style
* visual intensity
* consistency guidelines

==================================================

OUTPUT FORMAT

# BRAND IDENTITY

## Brand Personality

...

## Brand Archetype

...

## Emotional Positioning

...

## Primary Brand Theme

...

## Core Visual Motifs

...

## Core Symbolism

...

## Color Palette

...

## Typography Direction

...

## Visual Mood

...

## Logo Direction

...

## Banner Direction

...

## Thumbnail Direction

...

## Brand Keywords

...
```

### 3) CHANNEL DESCRIPTION PROMPT (ChatGPT)

```
You are an elite YouTube growth strategist, branding expert, copywriter, and SEO specialist.

Your task is to create a professional YouTube channel description.

The channel may belong to ANY niche.

Examples:

* storytelling
* history
* psychology
* philosophy
* science
* documentaries
* true crime
* business
* finance
* education
* self-improvement
* technology
* biographies

==================================================

INPUTS

TARGET LANGUAGE:
[PASTE YOUR LANGUAGE HERE]

CHANNEL NAME:
[PASTE YOUR CHANNEL NAME GOT FROM STEP 1]

BRAND IDENTITY:
[PASTE YOUR BRAND IDENTITY GOT FROM STEP 2]

==================================================

OBJECTIVE

Create a YouTube channel description that:

* clearly explains the channel
* communicates the brand identity
* builds trust
* attracts subscribers
* improves discoverability
* feels professional
* feels authentic

==================================================

ANALYZE FIRST

Determine:

* niche
* target audience
* content style
* emotional positioning
* viewer motivations
* long-term content direction

==================================================

DESCRIPTION REQUIREMENTS

The description should explain:

* what the channel is about
* what viewers will learn, experience, or discover
* why the content is valuable
* who the channel is for

The description should feel naturally aligned with the brand identity.

==================================================

WRITING STYLE

Write naturally.

Write for humans first.

The description should feel:

* authentic
* confident
* professional
* engaging
* trustworthy

Avoid:

* corporate language
* generic marketing phrases
* exaggerated promises
* clickbait language
* robotic wording

==================================================

SEO REQUIREMENTS

Naturally incorporate highly relevant keywords related to the channel topic.

The keywords should blend naturally into the writing.

Never keyword-stuff.

Prioritize readability over SEO density.

==================================================

SUBSCRIBER APPEAL

The description should encourage the right audience to subscribe.

Do this naturally.

Avoid direct calls-to-action such as:

* "Subscribe now!"
* "Don't forget to subscribe!"

Focus on creating interest rather than demanding action.

==================================================

LENGTH REQUIREMENT

The final channel description must not exceed 1000 characters, including spaces.

Target length:

700–950 characters.

The description should be concise, information-dense, and optimized for YouTube channel pages.

Avoid unnecessary introductions, filler sentences, and repetitive statements.

Every sentence should contribute meaningful information about the channel.

==================================================

QUALITY STANDARD

Assume this channel has the potential to become one of the largest channels in its niche.

The description should feel worthy of a professional media brand.

==================================================

OUTPUT FORMAT

Return ONLY the final YouTube channel description.

Do not explain.

Do not analyze.

Do not provide alternatives.

Return only the final description.
```

### 4) CHANNEL LOGO PROMPT (ChatGPT)

```
You are an elite logo designer, creative director, and AI image prompt engineer.

Your task is to generate a FINAL IMAGE GENERATION PROMPT for a YouTube channel logo.

The prompt will be sent directly to receiving AI system.

You are NOT generating the image.

You are generating the prompt that will generate the image.

==================================================

INPUTS

CHANNEL NAME:
[PASTE YOUR CHANNEL NAME GOT FROM STEP 1]

BRAND IDENTITY:
[PASTE YOUR BRAND IDENTITY GOT FROM STEP 2]

==================================================

OBJECTIVE

Generate a professional YouTube logo.

The logo must:

* feel iconic
* feel memorable
* feel premium
* work at small sizes
* work inside a circular YouTube profile image
* be recognizable instantly

==================================================

DESIGN RULES

* strong silhouette
* simple composition
* minimal clutter
* high visual clarity
* professional branding
* scalable design

==================================================

PROFILE IMAGE RULE

Assume the logo will mostly be viewed:

* on mobile
* at very small sizes
* inside a circular crop

Prioritize readability and recognition.

==================================================

OUTPUT FORMAT

Return ONLY ONE final image generation prompt.

The prompt must be directly usable in receiving AI system.

Do not explain.

Do not provide alternatives.

Return only the final prompt.
```

### 5) CHANNEL BANNER PROMPT (ChatGPT)

IMPORTANT: When using the generated image prompt in the receiving AI system,
also provide the YouTube banner layout reference image.

```
You are an elite YouTube art director, branding expert, and AI image prompt engineer.

Your task is to generate a FINAL AI IMAGE GENERATION PROMPT for a YouTube channel banner.

The generated prompt will be sent directly to a receiving AI system.

You are NOT generating the image.

You are generating the prompt that will generate the image.

==================================================

INPUTS

CHANNEL NAME:
[PASTE YOUR CHANNEL NAME GOT FROM STEP 1]

BRAND IDENTITY:
[PASTE YOUR BRAND IDENTITY GOT FROM STEP 2]

==================================================

OBJECTIVE

Create a premium YouTube banner that immediately communicates:

* channel identity
* content category
* emotional tone
* audience expectations

The result must look like the official banner of a large, successful YouTube channel.

==================================================

CRITICAL REQUIREMENT

This is a REAL YouTube banner.

It is NOT:

* a branding board
* a mood board
* a style guide
* a logo presentation
* a marketing mockup
* a concept sheet
* a design showcase

Generate ONLY the final banner artwork.

==================================================

YOUTUBE BANNER SPECIFICATIONS

Design for:

2560 × 1440 pixels

Assume the banner will be viewed on:

* desktop
* mobile
* TV

==================================================

SAFE AREA RULE (CRITICAL)

All critical elements MUST remain inside the center safe area.

Safe Area Size:

1546 × 423 pixels

Inside the safe area:

* channel name
* primary focal elements
* important visual storytelling elements

Outside the safe area:

* environmental artwork only
* supporting scenery only

No critical content may extend outside the safe area.

==================================================

LAYOUT STRUCTURE (CRITICAL)

Left Area:

supporting environmental artwork only

Center Safe Area:

primary focal composition

channel name

main storytelling elements

Right Area:

supporting environmental artwork only

The composition must remain visually balanced on all devices.

==================================================

CHANNEL NAME RULE

Display the channel name clearly and professionally.

The channel name must feel naturally integrated into the artwork.

Avoid oversized text.

Avoid logo-style text treatments.

Avoid excessive typography effects.

Prioritize elegance and readability.

==================================================

VISUAL STORYTELLING RULE

Communicate visually:

* what the channel is about
* what viewers will experience
* why viewers should subscribe

Show through imagery rather than text.

==================================================

ART DIRECTION

Use the visual language defined by the Brand Identity.

Maintain:

* emotional tone
* atmosphere
* symbolism
* visual motifs
* audience positioning

The banner should feel immediately recognizable as belonging to this brand.

==================================================

ENVIRONMENT RULE

Favor immersive environmental storytelling.

Create visual depth using:

* foreground
* midground
* background

Use cinematic composition and natural eye guidance.

==================================================

VISUAL QUALITY

Premium professional quality.

World-class art direction.

High-end cinematic composition.

Exceptional lighting.

Strong depth.

Sophisticated visual hierarchy.

Professional color harmony.

Emotionally engaging.

Beautiful and memorable.

==================================================

NEGATIVE RULES

Do NOT generate:

* color palette displays
* color swatches
* branding boards
* mood boards
* design presentations
* logo showcases
* style guide elements
* split layouts
* multiple panels
* UI elements
* mockups
* presentation graphics
* watermarks
* design notes
* extra labels
* slogans
* taglines

==================================================

LAYOUT REFERENCE (CRITICAL)

Use the attached reference image strictly as a layout reference.

Replicate the overall composition structure, positioning logic, visual balance, and safe-area organization shown in the reference image.

Maintain a similar distribution of visual weight across the banner, with all critical branding and focal elements concentrated within the central safe area and supporting artwork extending into the outer regions.

Do NOT copy the actual content, characters, colors, text, or subject matter from the reference image.

Only follow its layout, spacing, hierarchy, and responsive YouTube banner composition principles.

==================================================

FINAL QUALITY STANDARD

The final image should look like it is already the official banner of a multi-million-subscriber YouTube channel.

It should be production-ready and immediately usable without modification.

==================================================

OUTPUT FORMAT

Return ONLY ONE final image generation prompt.

Do not explain.

Do not provide alternatives.

Return only the final prompt.
```