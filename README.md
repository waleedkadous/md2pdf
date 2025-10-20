# md2pdf

Convert Markdown files to beautifully styled PDFs using headless Chrome.

## Features

- 🎨 Clean, professional styling with GitHub-inspired theme
- 📊 Support for tables, code blocks, and fenced code
- 🚀 Fast conversion using headless Chrome
- 💻 Cross-platform (macOS, Linux)
- 📝 Preserves markdown formatting and structure

## Installation

### Prerequisites

- Python 3.9 or higher
- Google Chrome or Chromium browser

### Install

```bash
pip install md2pdf-converter
```

Or install from source:

```bash
git clone https://github.com/waleedkadous/md2pdf.git
cd md2pdf
pip install -e .
```

## Usage

### Command Line

```bash
# Convert markdown to PDF (creates input.pdf)
md2pdf input.md

# Specify output filename
md2pdf input.md output.pdf
```

### Python API

```python
from pathlib import Path
from md2pdf import convert_md_to_html, convert_html_to_pdf

md_file = Path("input.md")
html_file = Path("temp.html")
pdf_file = Path("output.pdf")

# Convert markdown to HTML
convert_md_to_html(md_file, html_file)

# Convert HTML to PDF
convert_html_to_pdf(html_file, pdf_file)
```

## Styling

The generated PDFs use a clean, professional style with:

- Sans-serif fonts (system default)
- Blue headers and accents (#0066cc)
- Syntax-highlighted code blocks
- Responsive tables
- Proper spacing and margins

## Requirements

- `markdown>=3.9` - Markdown processing library
- Google Chrome or Chromium (for PDF generation)

## How It Works

1. **Markdown → HTML**: Converts markdown to styled HTML using Python's `markdown` library
2. **HTML → PDF**: Uses headless Chrome to render and print the HTML to PDF

## Examples

### Convert a single file

```bash
md2pdf README.md
```

### Convert with custom output

```bash
md2pdf report.md /path/to/output.pdf
```

### Batch conversion

```bash
for f in *.md; do md2pdf "$f"; done
```

## Limitations

- Requires Chrome/Chromium to be installed
- Chrome path is auto-detected from common locations:
  - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
  - Linux: `/usr/bin/google-chrome`, `/usr/bin/chromium-browser`, `/usr/bin/chromium`

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Author

Waleed Kadous

## Acknowledgments

Created as part of the RAGDiff project for generating comparison reports.
