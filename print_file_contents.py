"""print_file_content.py - Examples for using file_content_printer.py

This module provides example commands and configurations for different project types
when using the file_content_printer.py script.

Common Usage Examples:

Rust Projects:
    # Print all Rust files in a project, excluding target directory
    python print_file_contents.py --dir ~/projects/pax --ext .rs --exclude "target/*" --output "rust_code.txt"
    
    # Analyze a specific Rust workspace with multiple excludes
    python print_file_contents.py --dir ~/rust/substrate --ext .rs .toml --exclude "target/*" "*.tmp" "**/node_modules/*" --output "substrate_code.txt"
    
    # Get Rust code from specific module
    python print_file_contents.py --dir ~/projects/pax/src/runtime --ext .rs --exclude "target/*" --output "runtime_code.txt"

Go Projects:
    # Print all Go files in a project
    python print_file_contents.py --dir ~/go/src/myproject --ext .go --exclude "vendor/*" --output "go_code.txt"
    
    # Get Go code including module files
    python print_file_contents.py --dir ~/projects/hugo --ext .go .mod .sum --exclude "vendor/*" "bin/*" --output "hugo_code.txt"
    
    # Analyze specific Go package
    python print_file_contents.py --dir ~/go/src/myproject/pkg/api --ext .go --output "api_code.txt"

Python Projects:
    # Print all Python files in a Django project
    python print_file_contents.py --dir ~/projects/django-app --ext .py --exclude "__pycache__/*" "venv/*" "*.pyc" --output "django_code.txt"
    
    # Get Python code including Cython files
    python print_file_contents.py --dir ~/projects/numpy --ext .py .pyx .pxd --exclude "build/*" "*.pyc" --output "numpy_code.txt"
    
    # Analyze specific Python package
    python print_file_contents.py --dir ~/projects/flask/src/views --ext .py --exclude "__pycache__/*" --output "views_code.txt"

Node.js Projects:
    # Print all TypeScript files in a React project
    python print_file_contents.py --dir ~/projects/react-app --ext .ts .tsx --exclude "node_modules/*" "build/*" --output "react_code.txt"
    
    # Get all JavaScript and TypeScript code
    python print_file_contents.py --dir ~/projects/next-app --ext .js .jsx .ts .tsx --exclude "node_modules/*" ".next/*" --output "next_code.txt"
    
    # Analyze specific React component directory
    python print_file_contents.py --dir ~/projects/react-app/src/components --ext .tsx --output "components_code.txt"

Java Projects:
    # Print all Java files in a Spring project
    python print_file_contents.py --dir ~/projects/spring-app --ext .java --exclude "target/*" "build/*" --output "spring_code.txt"
    
    # Get Java code including config files
    python print_file_contents.py --dir ~/projects/android-app --ext .java .xml .gradle --exclude "build/*" ".gradle/*" --output "android_code.txt"
    
    # Analyze specific Java package
    python print_file_contents.py --dir ~/projects/app/src/main/java/com/example/service --ext .java --output "service_code.txt"

Advanced Usage:
    # Multiple specific excludes
    python print_file_contents.py --dir ~/projects/full-stack --ext .rs .ts --exclude "target/*" "node_modules/*" "dist/*" "*.tmp" --output "code.txt"
    
    # Debug mode with verbose output
    python print_file_contents.py --dir ~/projects/pax --ext .rs --exclude "target/*" --verbose --output "debug_code.txt"
    
    # Print to console instead of file
    python print_file_contents.py --dir ~/projects/pax/src --ext .rs --exclude "target/*"

Examples:
    # Print examples for all project types
    python file_printer_examples.py all

    # Print examples for specific project type
    python file_printer_examples.py rust
    python file_printer_examples.py go
"""

import os
import fnmatch
import logging

