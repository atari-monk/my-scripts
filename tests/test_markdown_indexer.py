import unittest
import os
import tempfile
from core.markdown_indexer.Heading import Heading
from core.markdown_indexer.MarkdownIndexer import MarkdownIndexer

class TestMarkdownIndexer(unittest.TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.md')
        self.test_content = """# Main Title

Some intro text

## Section 1
Content 1

### Subsection 1.1
More content

## Section 2
Final content
"""
        self.test_file.write(self.test_content)
        self.test_file.close()
        
    def tearDown(self):
        os.unlink(self.test_file.name)
        
    def test_heading_detection(self):
      indexer = MarkdownIndexer(self.test_file.name)
      headings = indexer.extract_headings()
      self.assertEqual(len(headings), 4)
      self.assertEqual(headings[0].text, 'Main Title')
      self.assertEqual(headings[0].level, 1)

    def test_heading_validation(self):
      with self.assertRaises(ValueError):
          Heading(level=0, text="Invalid", line_number=0)
      with self.assertRaises(ValueError):
          Heading(level=7, text="Invalid", line_number=0)
      with self.assertRaises(ValueError):
          Heading(level=1, text="", line_number=0)

    def test_index_generation(self):
        indexer = MarkdownIndexer(self.test_file.name)
        headings = indexer.extract_headings()
        index = indexer.generate_index(headings)
        self.assertIn('- [Main Title](#main-title)', index)
        self.assertIn('  - [Section 1](#section-1)', index)
        
    def test_index_insertion(self):
        indexer = MarkdownIndexer(self.test_file.name)
        result = indexer.insert_index()
        with open(self.test_file.name, 'r') as f:
            content = f.read()
        self.assertIn('# Main Title\n\n## Table of Contents', content)
        self.assertIn('- [Section 1](#section-1)', content)
        
    def test_no_duplicate_index(self):
        indexer = MarkdownIndexer(self.test_file.name)
        first_run = indexer.insert_index()
        second_run = indexer.insert_index()
        self.assertEqual(first_run, second_run)

if __name__ == '__main__':
    unittest.main()