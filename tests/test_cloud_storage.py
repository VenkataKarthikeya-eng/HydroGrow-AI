import unittest
from backend.cloud.cloud_storage import CloudStorageProvider

class TestCloudStorage(unittest.TestCase):

    def test_upload_and_download_file(self):
        storage = CloudStorageProvider(provider="local")
        content = b"HydroGrow AI Cloud Data Test"
        dest = "test_data/sample.txt"

        up_res = storage.upload_file(content, dest)
        self.assertEqual(up_res["status"], "uploaded")

        dl_data = storage.download_file(dest)
        self.assertEqual(dl_data, content)

        deleted = storage.delete_file(dest)
        self.assertTrue(deleted)

if __name__ == "__main__":
    unittest.main()
