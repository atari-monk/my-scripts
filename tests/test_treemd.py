#!/usr/bin/env python3
import os
import unittest
import tempfile
import shutil
from unittest.mock import patch
import pyperclip
from scripts.treemd import validate_directory, save_to_file, main

class TestTreemd(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("test content")
        self.sub_dir = os.path.join(self.test_dir, "subdir")
        os.makedirs(self.sub_dir)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_validate_directory(self):
        self.assertTrue(validate_directory(self.test_dir))
        self.assertFalse(validate_directory("/nonexistent/path"))
        self.assertFalse(validate_directory(self.test_file))

    def test_save_to_file(self):
        test_content = "Test content"
        output_dir = os.path.join(self.test_dir, "output")
        filename = "test_output.md"
        
        output_path = save_to_file(test_content, output_dir, filename)
        self.assertTrue(os.path.exists(output_path))
        
        with open(output_path, "r") as f:
            content = f.read()
        self.assertEqual(content, test_content)
        
        output_path = save_to_file(test_content, output_dir, filename)
        self.assertTrue(os.path.exists(output_path))

    @patch('pyperclip.copy')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse_args, mock_pyperclip):
        mock_args = type('', (), {})()
        mock_args.path = self.test_dir
        mock_args.save = False
        mock_args.output_dir = "docs"
        mock_parse_args.return_value = mock_args
        
        with patch('builtins.print') as mock_print:
            main()
        
        mock_pyperclip.assert_called_once()
        mock_print.assert_called_with("Structure copied to clipboard!")

    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_directory(self, mock_parse_args):
        mock_args = type('', (), {})()
        mock_args.path = "/invalid/path"
        mock_args.save = False
        mock_args.output_dir = "docs"
        mock_parse_args.return_value = mock_args
        
        with patch('builtins.print') as mock_print:
            main()
        
        mock_print.assert_called_with("Error: Invalid directory path")

    @patch('pyperclip.copy')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_save(self, mock_parse_args, mock_pyperclip):
        mock_args = type('', (), {})()
        mock_args.path = self.test_dir
        mock_args.save = True
        mock_args.output_dir = "docs"
        mock_parse_args.return_value = mock_args
        
        with patch('builtins.print') as mock_print:
            main()
        
        mock_pyperclip.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)
        self.assertIn("Structure copied to clipboard!", mock_print.call_args_list[0][0][0])
        self.assertIn("Saved to", mock_print.call_args_list[1][0][0])

    @patch('pyperclip.copy', side_effect=pyperclip.PyperclipException("Clipboard error"))
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_clipboard_error(self, mock_parse_args, mock_pyperclip):
        mock_args = type('', (), {})()
        mock_args.path = self.test_dir
        mock_args.save = False
        mock_args.output_dir = "docs"
        mock_parse_args.return_value = mock_args
        
        with patch('builtins.print') as mock_print:
            main()
        
        mock_print.assert_called_with("Warning: Could not copy to clipboard - Clipboard error")

if __name__ == '__main__':
    unittest.main()