def print_file_contents(directory='.', file_extensions=None, exclude_patterns=None, output_file=None, verbose=False):
    """
    Recursively print contents of all files in the given directory.
    
    Args:
        directory (str): The root directory to start searching from
        file_extensions (list): Optional list of file extensions to filter (e.g., ['.rs', '.py'])
        exclude_patterns (list): List of glob patterns to exclude (e.g., ['*.pyc', 'node_modules/**'])
        output_file (str): Optional file path to write output instead of printing to console
        verbose (bool): Whether to print debug information
    """
    
    # Setup logging
    logging_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(message)s')
    
    def normalize_path(path):
        """Convert path to absolute path and normalize it"""
        return os.path.normpath(os.path.abspath(path))
    
    def should_exclude(path):
        if not exclude_patterns:
            return False
            
        # Get path relative to the target directory
        rel_path = os.path.relpath(path, abs_directory)
        logging.debug(f"Checking path: {path}")
        logging.debug(f"Relative to {abs_directory}: {rel_path}")
        
        for pattern in exclude_patterns:
            # Normalize pattern - convert backslashes to forward slashes
            pattern = pattern.replace('\\', '/')
            # Convert path to forward slashes for consistent matching
            check_path = rel_path.replace('\\', '/')
            
            # Handle directory patterns (ending with /**)
            if pattern.endswith('/**'):
                dir_pattern = pattern[:-3]
                if check_path.startswith(dir_pattern):
                    logging.debug(f"Excluded {check_path} (matches directory pattern {pattern})")
                    return True
            
            # Handle simple glob patterns
            if fnmatch.fnmatch(check_path, pattern) or \
               fnmatch.fnmatch(os.path.basename(path), pattern):
                logging.debug(f"Excluded {check_path} (matches pattern {pattern})")
                return True
                
        logging.debug(f"Including {rel_path}")
        return False
    
    def write_output(text):
        if output_file:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
        else:
            print(text)
    
    def get_file_extension(file_path):
        """Get the file extension without the dot"""
        return os.path.splitext(file_path)[1][1:]
    
    # Clear output file if it exists
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('')
    
    # Convert directory to absolute path
    abs_directory = normalize_path(directory)
    logging.debug(f"Absolute directory path: {abs_directory}")
    
    # Log initial settings
    if exclude_patterns:
        logging.debug("Exclude patterns:")
        for pattern in exclude_patterns:
            logging.debug(f"  - {pattern}")
    
    # Walk through directory
    for root, dirs, files in os.walk(abs_directory):
        # Remove excluded directories using absolute paths
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip if file should be excluded
            if should_exclude(file_path):
                continue
                
            # Check if we should filter by extension
            if file_extensions:
                if not any(file.endswith(ext) for ext in file_extensions):
                    logging.debug(f"Skipping {file_path} (extension not in {file_extensions})")
                    continue
            
            try:
                # Get relative path for cleaner output
                rel_path = os.path.relpath(file_path, abs_directory)
                
                # Write the file path
                write_output(f"\n{rel_path}")
                
                # Get file extension for code block
                ext = get_file_extension(file_path)
                
                # Write opening code fence with language
                write_output(f"```{ext}")
                
                # Read and write the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove trailing whitespace but keep newlines
                    content = '\n'.join(line.rstrip() for line in content.splitlines())
                    write_output(content)
                
                # Write closing code fence
                write_output("```")
                    
            except Exception as e:
                write_output(f"Error reading {file_path}: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Print contents of all files in a directory')
    parser.add_argument('--dir', default='.', help='Directory to search (default: current directory)')
    parser.add_argument('--ext', nargs='+', help='File extensions to include (e.g., .rs .py)')
    parser.add_argument('--exclude', nargs='+', help='Glob patterns to exclude (e.g., *.pyc target/**)')
    parser.add_argument('--output', help='Output file path (default: print to console)')
    parser.add_argument('--verbose', action='store_true', help='Print debug information')
    
    args = parser.parse_args()
    
    print_file_contents(
        args.dir, 
        args.ext, 
        args.exclude,
        args.output,
        args.verbose
    )
