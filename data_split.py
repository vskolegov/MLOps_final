import os
import pandas as pd

#  Split dataset to different length parts
def split_dataset(file_path, splits, output_dir):
    df = pd.read_csv(file_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for split in splits:
        split_df = df.sample(n=split, random_state=42)
        local_path = os.path.join(output_dir, f'dataset_{split}.csv')
        
        split_df.to_csv(local_path, index=False)
        print(f'Dataset with {split} rows saved to {local_path}')

if __name__ == "__main__":
    dataset_path = 'D:\Develop\MLOps_final\wine.data.csv'  
    splits = [50, 100, 150]  
    output_dir = 'split_datasets' 

    split_dataset(dataset_path, splits, output_dir)
