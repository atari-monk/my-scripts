#!/usr/bin/env python3
import argparse
from pathlib import Path
from core.markdown_indexer.MarkdownIndexer import MarkdownIndexer

def main():
    parser = argparse.ArgumentParser(
        description="Generate and insert a table of contents in markdown files"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to markdown file or directory (default: current directory)",
    )
    args = parser.parse_args()

    path = Path(args.path)
    if path.is_file() and path.suffix == ".md":
        process_file(path)
    elif path.is_dir():
        process_directory(path)
    else:
        print(f"Error: {path} is not a markdown file or directory")

def process_file(md_file: Path):
    try:
        indexer = MarkdownIndexer(str(md_file))
        if indexer.insert_index():
            print(f"Added table of contents to: {md_file}")
        else:
            print(f"No changes made to: {md_file} (already has TOC or no headings)")
    except Exception as e:
        print(f"Error processing {md_file}: {str(e)}")

def process_directory(directory: Path):
    md_files = list(directory.glob("**/*.md"))
    if not md_files:
        print(f"No markdown files found in: {directory}")
        return

    for md_file in md_files:
        process_file(md_file)

if __name__ == "__main__":
    main()