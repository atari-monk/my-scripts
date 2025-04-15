import os
from unittest.mock import patch
import pytest
import pyperclip
from core.TreeMDGenerator import TreeMDGenerator

class TestTreeMDGenerator:
    @pytest.fixture
    def generator(self):
        return TreeMDGenerator()

    @pytest.fixture
    def mock_directory_tree_generator(self):
        with patch('core.TreeMDGenerator.DirectoryTreeGenerator') as mock:
            mock_instance = mock.return_value
            mock_instance.generate.return_value = "mock_md_content"
            mock_instance.repo_name = "mock_repo"
            yield mock_instance

    @pytest.fixture
    def mock_path(self, tmp_path):
        return str(tmp_path)

    def test_validate_directory_with_valid_path(self, generator, mock_path):
        assert generator.validate_directory(mock_path) is True

    def test_validate_directory_with_invalid_path(self, generator):
        assert generator.validate_directory("/nonexistent/path") is False

    def test_save_to_file_creates_directory_and_file(self, generator, mock_path):
        test_content = "test content"
        test_filename = "test_file.md"
        output_path = generator.save_to_file(test_content, mock_path, test_filename)

        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            assert f.read() == test_content

    def test_generate_tree_with_invalid_directory(self, generator):
        result = generator.generate_tree("/invalid/path")
        assert result is None

    def test_generate_tree_without_save(self, generator, mock_path, mock_directory_tree_generator):
        result = generator.generate_tree(mock_path)
        assert result == "mock_md_content"
        mock_directory_tree_generator.generate.assert_called_once()

    def test_generate_tree_with_save(self, generator, mock_path, mock_directory_tree_generator):
        result = generator.generate_tree(mock_path, save=True)
        expected_path = os.path.join(mock_path, "docs", "mock_repo_file_tree.md")
        assert result == expected_path
        assert os.path.exists(result)

    def test_generate_tree_clipboard_success(self, generator, mock_path, mock_directory_tree_generator):
        with patch('pyperclip.copy') as mock_copy:
            generator.generate_tree(mock_path)
            mock_copy.assert_called_once_with("mock_md_content")

    def test_generate_tree_clipboard_failure(self, generator, mock_path, mock_directory_tree_generator):
        with patch('pyperclip.copy', side_effect=pyperclip.PyperclipException("mock error")):
            generator.generate_tree(mock_path)
            mock_directory_tree_generator.generate.assert_called_once()

    def test_generate_tree_exception_handling(self, generator, mock_path):
        with patch('core.TreeMDGenerator.DirectoryTreeGenerator', side_effect=Exception("mock error")):
            with pytest.raises(Exception):
                generator.generate_tree(mock_path)