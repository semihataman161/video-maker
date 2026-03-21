# Get script from Claude Sonnet 4.5
SCRIPT = """
Liam was twenty-eight years old.

He lived in a small mountain town where everyone knew each other.

For the past year, he had felt stuck.

He wanted his life to change.

He wanted a better job, a relationship, a fresh start.

But nothing seemed to move forward.

Every day felt the same.

This feeling made him restless.

He would start projects and abandon them.

He would make plans and give up halfway.

He kept waiting for something big to happen.

Some sign that would tell him what to do.

But the sign never came.

At the grocery store, he sighed.

At the coffee shop, he scrolled through his phone, searching.

He watched other people and wondered why their lives seemed to work.

His own felt frozen in place.

One cold afternoon, Liam walked past the community garden.

An old man was working there alone.

His name was Thomas.

Thomas had lived in the town his whole life.

He used to run the hardware store until he retired.

Now he spent most of his time in the garden.

People said he could grow anything.

Even in the hardest seasons, something in his plot was alive.

Liam had walked past the garden a hundred times.

But today, he stopped.

Thomas was kneeling in the dirt, even though it was winter.

"What are you planting?" Liam asked.

Thomas looked up and smiled.

"Garlic," he said.

"In winter?" Liam asked.

"It seems like the wrong time."

"It's exactly the right time," Thomas replied.

They talked for a few minutes.

Something about Thomas made Liam feel comfortable.

Before he knew it, Liam was speaking honestly.

"I feel stuck," Liam said.

"I keep waiting for my life to change, but nothing happens."

Thomas brushed the dirt from his hands.

"Do you have a few hours?" he asked.

"Yes," Liam said.

"Then help me plant," Thomas said.

"It might teach you something."

Liam agreed, though he wasn't sure why.

Thomas handed him a small bag of garlic cloves.

"We're going to plant these," Thomas said.

"Each one goes in the ground, pointed side up."

"About two inches deep."

"Six inches apart."

Liam knelt down and began.

The ground was cold and hard.

He had to press firmly to make each hole.

It was slow work.

After ten cloves, his hands were dirty and cold.

"This is going to take forever," Liam said.

"Yes," Thomas replied, still planting beside him.

"And you won't see anything for months."

Liam paused.

"Then why do it?"

Thomas looked at him.

"Because garlic planted in winter grows strong roots," he said.

"Roots you can't see."

"By spring, it will push through the ground."

"By summer, it will be ready to harvest."

"But none of that happens without this moment."

"Right now."

"In the cold."

They kept planting.

Clove after clove.

Row after row.

Liam's fingers were numb, but he didn't stop.

There was something calming about the rhythm.

Press the soil.

Place the clove.

Cover it gently.

Move to the next spot.

When they finished, Thomas sat back.

"Now we wait," he said.

Liam looked at the dirt.

It looked empty.

"I don't see anything," Liam said.

"Not yet," Thomas agreed.

"But something is happening."

"Under the surface."

"You just can't see it."

They sat together in the quiet garden.

Then Thomas spoke again.

"You told me you feel stuck," he said.

"You're waiting for something to change."

Liam nodded.

"But change doesn't announce itself," Thomas said.

"It starts small."

"Invisible."

"Like a root in winter."

He gestured to the rows they had just planted.

"You don't wait for the garlic to grow," Thomas continued.

"You plant it."

"You do the work even when you can't see the result."

"And then, quietly, it grows."

Liam stared at the ground.

"So I'm supposed to just... do things?" he asked.

"Even if I don't know if they'll work?"

"Yes," Thomas said simply.

"Take one small step."

"Then another."

"Not because you see the whole path."

"But because that's how anything grows."

Liam felt something shift inside him.

He thought about all the things he'd started and stopped.

All the plans he'd abandoned because they didn't show results fast enough.

"I've been waiting for proof before I begin," Liam said quietly.

Thomas nodded.

"Most people do."

"But the proof comes after."

"Never before."

Liam left the garden that day with dirt under his nails.

That week, he signed up for a class he'd been considering for months.

He didn't know if it would lead anywhere.

But he went anyway.

He started writing again, just fifteen minutes each morning.

Not because he had a plan for it.

But because it felt like planting something.

He reached out to an old friend.

He applied for a job that scared him.

Each action was small.

None of them promised anything.

But he did them anyway.

Winter turned to spring.

One morning, Liam walked past the garden again.

He saw tiny green shoots pushing through the soil.

The garlic was growing.

Thomas was there, watering the rows.

"It worked," Liam said, smiling.

"It always does," Thomas replied.

"If you plant it."

Liam thought about his own life.

The small steps he'd been taking.

Some had led somewhere.

Some hadn't.

But he didn't feel stuck anymore.

He felt like he was growing.

Slowly.

Quietly.

But growing.

He stood beside Thomas in the spring sunlight.

"Thank you," Liam said.

Thomas handed him a watering can.

"Keep planting," he said.

And Liam did.

Not because he could see the future.

But because he finally understood.

Growth happens in the doing.

Not in the waiting.
"""

