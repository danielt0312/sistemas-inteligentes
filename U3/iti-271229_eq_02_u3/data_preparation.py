import os
import shutil
from sklearn.model_selection import train_test_split

def organize_data(base_path, output_path, test_size=0.2):
    """
    Organiza las imágenes en carpetas para entrenamiento y validación.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for label in os.listdir(base_path):
        label_path = os.path.join(base_path, label)
        if not os.path.isdir(label_path):
            continue
        
        files = os.listdir(label_path)
        train_files, val_files = train_test_split(files, test_size=test_size)
        
        for subset, file_list in zip(['train', 'val'], [train_files, val_files]):
            subset_path = os.path.join(output_path, subset, label)
            if not os.path.exists(subset_path):
                os.makedirs(subset_path)
            
            for file in file_list:
                shutil.copy(os.path.join(label_path, file), subset_path)

if __name__ == "__main__":
    organize_data('data/train', 'data/otra')
