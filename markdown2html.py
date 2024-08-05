#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts a Markdown file to an HTML file.
    """
    try:
        with open(markdown_file, 'r') as md_file:
            markdown_content = md_file.read()

        # Basic conversion: wrapping content in HTML tags
        html_content = f"<html>\n<body>\n{markdown_content}\n</body>\n</html>"

        with open(html_file, 'w') as html_file:
            html_file.write(html_content)

    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    convert_markdown_to_html(markdown_file, html_file)
    sys.exit(0)

