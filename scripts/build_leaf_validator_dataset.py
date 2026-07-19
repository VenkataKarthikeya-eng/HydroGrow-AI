import os
import glob
import shutil
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))

DATASET_ROOT = os.path.join(PROJECT_ROOT, "data", "leaf_validator_dataset")
LEAF_DIR = os.path.join(DATASET_ROOT, "lettuce_leaf")
NON_LEAF_DIR = os.path.join(DATASET_ROOT, "non_leaf")

def build_dataset(samples_per_class=200):
    print("=" * 60)
    print("STEP 1: BUILDING LEAF VALIDATOR DATASET")
    print("=" * 60)

    os.makedirs(LEAF_DIR, exist_ok=True)
    os.makedirs(NON_LEAF_DIR, exist_ok=True)

    # 1. Collect Lettuce Leaf Images from nutrient_dataset and growth_dataset
    nutrient_imgs = glob.glob(os.path.join(PROJECT_ROOT, "data", "nutrient_dataset", "**", "*.*"), recursive=True)
    growth_imgs = glob.glob(os.path.join(PROJECT_ROOT, "data", "growth_dataset", "**", "*.png"), recursive=True)
    
    all_leaf_imgs = [p for p in nutrient_imgs + growth_imgs if os.path.splitext(p)[1].lower() in ['.png', '.jpg', '.jpeg']]
    random.seed(42)
    selected_leafs = random.sample(all_leaf_imgs, min(samples_per_class, len(all_leaf_imgs)))

    print(f"Sampling {len(selected_leafs)} real lettuce leaf images...")
    for idx, src in enumerate(selected_leafs):
        ext = os.path.splitext(src)[1].lower()
        dst = os.path.join(LEAF_DIR, f"lettuce_{idx:03d}{ext}")
        shutil.copy(src, dst)

    # 2. Generate/Collect Non-Leaf Images (documents, text, geometric noise, patterns)
    print(f"Generating {samples_per_class} non-leaf training images (documents, text, textures, non-plant patterns)...")
    
    for i in range(samples_per_class):
        img_type = i % 5
        img = Image.new('RGB', (224, 224), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        if img_type == 0: # Document / Text page
            for y in range(20, 200, 15):
                line_len = random.randint(100, 180)
                draw.line([(20, y), (20 + line_len, y)], fill=(40, 40, 40), width=3)
            # Add header text box
            draw.rectangle([(20, 10), (100, 18)], fill=(0, 0, 0))

        elif img_type == 1: # Geometric grid / technical blueprint
            img = Image.new('RGB', (224, 224), color=(30, 40, 60))
            draw = ImageDraw.Draw(img)
            for x in range(0, 224, 20):
                draw.line([(x, 0), (x, 224)], fill=(70, 100, 140), width=1)
            for y in range(0, 224, 20):
                draw.line([(0, y), (224, y)], fill=(70, 100, 140), width=1)
            draw.rectangle([(50, 50), (170, 170)], outline=(200, 220, 255), width=2)

        elif img_type == 2: # Red / Blue / Metal Appliance Texture
            c1 = (random.randint(150, 255), random.randint(20, 80), random.randint(20, 80))
            img = Image.new('RGB', (224, 224), color=c1)
            draw = ImageDraw.Draw(img)
            draw.ellipse([(30, 30), (190, 190)], fill=(random.randint(50, 100), 50, 50))

        elif img_type == 3: # Noise / Random Pixel Texture
            arr = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
            img = Image.fromarray(arr)

        else: # Wood / Brick / Checkerboard pattern
            c1 = (random.randint(180, 220), random.randint(120, 150), random.randint(80, 100))
            img = Image.new('RGB', (224, 224), color=c1)
            draw = ImageDraw.Draw(img)
            for x in range(0, 224, 32):
                for y in range(0, 224, 32):
                    if (x // 32 + y // 32) % 2 == 0:
                        draw.rectangle([(x, y), (x + 32, y + 32)], fill=(120, 80, 50))

        dst_path = os.path.join(NON_LEAF_DIR, f"non_leaf_{i:03d}.png")
        img.save(dst_path)

    print(f"\nDataset build complete!")
    print(f"  - Lettuce Leaf Images: {len(os.listdir(LEAF_DIR))}")
    print(f"  - Non-Leaf Images: {len(os.listdir(NON_LEAF_DIR))}")

if __name__ == '__main__':
    build_dataset()
