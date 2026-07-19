import os
import glob
import pandas as pd
from datetime import datetime

def generate_labels(dataset_dir="data/growth_dataset", output_csv="data/processed/growth_labels.csv"):
    month_starts = {
        'Month1': datetime.strptime('2024-03-09', '%Y-%m-%d'),
        'Month2': datetime.strptime('2024-04-16', '%Y-%m-%d'),
        'Month3': datetime.strptime('2024-05-21', '%Y-%m-%d')
    }

    records = []
    
    print(f"Scanning dataset in '{dataset_dir}'...")
    
    for month, start_dt in month_starts.items():
        month_path = os.path.join(dataset_dir, month)
        if not os.path.exists(month_path):
            print(f"Warning: Directory '{month_path}' not found!")
            continue

        # Find all png files
        png_files = glob.glob(os.path.join(month_path, '**', '*.png'), recursive=True)
        print(f"  {month}: Found {len(png_files)} PNG images.")
        
        for p in png_files:
            # Normalize path slashes
            rel_path = os.path.normpath(p).replace('\\', '/')
            parts = rel_path.split('/')
            
            date_str = None
            for pt in parts:
                if len(pt) == 10 and pt.count('-') == 2:
                    date_str = pt
                    break
            
            if date_str:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                growth_day = (dt - start_dt).days + 1
                
                # Assign stage label
                if growth_day <= 10:
                    growth_stage = 'Seedling'
                elif growth_day <= 20:
                    growth_stage = 'Vegetative'
                else:
                    growth_stage = 'Mature / Harvest'
                
                records.append({
                    'image_path': rel_path,
                    'date': date_str,
                    'growth_day': growth_day,
                    'growth_stage': growth_stage
                })

    df = pd.DataFrame(records)
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    df.to_csv(output_csv, index=False)
    print(f"\nSuccessfully saved {len(df):,} records to '{output_csv}'.")
    
    # Display summary
    print("\nDataset Summary:")
    print(df['growth_stage'].value_counts())
    print("\nGrowth Day Summary:")
    print(f"  Min growth day: {df['growth_day'].min()}")
    print(f"  Max growth day: {df['growth_day'].max()}")
    print(f"  Unique dates count: {df['date'].nunique()}")
    
    return df

if __name__ == '__main__':
    generate_labels()
