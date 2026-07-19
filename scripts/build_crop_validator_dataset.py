import os
import glob
import shutil
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))

DATASET_ROOT = os.path.join(PROJECT_ROOT, "data", "crop_validator_dataset")
LETTUCE_DIR = os.path.join(DATASET_ROOT, "lettuce_leaf")
OTHER_PLANT_DIR = os.path.join(DATASET_ROOT, "other_plant_leaf")
NON_LEAF_DIR = os.path.join(DATASET_ROOT, "non_leaf")

def build_crop_validator_dataset(target_per_class=1000):
    print("=" * 60)
    print("PART 3: BUILDING 3-CLASS CROP VALIDATOR DATASET (3,000+ IMAGES)")
    print("=" * 60)

    for d in [LETTUCE_DIR, OTHER_PLANT_DIR, NON_LEAF_DIR]:
        os.makedirs(d, exist_ok=True)

    # 1. Collect 1,000+ Lettuce Leaf Images
    print("1/3 Collecting real lettuce leaf images...")
    growth_imgs = glob.glob(os.path.join(PROJECT_ROOT, "data", "growth_dataset", "**", "*.png"), recursive=True)
    nutrient_imgs = glob.glob(os.path.join(PROJECT_ROOT, "data", "nutrient_dataset", "**", "*.*"), recursive=True)
    
    all_lettuce = [p for p in growth_imgs + nutrient_imgs if os.path.splitext(p)[1].lower() in ['.png', '.jpg', '.jpeg']]
    random.seed(42)
    selected_lettuce = random.sample(all_lettuce, min(target_per_class, len(all_lettuce)))

    for idx, src in enumerate(selected_lettuce):
        ext = os.path.splitext(src)[1].lower()
        dst = os.path.join(LETTUCE_DIR, f"lettuce_{idx:04d}{ext}")
        try:
            with Image.open(src) as img:
                img.verify()
            shutil.copy(src, dst)
        except Exception:
            continue
            
    print(f"   Collected {len(os.listdir(LETTUCE_DIR))} valid lettuce_leaf images.")

    # 2. Generate/Collect 1,000+ Other Plant Leaf Images (Tomato, Potato, Spinach, Basil, Mango)
    print("2/3 Generating 1,000+ non-lettuce plant leaf images (Tomato, Potato, Spinach, Basil, Mango)...")
    plant_types = ['tomato', 'potato', 'spinach', 'basil', 'mango']
    
    for i in range(target_per_class):
        ptype = plant_types[i % len(plant_types)]
        img = Image.new('RGB', (224, 224), color=(random.randint(180, 220), random.randint(160, 200), random.randint(120, 160))) # Soil/pot background
        draw = ImageDraw.Draw(img)
        
        if ptype == 'tomato':
            # Dark serrated compound leaf shape
            leaf_color = (random.randint(20, 60), random.randint(90, 140), random.randint(20, 50))
            draw.polygon([(112, 30), (70, 80), (50, 120), (90, 140), (112, 190), (134, 140), (174, 120), (154, 80)], fill=leaf_color)
            draw.line([(112, 30), (112, 190)], fill=(random.randint(70, 110), 160, 70), width=3)
        elif ptype == 'potato':
            # Oval dark green textured leaf
            leaf_color = (random.randint(10, 50), random.randint(80, 120), random.randint(15, 40))
            draw.ellipse([(40, 30), (184, 194)], fill=leaf_color)
            draw.line([(112, 30), (112, 194)], fill=(40, 140, 50), width=4)
        elif ptype == 'spinach':
            # Arrowhead/triangular smooth leaf
            leaf_color = (random.randint(30, 70), random.randint(120, 170), random.randint(30, 60))
            draw.polygon([(112, 20), (30, 160), (90, 150), (112, 200), (134, 150), (194, 160)], fill=leaf_color)
        elif ptype == 'basil':
            # Small rounded cupped glossy leaf
            leaf_color = (random.randint(40, 80), random.randint(140, 190), random.randint(40, 70))
            draw.ellipse([(50, 40), (174, 184)], fill=leaf_color)
            draw.line([(112, 40), (112, 184)], fill=(100, 200, 100), width=2)
        else: # Mango
            # Narrow elongated lanceolate leaf
            leaf_color = (random.randint(20, 50), random.randint(70, 110), random.randint(20, 40))
            draw.polygon([(112, 10), (80, 112), (112, 214), (144, 112)], fill=leaf_color)
            draw.line([(112, 10), (112, 214)], fill=(120, 150, 80), width=3)

        # Random angle rotation and noise
        angle = random.randint(0, 360)
        img = img.rotate(angle)
        
        dst_path = os.path.join(OTHER_PLANT_DIR, f"other_plant_{i:04d}.png")
        img.save(dst_path)

    print(f"   Generated {len(os.listdir(OTHER_PLANT_DIR))} valid other_plant_leaf images.")

    # 3. Generate/Collect 1,000+ Non-Leaf Images (Documents, Screenshots, Objects, Humans, Soil)
    print("3/3 Generating 1,000+ non-leaf images (Documents, Screenshots, Objects, Humans, Soil)...")
    non_leaf_categories = ['document', 'screenshot', 'object', 'human', 'animal', 'soil', 'background']
    
    for i in range(target_per_class):
        cat = non_leaf_categories[i % len(non_leaf_categories)]
        img = Image.new('RGB', (224, 224), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        if cat == 'document':
            for y in range(15, 210, 12):
                l_len = random.randint(80, 190)
                draw.line([(20, y), (20 + l_len, y)], fill=(30, 30, 30), width=2)
            draw.rectangle([(20, 10), (90, 18)], fill=(0, 50, 150))
        elif cat == 'screenshot':
            img = Image.new('RGB', (224, 224), color=(15, 23, 42)) # Dark theme UI
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (224, 30)], fill=(30, 41, 59)) # Header bar
            draw.rectangle([(20, 50), (100, 110)], fill=(51, 65, 85)) # Code block
            draw.rectangle([(120, 50), (204, 110)], fill=(16, 185, 129)) # Button
        elif cat == 'object':
            c = (random.randint(180, 240), random.randint(50, 100), random.randint(50, 100))
            img = Image.new('RGB', (224, 224), color=(230, 230, 230))
            draw = ImageDraw.Draw(img)
            draw.rectangle([(40, 40), (184, 184)], fill=c)
            draw.ellipse([(60, 60), (164, 164)], fill=(50, 50, 50))
        elif cat == 'human':
            img = Image.new('RGB', (224, 224), color=(240, 220, 200)) # Skin tone
            draw = ImageDraw.Draw(img)
            draw.ellipse([(60, 30), (164, 150)], fill=(220, 180, 150)) # Face contour
            draw.ellipse([(80, 70), (100, 90)], fill=(50, 30, 20)) # Eye 1
            draw.ellipse([(124, 70), (144, 90)], fill=(50, 30, 20)) # Eye 2
            draw.line([(90, 120), (134, 120)], fill=(180, 80, 80), width=4) # Mouth
        elif cat == 'animal':
            # Fur texture pattern
            arr = np.random.randint(80, 160, (224, 224, 3), dtype=np.uint8)
            img = Image.fromarray(arr).filter(ImageFilter.BLUR)
        elif cat == 'soil':
            # Brown soil texture
            arr = np.random.randint(40, 90, (224, 224, 3), dtype=np.uint8)
            arr[:, :, 0] += 40 # Add brown tint
            img = Image.fromarray(arr)
        else: # Random background / indoor noise
            arr = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
            img = Image.fromarray(arr)

        dst_path = os.path.join(NON_LEAF_DIR, f"non_leaf_{i:04d}.png")
        img.save(dst_path)

    print(f"   Generated {len(os.listdir(NON_LEAF_DIR))} valid non_leaf images.")
    print("\nDataset Build Summary:")
    print(f"  - lettuce_leaf:       {len(os.listdir(LETTUCE_DIR))} images")
    print(f"  - other_plant_leaf:   {len(os.listdir(OTHER_PLANT_DIR))} images")
    print(f"  - non_leaf:           {len(os.listdir(NON_LEAF_DIR))} images")
    print(f"  - Total Dataset Size: {len(os.listdir(LETTUCE_DIR)) + len(os.listdir(OTHER_PLANT_DIR)) + len(os.listdir(NON_LEAF_DIR))} images")

if __name__ == '__main__':
    build_crop_validator_dataset()
