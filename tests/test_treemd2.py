#!/usr/bin/env python3
import os
import unittest
import tempfile
import shutil
import logging
from unittest.mock import patch, MagicMock
from pathlib import Path
import pyperclip
from scripts.treemd2 import TreeMDGenerator

class TestTreeMDGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        (Path(self.test_dir) / "test_file.txt").write_text("test content")
        self.sub_dir = Path(self.test_dir) / "subdir"
        self.sub_dir.mkdir()
        
        self.log_capture = []
        self.handler = logging.Handler()
        self.handler.emit = lambda record: self.log_capture.append(record)
        logging.getLogger('scripts.treemd2').addHandler(self.handler)
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        logging.getLogger('scripts.treemd2').removeHandler(self.handler)

    def test_validate_directory(self):
        generator = TreeMDGenerator()
        self.assertTrue(generator.validate_directory(self.test_dir))
        self.assertFalse(generator.validate_directory("/nonexistent/path"))
        self.assertFalse(generator.validate_directory(str(Path(self.test_dir) / "test_file.txt")))

    def test_save_to_file(self):
        generator = TreeMDGenerator()
        test_content = "Test content"
        output_dir = str(Path(self.test_dir) / "output")
        filename = "test_output.md"
        
        output_path = generator.save_to_file(test_content, output_dir, filename)
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(Path(output_path).read_text(), test_content)

    @patch('pyperclip.copy')
    def test_generate_tree_success(self, mock_copy):
        generator = TreeMDGenerator()
        generator.generate_tree(self.test_dir)
        
        mock_copy.assert_called_once()
        self.assertTrue(any("Structure copied to clipboard!" in record.getMessage() 
                         for record in self.log_capture 
                         if record.levelno == logging.INFO))

    @patch('pyperclip.copy')
    def test_generate_tree_with_save(self, mock_copy):
        generator = TreeMDGenerator()
        generator.generate_tree(self.test_dir, save=True)
        
        mock_copy.assert_called_once()
        self.assertTrue(any("Structure copied to clipboard!" in record.getMessage() 
                         for record in self.log_capture 
                         if record.levelno == logging.INFO))
        self.assertTrue(any("Saved to" in record.getMessage() 
                          for record in self.log_capture 
                          if record.levelno == logging.INFO))
        
        output_path = Path(self.test_dir) / "docs" / f"{Path(self.test_dir).name}_file_tree.md"
        self.assertTrue(output_path.exists())

    def test_generate_tree_invalid_directory(self):
        generator = TreeMDGenerator()
        result = generator.generate_tree("/invalid/path")
        
        self.assertIsNone(result)
        self.assertTrue(any("Invalid directory path" in record.getMessage() 
                         for record in self.log_capture 
                         if record.levelno == logging.ERROR))

    @patch('pyperclip.copy', side_effect=pyperclip.PyperclipException("Clipboard error"))
    def test_generate_tree_clipboard_error(self, mock_copy):
        generator = TreeMDGenerator()
        result = generator.generate_tree(self.test_dir)
        
        self.assertIsNotNone(result)
        self.assertTrue(any("Could not copy to clipboard" in record.getMessage() 
                         for record in self.log_capture 
                         if record.levelno == logging.WARNING))

    @patch('scripts.treemd2.DirectoryTreeGenerator')
    def test_generate_tree_generation_error(self, mock_generator):
        mock_generator.return_value.generate.side_effect = Exception("Generation failed")
        generator = TreeMDGenerator()
        
        with self.assertRaises(Exception):
            generator.generate_tree(self.test_dir)
        
        self.assertTrue(any("Generation failed" in record.getMessage() 
                         for record in self.log_capture 
                         if record.levelno == logging.ERROR))

    @patch('scripts.treemd2.TreeMDGenerator')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse_args, mock_generator):
        mock_args = MagicMock()
        mock_args.path = self.test_dir
        mock_args.save = False
        mock_args.output_dir = "docs"
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args
        
        from scripts.treemd2 import main
        main()
        
        mock_generator.return_value.generate_tree.assert_called_once_with(
            self.test_dir, False, "docs")

    @patch('scripts.treemd2.TreeMDGenerator')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_verbose(self, mock_parse_args, mock_generator):
        mock_args = MagicMock()
        mock_args.path = self.test_dir
        mock_args.save = True
        mock_args.output_dir = "custom_output"
        mock_args.verbose = True
        mock_parse_args.return_value = mock_args
        
        from scripts.treemd2 import main
        main()
        
        mock_generator.return_value.generate_tree.assert_called_once_with(
            self.test_dir, True, "custom_output")

if __name__ == '__main__':
    unittest.main()