import logging
from unittest.mock import Mock, patch
from core.markdown_index.cli import main

@patch('core.markdown_index.MarkdownIndex')
@patch('core.markdown_index.cli.argparse.ArgumentParser')
def test_main_default_args(mock_parser, mock_generator):
    mock_args = Mock()
    mock_args.path = "/test/path"
    mock_args.verbose = False
    mock_parser.return_value.parse_args.return_value = mock_args

    mock_instance = Mock()
    mock_generator.return_value = mock_instance

    result = main()

    mock_generator.assert_called_once_with("/test/path", logging.getLogger('markdown_index.cli'))
    mock_instance.generate.assert_called_once()
    assert result == 0

@patch('core.markdown_index.MarkdownIndex')
@patch('core.markdown_index.cli.argparse.ArgumentParser')
def test_main_verbose_flag(mock_parser, mock_generator):
    mock_args = Mock()
    mock_args.path = "/test/path"
    mock_args.verbose = True
    mock_parser.return_value.parse_args.return_value = mock_args

    mock_instance = Mock()
    mock_generator.return_value = mock_instance

    result = main()

    mock_generator.assert_called_once_with("/test/path", logging.getLogger('markdown_index.cli'))
    mock_instance.generate.assert_called_once()
    assert result == 0
    assert logging.getLogger('markdown_index.cli').level == logging.DEBUG

@patch('core.markdown_index.MarkdownIndex')
@patch('core.markdown_index.cli.argparse.ArgumentParser')
def test_main_generator_exception(mock_parser, mock_generator):
    mock_args = Mock()
    mock_args.path = "/broken/path"
    mock_args.verbose = False
    mock_parser.return_value.parse_args.return_value = mock_args

    mock_generator.return_value.generate.side_effect = Exception("Generation failed")

    result = main()

    mock_generator.assert_called_once()
    assert result == 1
