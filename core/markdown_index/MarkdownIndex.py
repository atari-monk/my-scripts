import re
from typing import List
from core.markdown_index.Heading import Heading

class MarkdownIndex:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._headings: List[Heading] = []
        self._content_lines: List[str] = []
        self._load_content()

    def _load_content(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self._content_lines = f.readlines()

    def extract_headings(self) -> List[Heading]:
        if self._headings:
            return self._headings

        heading_pattern = re.compile(r'^(#+)\s+(.+)$')
        self._headings = []

        for i, line in enumerate(self._content_lines):
            match = heading_pattern.match(line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                self._headings.append(Heading(level, text, i))

        return self._headings

    def generate_index(self, headings: List[Heading]) -> str:
        if not headings:
            return ""

        index_lines = ["## Table of Contents\n"]
        for heading in headings:
            indent = '  ' * (heading.level - 1)
            anchor = self._create_anchor(heading.text)
            index_lines.append(f"{indent}- [{heading.text}](#{anchor})")

        return '\n'.join(index_lines) + '\n'

    def _create_anchor(self, text: str) -> str:
        # Convert to lowercase, replace spaces with hyphens, remove special chars
        anchor = text.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        return anchor

    def insert_index(self) -> bool:
        headings = self.extract_headings()
        if not headings or headings[0].level != 1:
            return False

        index = self.generate_index(headings)
        first_heading_line = headings[0].line_number
        next_line = first_heading_line + 1

        # Check if index already exists
        if (next_line < len(self._content_lines) and 
            "## Table of Contents" in self._content_lines[next_line]):
            return False

        # Insert the index after the main title
        new_content = (
            self._content_lines[:first_heading_line + 1] +
            ['\n', index, '\n'] +
            self._content_lines[first_heading_line + 1:]
        )

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_content)

        return True