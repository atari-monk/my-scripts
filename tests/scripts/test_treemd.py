import logging
from unittest.mock import Mock, patch
from scripts.treemd import main

@patch('scripts.treemd.TreeMDGenerator')
@patch('scripts.treemd.argparse.ArgumentParser')
def test_main_default_args(mock_parser, mock_generator):
    mock_args = Mock()
    mock_args.path = "/test/path"
    mock_args.save = False
    mock_args.output_dir = "docs"
    mock_args.verbose = False
    mock_parser.return_value.parse_args.return_value = mock_args
    
    mock_gen_instance = Mock()
    mock_generator.return_value = mock_gen_instance
    
    main()
    
    mock_generator.assert_called_once_with(log_level=logging.INFO)
    mock_gen_instance.generate_tree.assert_called_once_with("/test/path", False, "docs")

@patch('scripts.treemd.TreeMDGenerator')
@patch('scripts.treemd.argparse.ArgumentParser')
def test_main_verbose_flag(mock_parser, mock_generator):
    mock_args = Mock()
    mock_args.path = "/path"
    mock_args.save = False
    mock_args.output_dir = "docs"
    mock_args.verbose = True
    mock_parser.return_value.parse_args.return_value = mock_args
    
    main()
    mock_generator.assert_called_once_with(log_level=logging.DEBUG)

@patch('scripts.treemd.TreeMDGenerator')
@patch('scripts.treemd.argparse.ArgumentParser')
def test_main_save_flag(mock_parser, mock_generator):
    mock_args = Mock()
    mock_args.path = "/path"
    mock_args.save = True
    mock_args.output_dir = "docs"
    mock_args.verbose = False
    mock_parser.return_value.parse_args.return_value = mock_args
    
    main()
    mock_generator.return_value.generate_tree.assert_called_once()

@patch('scripts.treemd.TreeMDGenerator')
@patch('scripts.treemd.argparse.ArgumentParser')
def test_main_custom_output_dir(mock_parser, mock_generator):
    mock_args = Mock()
    mock_args.path = "/path"
    mock_args.save = False
    mock_args.output_dir = "custom"
    mock_args.verbose = False
    mock_parser.return_value.parse_args.return_value = mock_args
    
    main()
    mock_generator.return_value.generate_tree.assert_called_with('/path', False, 'custom')