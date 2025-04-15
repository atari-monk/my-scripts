#!/usr/bin/env python3
import argparse
import logging
from core.TreeMDGenerator import DEFAULT_DOCS_DIR, TreeMDGenerator

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory path to generate structure for")
    parser.add_argument("-s", "--save", action="store_true", help="Save to markdown file")
    parser.add_argument("-o", "--output-dir", default=DEFAULT_DOCS_DIR, help="Output directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    generator = TreeMDGenerator(log_level=logging.DEBUG if args.verbose else logging.INFO)
    generator.generate_tree(args.path, args.save, args.output_dir)

if __name__ == "__main__":
    main()