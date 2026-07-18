import unittest
import os
from backend.database.backup_manager import BackupManager

class TestBackupManager(unittest.TestCase):

    def test_backup_generation_and_validation(self):
        bm = BackupManager()
        res = bm.generate_backup()
        self.assertEqual(res["status"], "success")
        self.assertTrue(os.path.exists(res["filepath"]))
        self.assertTrue(bm.validate_backup(res["filepath"]))

if __name__ == "__main__":
    unittest.main()
