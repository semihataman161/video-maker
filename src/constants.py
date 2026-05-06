CHUNKS = """
[1] Liam was twenty-eight years old. He lived in a small mountain town where everyone knew each other.
[2] For the past year, he had felt stuck. He wanted his life to change. He wanted a better job, a relationship, a fresh start. But nothing seemed to move forward. Every day felt the same. This feeling made him restless.
[3] He would start projects and abandon them. He would make plans and give up halfway. He kept waiting for something big to happen. Some sign that would tell him what to do. But the sign never came.
[4] At the grocery store, he sighed. At the coffee shop, he scrolled through his phone, searching. He watched other people and wondered why their lives seemed to work. His own felt frozen in place.
[5] One cold afternoon, Liam walked past the community garden. An old man was working there alone. His name was Thomas. Thomas had lived in the town his whole life. He used to run the hardware store until he retired. Now he spent most of his time in the garden. People said he could grow anything. Even in the hardest seasons, something in his plot was alive.
[6] Liam had walked past the garden a hundred times. But today, he stopped. Thomas was kneeling in the dirt, even though it was winter.
[7] "What are you planting?" Liam asked. Thomas looked up and smiled. "Garlic," he said. "In winter?" Liam asked. "It seems like the wrong time." "It's exactly the right time," Thomas replied.
[8] They talked for a few minutes. Something about Thomas made Liam feel comfortable. Before he knew it, Liam was speaking honestly. "I feel stuck," Liam said. "I keep waiting for my life to change, but nothing happens."
[9] Thomas brushed the dirt from his hands. "Do you have a few hours?" he asked. "Yes," Liam said. "Then help me plant," Thomas said. "It might teach you something."
[10] Liam agreed, though he wasn't sure why. Thomas handed him a small bag of garlic cloves. "We're going to plant these," Thomas said. "Each one goes in the ground, pointed side up." "About two inches deep." "Six inches apart."
[11] Liam knelt down and began. The ground was cold and hard. He had to press firmly to make each hole. It was slow work. After ten cloves, his hands were dirty and cold.
[12] "This is going to take forever," Liam said. "Yes," Thomas replied, still planting beside him. "And you won't see anything for months."
[13] Liam paused. "Then why do it?" Thomas looked at him. "Because garlic planted in winter grows strong roots," he said. "Roots you can't see." "By spring, it will push through the ground." "By summer, it will be ready to harvest." "But none of that happens without this moment." "Right now." "In the cold."
[14] They kept planting. Clove after clove. Row after row. Liam's fingers were numb, but he didn't stop. There was something calming about the rhythm. Press the soil. Place the clove. Cover it gently. Move to the next spot.
[15] When they finished, Thomas sat back. "Now we wait," he said. Liam looked at the dirt. It looked empty. "I don't see anything," Liam said. "Not yet," Thomas agreed. "But something is happening." "Under the surface." "You just can't see it."
[16] They sat together in the quiet garden. Then Thomas spoke again. "You told me you feel stuck," he said. "You're waiting for something to change." Liam nodded.
[17] "But change doesn't announce itself," Thomas said. "It starts small." "Invisible." "Like a root in winter." He gestured to the rows they had just planted.
[18] "You don't wait for the garlic to grow," Thomas continued. "You plant it." "You do the work even when you can't see the result." "And then, quietly, it grows."
[19] Liam stared at the ground. "So I'm supposed to just... do things?" he asked. "Even if I don't know if they'll work?" "Yes," Thomas said simply. "Take one small step." "Then another." "Not because you see the whole path." "But because that's how anything grows."
[20] Liam felt something shift inside him. He thought about all the things he'd started and stopped. All the plans he'd abandoned because they didn't show results fast enough. "I've been waiting for proof before I begin," Liam said quietly. Thomas nodded. "Most people do." "But the proof comes after." "Never before."
[21] Liam left the garden that day with dirt under his nails.
[22] That week, he signed up for a class he'd been considering for months. He didn't know if it would lead anywhere. But he went anyway.
[23] He started writing again, just fifteen minutes each morning. Not because he had a plan for it. But because it felt like planting something.
[24] He reached out to an old friend. He applied for a job that scared him. Each action was small. None of them promised anything. But he did them anyway.
[25] Winter turned to spring. One morning, Liam walked past the garden again. He saw tiny green shoots pushing through the soil. The garlic was growing.
[26] Thomas was there, watering the rows. "It worked," Liam said, smiling. "It always does," Thomas replied. "If you plant it."
[27] Liam thought about his own life. The small steps he'd been taking. Some had led somewhere. Some hadn't. But he didn't feel stuck anymore. He felt like he was growing.
[28] Slowly. Quietly. But growing.
[29] He stood beside Thomas in the spring sunlight. "Thank you," Liam said. Thomas handed him a watering can. "Keep planting," he said.
[30] And Liam did. Not because he could see the future. But because he finally understood. Growth happens in the doing. Not in the waiting.
"""

TARGET_IMAGE_SIZE = (1920, 1080)

from pathlib import Path

# ASSETS DIRECTORIES
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"

# OUTPUT DIRECTORIES
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
AUDIO_DIR = OUTPUT_DIR / "audio"
IMAGES_DIR = OUTPUT_DIR / "images"
ORIGINAL_IMAGES_DIR = IMAGES_DIR / "original"
CROPPED_IMAGES_DIR = IMAGES_DIR / "cropped"
