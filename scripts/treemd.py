#!/usr/bin/env python3

import os
import argparse
import pyperclip
from core.directory_tree import DirectoryTreeGenerator

DEFAULT_ENCODING = "utf-8"
DEFAULT_DOCS_DIR = "docs"
OUTPUT_FILENAME_TEMPLATE = "{repo_name}_file_tree.md"

def validate_directory(path: str) -> bool:
    return os.path.isdir(path)

def save_to_file(content: str, directory: str, filename: str) -> str:
    os.makedirs(directory, exist_ok=True)
    output_path = os.path.join(directory, filename)
    
    with open(output_path, "w", encoding=DEFAULT_ENCODING) as f:
        f.write(content)
    
    return output_path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory path to generate structure for")
    parser.add_argument("--save", action="store_true", help="Save to markdown file")
    parser.add_argument("--output-dir", default=DEFAULT_DOCS_DIR)
    args = parser.parse_args()

    if not validate_directory(args.path):
        print("Error: Invalid directory path")
        return

    try:
        generator = DirectoryTreeGenerator(args.path)
        md_content = generator.generate()
        
        try:
            pyperclip.copy(md_content)
            print("Structure copied to clipboard!")
        except pyperclip.PyperclipException as e:
            print(f"Warning: Could not copy to clipboard - {str(e)}")
        
        if args.save:
            output_filename = OUTPUT_FILENAME_TEMPLATE.format(
                repo_name=generator.repo_name
            )
            output_path = save_to_file(
                md_content,
                os.path.join(args.path, args.output_dir),
                output_filename
            )
            print(f"Saved to {output_path}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()