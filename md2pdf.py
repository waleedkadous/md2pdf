#!/usr/bin/env python3
"""Convert markdown files to PDF via HTML using headless Chrome.

Usage:
    python md2pdf.py input.md [output.pdf]
    python md2pdf.py input.md  # Creates input.pdf
"""

import re
import subprocess
import sys
from pathlib import Path

import markdown


def preprocess_markdown(content: str) -> str:
    """Normalize markdown by adding blank lines before lists."""
    lines = content.split('\n')
    result = []

    for i, line in enumerate(lines):
        # Check if this line starts a list (unordered or ordered)
        is_list_item = re.match(r'^(\s*)[-*+]\s', line) or re.match(r'^(\s*)\d+\.\s', line)

        if is_list_item and i > 0:
            prev_line = lines[i-1].strip()
            # Add blank line before list if previous line is not blank and not a list item
            prev_is_list = re.match(r'^[-*+]\s', prev_line) or re.match(r'^\d+\.\s', prev_line)
            if prev_line and not prev_is_list:
                result.append('')

        result.append(line)

    return '\n'.join(result)


def convert_md_to_html(md_file: Path, html_file: Path) -> None:
    """Convert markdown file to styled HTML."""
    md_content = md_file.read_text()
    md_content = preprocess_markdown(md_content)

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{md_file.stem}</title>
    <style>
        /* Custom PDF styling */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            font-size: 9pt;
            line-height: 1.8;
            color: #333;
            max-width: 100%;
        }}

        /* Headings */
        h1 {{
            font-size: 14pt;
            font-weight: 600;
            margin-top: 20pt;
            margin-bottom: 10pt;
            color: #1a1a1a;
        }}

        h2 {{
            font-size: 12pt;
            font-weight: 600;
            margin-top: 16pt;
            margin-bottom: 8pt;
            color: #2a2a2a;
        }}

        h3 {{
            font-size: 10pt;
            font-weight: 600;
            margin-top: 12pt;
            margin-bottom: 6pt;
            color: #3a3a3a;
        }}

        h4 {{
            font-size: 9pt;
            font-weight: 600;
            margin-top: 10pt;
            margin-bottom: 5pt;
            color: #4a4a4a;
        }}

        /* Paragraphs */
        p {{
            margin-bottom: 10pt;
        }}

        /* Code blocks */
        pre {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 8pt;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 7pt;
            line-height: 1.6;
            overflow-x: auto;
        }}

        code {{
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 7pt;
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            border-radius: 3px;
        }}

        /* Tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10pt 0;
            font-size: 8pt;
        }}

        th {{
            background-color: #f0f0f0;
            font-weight: 600;
            padding: 8pt;
            text-align: left;
            border: 1px solid #ddd;
        }}

        td {{
            padding: 6pt 8pt;
            border: 1px solid #ddd;
        }}

        /* Lists */
        ul, ol {{
            margin: 8pt 0;
            padding-left: 20pt;
        }}

        li {{
            margin-bottom: 4pt;
        }}

        /* Links */
        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        /* Blockquotes */
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 12pt 0;
            padding-left: 12pt;
            color: #666;
            font-style: italic;
        }}

        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 20pt 0;
        }}

        /* Strong/bold */
        strong {{
            font-weight: 600;
        }}

        /* Emphasis */
        em {{
            font-style: italic;
        }}
    </style>
</head>
<body>
{markdown.markdown(md_content, extensions=['extra', 'sane_lists', 'nl2br'])}
</body>
</html>
"""

    html_file.write_text(html_content)
    print(f"✓ HTML generated: {html_file}")


def convert_html_to_pdf(html_file: Path, pdf_file: Path) -> None:
    """Convert HTML to PDF using headless Chrome."""
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
    ]

    chrome_path = None
    for path in chrome_paths:
        if Path(path).exists():
            chrome_path = path
            break

    if not chrome_path:
        raise RuntimeError(
            "Chrome/Chromium not found. Install Google Chrome or set CHROME_PATH env var."
        )

    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_file.absolute()}",
        str(html_file.absolute()),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Chrome conversion failed: {result.stderr}")

    if pdf_file.exists():
        size_kb = pdf_file.stat().st_size / 1024
        print(f"✓ PDF generated: {pdf_file} ({size_kb:.1f} KB)")
    else:
        raise RuntimeError("PDF file was not created")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"Error: File not found: {md_file}")
        sys.exit(1)

    if not md_file.suffix == ".md":
        print("Warning: Input file doesn't have .md extension")

    # Determine output PDF file
    if len(sys.argv) >= 3:
        pdf_file = Path(sys.argv[2])
    else:
        pdf_file = md_file.with_suffix(".pdf")

    # Create temporary HTML file
    html_file = md_file.with_suffix(".html")

    try:
        # Convert MD -> HTML -> PDF
        convert_md_to_html(md_file, html_file)
        convert_html_to_pdf(html_file, pdf_file)

        print(f"\n✓ Conversion complete: {md_file} -> {pdf_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
