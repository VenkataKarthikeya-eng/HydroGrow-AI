import unittest
import os

class TestDockerConfiguration(unittest.TestCase):

    def test_docker_files_exist(self):
        root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        self.assertTrue(os.path.exists(os.path.join(root, "backend", "Dockerfile")))
        self.assertTrue(os.path.exists(os.path.join(root, "frontend", "Dockerfile")))
        self.assertTrue(os.path.exists(os.path.join(root, "docker-compose.yml")))
        self.assertTrue(os.path.exists(os.path.join(root, ".dockerignore")))

if __name__ == "__main__":
    unittest.main()