VISUAL_PLAN = {
    "characters": [
        {
            "name": "Maya",
            "age": 28,
            "gender": "female",
            "physical_appearance": "South Asian woman with shoulder-length dark brown hair, warm brown eyes, medium brown skin tone, gentle facial features, slender build, approximately 5'6\" tall",
            "clothing_style": "Simple modern casual wear - light colored linen shirt, dark comfortable pants, minimal jewelry, worn leather sandals",
            "overall_vibe": "Thoughtful, gentle, tired but kind, carries visible tension in her shoulders",
            "master_visual_prompt": "Cinematic portrait of a 28-year-old South Asian woman with shoulder-length dark brown hair and warm brown eyes, medium brown skin, gentle tired expression, wearing simple light linen clothing, soft natural lighting, 50mm lens, realistic film photography"
        },
        {
            "name": "Elena",
            "age": 72,
            "gender": "female",
            "physical_appearance": "Elderly woman with silver-gray hair pulled back in a low bun, warm smile lines around her eyes, light olive skin, weathered hands, petite frame, approximately 5'3\" tall, calm presence",
            "clothing_style": "Traditional simple clothing - long earth-toned skirt, loose cotton blouse, hand-knitted shawl around shoulders, comfortable worn shoes",
            "overall_vibe": "Wise, peaceful, gentle, grounded, radiates calm and patience",
            "master_visual_prompt": "Cinematic portrait of a 72-year-old woman with silver-gray hair in a low bun, warm wrinkled face with kind eyes, light olive skin, wearing earth-toned traditional simple clothing, peaceful expression, soft natural lighting, 50mm lens, realistic film photography"
        }
    ],
    "environment": {
        "location_type": "Small hillside village with traditional cottages",
        "cultural_setting": "Mediterranean or Southern European inspired village",
        "season": "Late spring or early summer",
        "weather_style": "Warm, gentle sunlight, clear skies, occasional soft clouds",
        "architecture_style": "Simple stone and whitewashed cottages, wooden details, terracotta roofs, cobblestone paths",
        "natural_elements": "Rolling hills in background, olive trees, wild grasses, small gardens with vegetables and flowers, scattered wildflowers",
        "overall_atmosphere": "Peaceful, timeless, sun-drenched, quiet rural beauty, warm and welcoming"
    },
    "visual_style": {
        "photography_style": "Cinematic film still, natural documentary style",
        "camera_lens": "35mm and 50mm prime lenses",
        "lighting_style": "Soft natural daylight, golden hour warmth, gentle shadows, no harsh contrasts",
        "color_grading": "Warm earth tones, muted pastels, soft greens and browns, gentle golden highlights, slightly desaturated for calm mood",
        "realism_level": "Photorealistic, natural, grounded in reality",
        "rendering_quality": "High detail, film grain texture, shallow depth of field, professional cinematography, 4K quality"
    },
    "scenes": [
        {
            "scene_number": 1,
            "short_title": "Maya waking up worried",
            "visual_description": "Maya lying in bed, eyes open staring at ceiling, morning light streaming through simple window, hand on forehead, rumpled bedsheets, small modest bedroom with minimal furniture",
            "main_characters_in_scene": ["Maya"],
            "camera_shot_type": "Medium close-up",
            "camera_angle": "Slightly high angle looking down at bed",
            "time_of_day": "Early morning",
            "emotional_tone": "Restless, tense, troubled",
            "key_objects": ["bed", "window", "morning light", "simple wooden furniture"]
        },
        {
            "scene_number": 2,
            "short_title": "Maya walking through village",
            "visual_description": "Maya walking alone on cobblestone path between whitewashed buildings, head slightly down, arms wrapped around herself, village market stalls in soft focus background, other villagers going about their day",
            "main_characters_in_scene": ["Maya"],
            "camera_shot_type": "Full body shot",
            "camera_angle": "Eye level, following from side",
            "time_of_day": "Mid-morning",
            "emotional_tone": "Isolated, burdened, distant",
            "key_objects": ["cobblestone path", "village buildings", "market stalls", "stone walls"]
        },
        {
            "scene_number": 3,
            "short_title": "Maya lying awake at night",
            "visual_description": "Maya in bed at night, moonlight through window, eyes wide open, hands clasped on chest, dark room with shadows, visible tension in her face",
            "main_characters_in_scene": ["Maya"],
            "camera_shot_type": "Close-up on face",
            "camera_angle": "Eye level from bedside",
            "time_of_day": "Night",
            "emotional_tone": "Sleepless, anxious, exhausted",
            "key_objects": ["bed", "window with moonlight", "pillow", "shadows"]
        },
        {
            "scene_number": 4,
            "short_title": "Elena's cottage exterior",
            "visual_description": "Small stone cottage at village edge with wooden door, small garden with vegetables and flowers, wooden bench outside, hills visible in background, warm afternoon sunlight, peaceful setting",
            "main_characters_in_scene": [],
            "camera_shot_type": "Wide establishing shot",
            "camera_angle": "Eye level",
            "time_of_day": "Afternoon",
            "emotional_tone": "Peaceful, inviting, warm",
            "key_objects": ["stone cottage", "wooden bench", "garden", "flowers", "hills"]
        },
        {
            "scene_number": 5,
            "short_title": "Elena shelling peas",
            "visual_description": "Elena sitting on wooden bench outside cottage, wooden bowl in lap, hands shelling peas, peaceful expression, garden visible beside her, dappled sunlight through nearby tree",
            "main_characters_in_scene": ["Elena"],
            "camera_shot_type": "Medium shot",
            "camera_angle": "Slightly low angle",
            "time_of_day": "Afternoon",
            "emotional_tone": "Serene, centered, calm",
            "key_objects": ["wooden bench", "bowl of peas", "garden", "cottage wall", "tree"]
        },
        {
            "scene_number": 6,
            "short_title": "Maya and Elena talking",
            "visual_description": "Maya and Elena sitting together on bench, facing each other, Maya leaning forward with worried expression, Elena listening with calm attentive face, cottage wall behind them, afternoon light",
            "main_characters_in_scene": ["Maya", "Elena"],
            "camera_shot_type": "Two-shot medium",
            "camera_angle": "Eye level",
            "time_of_day": "Afternoon",
            "emotional_tone": "Intimate, vulnerable, supportive",
            "key_objects": ["wooden bench", "cottage wall", "bowl of peas set aside"]
        },
        {
            "scene_number": 7,
            "short_title": "Elena giving Maya the bag",
            "visual_description": "Elena standing, handing large cloth bag to Maya who is receiving it with both hands, bag appears heavy, stones visible through opening, cottage doorway in background, both women in full view",
            "main_characters_in_scene": ["Maya", "Elena"],
            "camera_shot_type": "Full body medium shot",
            "camera_angle": "Eye level",
            "time_of_day": "Late afternoon",
            "emotional_tone": "Curious, solemn, beginning of task",
            "key_objects": ["cloth bag", "river stones", "cottage doorway", "Elena's garden"]
        },
        {
            "scene_number": 8,
            "short_title": "Maya carrying the heavy bag",
            "visual_description": "Maya walking on village path, large bag on shoulder, body leaning under weight, strained expression, one hand supporting bag, cobblestone path ahead, hills in background, late afternoon sun",
            "main_characters_in_scene": ["Maya"],
            "camera_shot_type": "Full body shot",
            "camera_angle": "Slightly low angle from front",
            "time_of_day": "Late afternoon",
            "emotional_tone": "Struggling, burdened, determined",
            "key_objects": ["heavy cloth bag", "stones", "cobblestone path", "village buildings"]
        },
        {
            "scene_number": 9,
            "short_title": "Maya resting exhausted",
            "visual_description": "Maya stopped on path, sitting on low stone wall, bag set down beside her, rubbing her shoulder, face showing pain and exhaustion, village path continues ahead, golden hour light",
            "main_characters_in_scene": ["Maya"],
            "camera_shot_type": "Medium shot",
            "camera_angle": "Eye level",
            "time_of_day": "Golden hour",
            "emotional_tone": "Exhausted, hurting, overwhelmed",
            "key_objects": ["stone wall", "heavy bag", "cobblestone path", "village in background"]
        },
        {
            "scene_number": 10,
            "short_title": "Elena explaining the lesson",
            "visual_description": "Elena and Maya sitting close on bench, Elena holding Maya's hand gently, speaking with kind expression, Maya listening with tears in eyes, morning light, cottage garden blooming beside them",
            "main_characters_in_scene": ["Maya", "Elena"],
            "camera_shot_type": "Close two-shot",
            "camera_angle": "Slightly low angle, intimate",
            "time_of_day": "Morning",
            "emotional_tone": "Tender, revelation, emotional breakthrough",
            "key_objects": ["wooden bench", "Elena's hand holding Maya's", "garden flowers", "cottage wall"]
        },
        {
            "scene_number": 11,
            "short_title": "Maya practicing releasing worry",
            "visual_description": "Maya standing alone on hillside path overlooking village, eyes closed, hands open at sides in releasing gesture, peaceful expression, gentle breeze moving her hair, wildflowers around her, warm afternoon light",
            "main_characters_in_scene": ["Maya"],
            "camera_shot_type": "Full body shot",
            "camera_angle": "Eye level from side",
            "time_of_day": "Afternoon",
            "emotional_tone": "Peaceful, practicing, lighter",
            "key_objects": ["hillside path", "wildflowers", "village below", "open sky"]
        },
        {
            "scene_number": 12,
            "short_title": "Maya and Elena at sunset",
            "visual_description": "Maya and Elena sitting together on bench outside cottage, side by side looking at sunset, pink and gold sky, peaceful silence between them, Maya's posture relaxed, Elena's hand near Maya's, garden silhouetted, tranquil ending",
            "main_characters_in_scene": ["Maya", "Elena"],
            "camera_shot_type": "Wide shot from behind",
            "camera_angle": "Eye level, viewing from back",
            "time_of_day": "Sunset",
            "emotional_tone": "Peaceful, resolved, companionable, hopeful",
            "key_objects": ["wooden bench", "cottage", "garden", "sunset sky", "hills in distance"]
        }
    ]
}
