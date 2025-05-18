# CSV Column Exporter with Substitution for Inkscape

Easily generate multiple customized SVG files from a single template using data from a CSV file. Replace placeholders like `{{name}}` or `{{color}}` in both **text content** and **any SVG attribute** (e.g. `style`, `id`, `x`, `y`, etc.).

Perfect for creating name tags, badges, product labels, certificates, and more — directly inside Inkscape.

---

## ✨ Features

* ✅ Replace text nodes (`<text>`, `<tspan>`)
* ✅ Replace **any attribute** (`fill`, `style`, `id`, `x`, etc.)
* ✅ Case-insensitive and whitespace-tolerant column matching
* ✅ Choose output directory
* ✅ Preview available CSV columns before export
* ✅ File and folder picker support (Inkscape 1.2+)
* ✅ Unicode/UTF-8 safe (emojis included!)

---

## 📦 Installation

1. Copy `merge.py` and `merge.inx` to your Inkscape extensions folder:

   * **Windows**:
     `%APPDATA%\Inkscape\extensions\`

   * **Linux/macOS**:
     `~/.config/inkscape/extensions/`

2. Restart Inkscape.

3. You’ll find the extension under:
   **Extensions → Export → CSV Column Exporter**

---

## 🧪 Example

**Template SVG:**

```xml
<text>{{Name}}</text>
<rect style="fill:{{Color}}" />
```

**CSV:**

```csv
Name,Color
Alice,#FF0000
Bob,#00FF00
```

**Result:**

* `Alice.svg` → Red fill with text "Alice"
* `Bob.svg` → Green fill with text "Bob"

---

## 💠 How Substitution Works

Placeholders use double curly braces, like `{{column_name}}`. These will be replaced using values from your CSV.

In the Python source code, the substitution pattern looks like this:

```python
new_text = new_text.replace(f"{{{{{key}}}}}", value)
```

This results in actual placeholders like `{{Name}}` being replaced properly at runtime. The extra braces are needed due to Python’s f-string formatting rules.

---

## 📄 License

MIT License
(c) 2024 Christian Sabourin
Feel free to use, modify, and distribute with attribution.

---

## 💬 Questions or suggestions?

Feel free to submit issues or pull requests. Feedback is welcome!
