#!/usr/bin/python3
"""
markdown2html module
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts a Markdown file to an HTML file with support for various Markdown features.
    """
    try:
        with open(markdown_file, 'r') as md_file:
            markdown_content = md_file.readlines()

        html_content = ""
        in_list = False
        in_ordered_list = False

        for line in markdown_content:
            line = line.strip()
            
            # Heading Handling
            if line.startswith("#"):
                heading_level = len(line.split(' ')[0])
                heading_text = line[heading_level:].strip()
                html_content += f"<h{heading_level}>{heading_text}</h{heading_level}>\n"
            
            # Unordered List Handling
            elif line.startswith("- "):
                if not in_list:
                    html_content += "<ul>\n"
                    in_list = True
                list_item = line[2:].strip()
                html_content += f"    <li>{list_item}</li>\n"
            
            # Ordered List Handling
            elif line.startswith("* "):
                if not in_ordered_list:
                    html_content += "<ol>\n"
                    in_ordered_list = True
                list_item = line[2:].strip()
                html_content += f"    <li>{list_item}</li>\n"
            
            # Bold and Emphasis Text Handling
            else:
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
                
                # Custom syntax handling
                line = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), line)
                line = re.sub(r'\(\((.*?)\)\)', lambda match: re.sub(r'[cC]', '', match.group(1)), line)
                
                if in_list:
                    html_content += "</ul>\n"
                    in_list = False
                if in_ordered_list:
                    html_content += "</ol>\n"
                    in_ordered_list = False
                
                if line:
                    # Handle line breaks within a paragraph
                    if '\n' in line:
                        lines = line.split('\n')
                        paragraph = '<br/>\n'.join(lines)
                    else:
                        paragraph = line
                    html_content += f"<p>\n{paragraph}\n</p>\n"

        with open(html_file, 'w') as html_file:
            html_file.write(f"<html>\n<body>\n{html_content}</body>\n</html>\n")

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

