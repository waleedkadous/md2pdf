# md2pdf Project Instructions

## Package Management

**This project uses uv for package management.**

- **Installing dependencies**: `uv pip install -e .`
- **Adding new dependencies**: Update `pyproject.toml` and run `uv pip install -e .`
- **DO NOT use pip directly** - always use uv commands

## Testing the Converter

To test the markdown to PDF conversion:

```bash
uv run python md2pdf.py example.md
```

Or after installing in development mode:

```bash
md2pdf example.md
```
