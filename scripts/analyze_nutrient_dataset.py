import os
import glob
from PIL import Image
import pandas as pd

def analyze_dataset(dataset_dir="data/nutrient_dataset"):
    print("=" * 60)
    print("STEP 1: NUTRIENT DATASET ANALYSIS")
    print("=" * 60)
    
    classes = ['healthy', 'nitrogen_deficiency', 'phosphorus_deficiency', 'potassium_deficiency']
    records = []
    corrupted_count = 0
    dimensions_set = set()
    
    for cls in classes:
        cls_dir = os.path.join(dataset_dir, cls)
        if not os.path.exists(cls_dir):
            print(f"Warning: Directory '{cls_dir}' does not exist!")
            continue
            
        imgs = glob.glob(os.path.join(cls_dir, "*.*"))
        for img_path in imgs:
            ext = os.path.splitext(img_path)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg']:
                continue
                
            is_valid = True
            width, height, mode = None, None, None
            try:
                with Image.open(img_path) as img:
                    img.verify()
                with Image.open(img_path) as img:
                    width, height = img.size
                    mode = img.mode
                    dimensions_set.add((width, height))
            except Exception:
                is_valid = False
                corrupted_count += 1
                
            records.append({
                'image_path': os.path.normpath(img_path).replace('\\', '/'),
                'class': cls,
                'width': width,
                'height': height,
                'mode': mode,
                'is_valid': is_valid
            })

    df = pd.DataFrame(records)
    total_imgs = len(df)
    
    print(f"\nTotal Images Analyzed: {total_imgs}")
    print(f"Corrupted Images: {corrupted_count}")
    print("\nClass Distribution:")
    class_counts = df['class'].value_counts()
    for cls_name, count in class_counts.items():
        pct = (count / total_imgs) * 100
        print(f"  - {cls_name}: {count} images ({pct:.1f}%)")
        
    print("\nSample Image Dimensions (width x height):")
    for dim in list(dimensions_set)[:5]:
        print(f"  - {dim[0]}x{dim[1]}")
        
    print("\nImbalance Analysis:")
    min_class = class_counts.idxmin()
    max_class = class_counts.idxmax()
    imbalance_ratio = class_counts[max_class] / max(class_counts[min_class], 1)
    print(f"  - Minority Class: '{min_class}' ({class_counts[min_class]} images)")
    print(f"  - Majority Class: '{max_class}' ({class_counts[max_class]} images)")
    print(f"  - Imbalance Ratio: {imbalance_ratio:.2f}x")
    print("  - Recommendation: Use stratified data splitting, class weighting, and targeted minority class augmentation.")
    
    return df

if __name__ == '__main__':
    analyze_dataset()
