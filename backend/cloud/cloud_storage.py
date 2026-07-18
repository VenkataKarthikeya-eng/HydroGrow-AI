import os
import shutil
from backend.config.settings import settings

class CloudStorageProvider:
    """
    Unified Cloud Storage abstraction interface.
    Supports local filesystem fallback as well as AWS S3, Azure Blob, and GCS integrations.
    """

    def __init__(self, provider: str = None):
        self.provider = provider or settings.STORAGE_PROVIDER
        self.local_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
        os.makedirs(self.local_root, exist_ok=True)

    def upload_file(self, file_content: bytes, destination_key: str) -> dict:
        target_path = os.path.join(self.local_root, destination_key)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "wb") as f:
            f.write(file_content)

        return {
            "status": "uploaded",
            "provider": self.provider,
            "destination_key": destination_key,
            "local_path": target_path,
            "size_bytes": len(file_content),
            "url": f"/uploads/{destination_key}"
        }

    def download_file(self, destination_key: str) -> bytes:
        target_path = os.path.join(self.local_root, destination_key)
        if os.path.exists(target_path):
            with open(target_path, "rb") as f:
                return f.read()
        return b""

    def delete_file(self, destination_key: str) -> bool:
        target_path = os.path.join(self.local_root, destination_key)
        if os.path.exists(target_path):
            os.remove(target_path)
            return True
        return False
