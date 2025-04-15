import os
import tempfile
import unittest
from core.DirectoryTreeGenerator import IGNORE, DirectoryTreeGenerator

class TestDirectoryTreeGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.repo_name = os.path.basename(self.test_dir)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def _create_test_files(self, structure):
        for name, content in structure.items():
            path = os.path.join(self.test_dir, name)
            if content is None:
                os.makedirs(path, exist_ok=True)
            else:
                with open(path, 'w') as f:
                    f.write(content)

    def test_ignore_files(self):
        structure = {
            "included.txt": "content",
            "package-lock.json": "{}"
        }
        self._create_test_files(structure)
        
        generator = DirectoryTreeGenerator(self.test_dir)
        result = generator.generate()
        
        self.assertIn("included.txt", result)
        self.assertNotIn("package-lock.json", result)

    def test_ignore_folders(self):
        structure = {
            "included_dir": None,
            ".git": None,
            "node_modules": None,
            "included_dir/file.txt": "content"
        }
        self._create_test_files(structure)
        
        generator = DirectoryTreeGenerator(self.test_dir)
        result = generator.generate()
        
        self.assertIn("included_dir", result)
        self.assertIn("file.txt", result)
        self.assertNotIn(".git", result)
        self.assertNotIn("node_modules", result)

    def test_should_ignore_folder(self):
        generator = DirectoryTreeGenerator(self.test_dir)
        for folder in IGNORE["folders"]:
            path = os.path.join(self.test_dir, folder)
            os.makedirs(path, exist_ok=True)
            self.assertTrue(generator._should_ignore(path, folder))

    def test_should_ignore_file(self):
        generator = DirectoryTreeGenerator(self.test_dir)
        for file in IGNORE["files"]:
            path = os.path.join(self.test_dir, file)
            with open(path, 'w') as f:
                f.write("test")
            self.assertTrue(generator._should_ignore(path, file))

if __name__ == '__main__':
    unittest.main()