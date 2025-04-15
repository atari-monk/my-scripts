#!/usr/bin/env python3

import sys
import logging
import argparse
from typing import List, Optional
from core.DocumentationGenerator import DocumentationGenerator

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description='Generate documentation index from docs folder or repo root',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to repository root directory'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    try:
        parsed_args = parser.parse_args(args)
        
        if parsed_args.verbose:
            logger.setLevel(logging.DEBUG)
            
        generator = DocumentationGenerator(parsed_args.path, logger)
        generator.generate()
        return 0
        
    except Exception as e:
        logger.error(str(e))
        return 1

if __name__ == '__main__':
    sys.exit(main())