# CSV Column Exporter with Substitution for Inkscape

Bulk-generate customized SVG files from a template and CSV data. Replace placeholders like `{{name}}` or `{{color}}` in text **or any attribute** (e.g., `style`, `id`, `x`, `y`).

## Features

✅ Replace text nodes (`<text>`, `<tspan>`)  
✅ Replace **any attribute** (`fill`, `style`, `id`, `x`, etc.)  
✅ Choose output directory  
✅ Preview available CSV columns  
✅ Use file and folder pickers (Inkscape 1.2+)  
✅ Unicode/UTF-8 safe

## Installation

Copy `merge.py` and `merge.inx` into your Inkscape extensions folder:

- **Windows**: `%APPDATA%\Inkscape\extensions\`
- **Linux/macOS**: `~/.config/inkscape/extensions/`

Then restart Inkscape. You’ll find the extension under **Extensions → Export → CSV Column Exporter**.

## Example

Template SVG:
```xml
<text>{{Name}}</text>
<rect style="fill:{{Color}}" />
