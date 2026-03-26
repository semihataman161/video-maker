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
            "name": "Liam",
            "age": 28,
            "gender": "male",
            "physical_appearance": "Caucasian man in his late twenties with short brown hair, light stubble, hazel eyes, average build, approximately 5'10\" tall, slightly tired expression",
            "clothing_style": "casual modern winter clothing - dark gray jacket, jeans, brown boots, simple knit beanie, neutral earth tones",
            "overall_vibe": "restless, searching, gentle, introspective",
            "master_visual_prompt": "anime style portrait of a 28-year-old Caucasian man with short brown hair and light stubble, hazel eyes, wearing a dark gray winter jacket, soft lighting, illustrative, clean lines, (Ghibli style:0.8)"
        },
        {
            "name": "Thomas",
            "age": 72,
            "gender": "male",
            "physical_appearance": "elderly Caucasian man with white hair, weathered kind face, deep smile lines, blue-gray eyes, lean build, approximately 5'8\" tall, gentle warm expression",
            "clothing_style": "practical gardening clothes - tan work jacket, flannel shirt, worn brown pants, gardening gloves tucked in pocket, earth-toned colors",
            "overall_vibe": "wise, calm, patient, grounded, warm",
            "master_visual_prompt": "anime style portrait of a 72-year-old Caucasian man with white hair and weathered kind face, blue-gray eyes, wearing a tan work jacket over flannel shirt, soft natural lighting, illustrative, (Ghibli style:0.8)"
        }
    ],
    "environment": {
        "location_type": "small mountain town with community garden",
        "cultural_setting": "rural North America, close-knit community",
        "season": "winter transitioning to early spring",
        "weather_style": "cold, overcast skies, occasional soft sunlight, crisp air",
        "architecture_style": "modest small-town buildings, wooden fences, simple structures",
        "natural_elements": "mountain backdrop, bare trees, cold soil, patches of grass, stone paths",
        "overall_cinematic_atmosphere": "quiet, peaceful, slightly melancholic winter beauty, natural muted colors, calm stillness"
    },
    "visual_style": {
        "photography_style": "anime illustration, Ghibli inspired",
        "camera_lens_type": "35mm and 50mm equivalent",
        "lighting_style": "soft diffused daylight, painterly shadows, overcast winter light, golden hour for spring scenes",
        "color_grading": "vibrant yet natural colors, cool blues and grays for winter, warm greens and golds for spring, muted palette",
        "realism_level": "stylized anime, illustrative",
        "rendering_quality_keywords": "masterpiece, high quality, highres, detailed background, clean lines"
    },
    "scenes": [
        {
            "scene_number": 1,
            "short_title": "Liam walking through empty street",
            "visual_description": "A young man walks alone down a quiet small-town street lined with modest buildings, hands in jacket pockets, head slightly down, empty sidewalk, overcast winter sky",
            "main_characters_in_scene": ["Liam"],
            "camera_shot_type": "wide shot",
            "camera_angle": "eye-level, slightly behind",
            "time_of_day": "late afternoon, winter",
            "emotional_tone": "isolated, quiet, contemplative",
            "key_objects": ["street, buildings, bare trees, empty sidewalk"]
        },
        {
            "scene_number": 2,
            "short_title": "Liam at coffee shop window",
            "visual_description": "A man sits alone at a small table by a coffee shop window, looking down at his phone, untouched coffee cup beside him, soft interior lighting, cold street visible through glass",
            "main_characters_in_scene": ["Liam"],
            "camera_shot_type": "medium shot",
            "camera_angle": "eye-level from outside looking in",
            "time_of_day": "afternoon",
            "emotional_tone": "distracted, disconnected, waiting",
            "key_objects": ["coffee cup, phone, window, table, street outside"]
        },
        {
            "scene_number": 3,
            "short_title": "First glimpse of Thomas in garden",
            "visual_description": "An elderly man kneels in a winter community garden plot, working with soil, wooden garden beds visible, bare ground, simple tools nearby, mountain backdrop in distance",
            "main_characters_in_scene": ["Thomas"],
            "camera_shot_type": "wide shot",
            "camera_angle": "slightly high angle",
            "time_of_day": "cold afternoon",
            "emotional_tone": "peaceful, focused, purposeful",
            "key_objects": ["garden beds, soil, gardening tools, fence, mountains"]
        },
        {
            "scene_number": 4,
            "short_title": "Liam approaches Thomas",
            "visual_description": "A young man stands at the edge of a garden looking at an elderly man who is kneeling and working, wooden fence between them, winter landscape, both figures clearly visible",
            "main_characters_in_scene": ["Liam", "Thomas"],
            "camera_shot_type": "medium wide shot",
            "camera_angle": "eye-level",
            "time_of_day": "afternoon",
            "emotional_tone": "curious, tentative, calm",
            "key_objects": ["garden fence, soil, pathway, bare trees"]
        },
        {
            "scene_number": 5,
            "short_title": "Conversation at garden edge",
            "visual_description": "Two men standing near a garden plot talking, the younger man with hands in pockets, the older man holding gardening gloves, cold breath visible in air, natural body language of conversation",
            "main_characters_in_scene": ["Liam", "Thomas"],
            "camera_shot_type": "medium shot",
            "camera_angle": "eye-level",
            "time_of_day": "late afternoon",
            "emotional_tone": "open, honest, gentle",
            "key_objects": ["garden plot, gloves, fence posts, cold ground"]
        },
        {
            "scene_number": 6,
            "short_title": "Thomas hands garlic to Liam",
            "visual_description": "Close view of an elderly weathered hand passing a small cloth bag to a younger hand, garlic cloves visible inside bag, natural outdoor lighting, dirt on both sets of hands",
            "main_characters_in_scene": ["Liam", "Thomas"],
            "camera_shot_type": "close-up",
            "camera_angle": "slightly high angle looking down at hands",
            "time_of_day": "afternoon",
            "emotional_tone": "gentle, instructive, connected",
            "key_objects": ["cloth bag, garlic cloves, hands, soil"]
        },
        {
            "scene_number": 7,
            "short_title": "Both men kneeling planting",
            "visual_description": "Two men kneel side by side in garden soil, both pressing garlic cloves into cold ground, rows of small holes visible, garden tools nearby, winter light casting soft shadows",
            "main_characters_in_scene": ["Liam", "Thomas"],
            "camera_shot_type": "wide shot",
            "camera_angle": "slightly high angle",
            "time_of_day": "afternoon",
            "emotional_tone": "peaceful, meditative, working together",
            "key_objects": ["soil, garlic cloves, garden rows, tools, wooden beds"]
        },
        {
            "scene_number": 8,
            "short_title": "Liam's hands in cold soil",
            "visual_description": "Close view of young hands with dirt under fingernails pressing a garlic clove into dark soil, fingers slightly red from cold, texture of earth clearly visible, shallow planting hole",
            "main_characters_in_scene": ["Liam"],
            "camera_shot_type": "extreme close-up",
            "camera_angle": "slightly high angle",
            "time_of_day": "afternoon",
            "emotional_tone": "focused, tactile, present",
            "key_objects": ["hands, soil, garlic clove, earth texture"]
        },
        {
            "scene_number": 9,
            "short_title": "Thomas and Liam sitting in garden",
            "visual_description": "Two men sit on the edge of a raised garden bed, elderly man gesturing gently while speaking, younger man listening intently, empty planted rows visible behind them, mountains in background",
            "main_characters_in_scene": ["Liam", "Thomas"],
            "camera_shot_type": "medium shot",
            "camera_angle": "eye-level",
            "time_of_day": "late afternoon, golden light",
            "emotional_tone": "wise, contemplative, understanding",
            "key_objects": ["garden bed, planted rows, mountains, bare trees"]
        },
        {
            "scene_number": 10,
            "short_title": "Liam looking at empty soil",
            "visual_description": "A young man crouches alone looking down at freshly planted garden rows, bare soil with no visible growth, hands resting on knees, contemplative posture, soft winter light",
            "main_characters_in_scene": ["Liam"],
            "camera_shot_type": "medium shot",
            "camera_angle": "slightly high angle",
            "time_of_day": "late afternoon",
            "emotional_tone": "thoughtful, absorbing, quiet realization",
            "key_objects": ["planted soil, garden rows, dirt, wooden bed frames"]
        },
        {
            "scene_number": 11,
            "short_title": "Spring garden with green shoots",
            "visual_description": "Garden rows now showing tiny bright green garlic shoots pushing through dark soil, early spring light, small signs of new growth visible across planted area, wooden garden beds weathered but same",
            "main_characters_in_scene": [],
            "camera_shot_type": "close-up transitioning to medium",
            "camera_angle": "low angle close to ground level",
            "time_of_day": "morning, spring",
            "emotional_tone": "hopeful, renewed, alive",
            "key_objects": ["green shoots, soil, garden rows, morning dew"]
        },
        {
            "scene_number": 12,
            "short_title": "Liam and Thomas in spring garden",
            "visual_description": "Two men stand together in a garden now showing green growth, younger man holding a watering can, both looking at the growing plants, warm spring sunlight, gentle smiles, peaceful companionship",
            "main_characters_in_scene": ["Liam", "Thomas"],
            "camera_shot_type": "medium wide shot",
            "camera_angle": "eye-level",
            "time_of_day": "morning, spring",
            "emotional_tone": "peaceful, content, connected, hopeful",
            "key_objects": ["watering can, green plants, garden beds, spring foliage, soft sunlight"]
        }
    ]
}
