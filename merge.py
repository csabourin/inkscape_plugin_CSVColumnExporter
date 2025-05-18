#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Christian Sabourin
#
# This Inkscape extension is released under the MIT License.
# See the LICENSE file or visit https://opensource.org/licenses/MIT for details.

import csv
import os
import re
import copy
import inkex
from lxml import etree
from inkex.command import inkscape

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

class CSVColumnExporterWithSubstitution(inkex.EffectExtension):
    """
    Inkscape extension to export multiple SVG files based on CSV data,
    with optional text and attribute substitution using double-brace placeholders.
    """

    def add_arguments(self, pars):
        pars.add_argument("--csv_path", type=str, help="Path to CSV file")
        pars.add_argument("--column_name", type=str, help="Column to use for filename")
        pars.add_argument("--output_dir", type=str, help="Folder where output files go")
        pars.add_argument("--enable_substitution", type=inkex.Boolean, default=False, help="Substitute text in SVG")
        pars.add_argument("--preview_columns", type=inkex.Boolean, default=False, help="Preview column headers only")

    def effect(self):
        try:
            self.process_csv()
        except Exception as e:
            import traceback
            self.msg("💥 An error occurred:\n" + traceback.format_exc())

    def process_csv(self):
        csv_path = self.options.csv_path
        col_name = self.options.column_name
        output_dir = self.options.output_dir.strip() or self.absolute_tempdir()
        substitute = self.options.enable_substitution
        preview = self.options.preview_columns

        if not os.path.isfile(csv_path):
            raise inkex.AbortExtension("❌ CSV file not found: " + csv_path)

        with open(csv_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            headers_raw = reader.fieldnames

            if not headers_raw:
                raise inkex.AbortExtension("❌ No headers found in CSV.")

            headers_map = {(h.strip().lower() if h else ""): h for h in headers_raw if h}
            normalized_headers = list(headers_map.keys())

            self.msg("📋 Available columns:")
            for h in headers_raw:
                if h:
                    self.msg(f"• {h.strip()}")

            if preview:
                self.msg("✅ Preview mode enabled — no exports were made.")
                return

            lookup_col = col_name.strip().lower()
            if lookup_col not in headers_map:
                raise inkex.AbortExtension(f"❌ Column '{col_name}' not found. (Checked against: {', '.join(normalized_headers)})")

            actual_col = headers_map[lookup_col]

            if not os.path.exists(output_dir):
                self.msg(f"ℹ️ Output folder not found. Attempting to create: {output_dir}")
                os.makedirs(output_dir, exist_ok=True)

            success_count = 0
            skipped_count = 0

            for i, row in enumerate(reader):
                if row is None:
                    self.msg(f"⚠️ Skipping row {i+1}: empty or malformed.")
                    skipped_count += 1
                    continue

                clean_row = {}
                for k, v in row.items():
                    if k is None:
                        continue
                    key = k.strip().lower()
                    val = v.strip() if v else ""
                    clean_row[key] = val

                if lookup_col not in clean_row or not clean_row[lookup_col]:
                    self.msg(f"⚠️ Row {i+1} missing or empty value for column '{col_name}'. Skipping.")
                    skipped_count += 1
                    continue

                raw_name = clean_row[lookup_col]
                file_name = sanitize_filename(raw_name)
                base_name = file_name
                counter = 1
                out_path = os.path.join(output_dir, f"{file_name}.svg")

                while os.path.exists(out_path):
                    file_name = f"{base_name}_{counter}"
                    out_path = os.path.join(output_dir, f"{file_name}.svg")
                    counter += 1

                temp_doc = copy.deepcopy(self.document)

                if substitute:
                    self.perform_substitution(temp_doc, clean_row)

                with open(out_path, 'wb') as out_file:
                    temp_doc.write(out_file)

                self.msg(f"✔ Exported: {out_path}")
                success_count += 1

            self.msg(f"✅ Export complete: {success_count} files created, {skipped_count} rows skipped.")

# Substitution uses double-brace placeholders like {{key}}, a common convention in templating engines.
# To render a literal {{ and }} in a Python f-string, we must write '{{{{' and '}}}}'.
# So f"{{{{{key}}}}}" becomes {{key}} at runtime.
  
    def perform_substitution(self, doc, row_data):
        """
        Replace all occurrences of {{key}} in text and attributes with corresponding CSV values.
        Double braces are used to avoid clashing with Python formatting or other templating syntaxes.
        """
        for elem in doc.iter():
            if elem.text:
                new_text = elem.text
                for key, value in row_data.items():
                    new_text = new_text.replace(f"{{{{{key}}}}}", value)
                elem.text = new_text

            for attr_name, attr_value in elem.attrib.items():
                new_attr = attr_value
                for key, value in row_data.items():
                    new_attr = new_attr.replace(f"{{{{{key}}}}}", value)
                elem.attrib[attr_name] = new_attr

if __name__ == '__main__':
    CSVColumnExporterWithSubstitution().run()
