import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = os.path.join("backend", "uploads", "plant_images")

class ImageProcessor:
    """
    Validates uploaded plant photos for type limits (JPG, JPEG, PNG)
    and size constraints (< 5MB), committing images to disk.
    """
    @staticmethod
    def validate_image(file: UploadFile) -> bool:
        filename = file.filename.lower()
        if not (filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png")):
            return False
            
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        
        max_size = 5 * 1024 * 1024
        if size > max_size:
            return False
            
        return True

    @staticmethod
    def save_image(file: UploadFile) -> str:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            
        unique_name = f"{uuid.uuid4().hex}_{file.filename}"
        save_path = os.path.join(UPLOAD_DIR, unique_name)
        
        file.file.seek(0)
        with open(save_path, "wb") as f:
            f.write(file.file.read())
            
        return save_path
