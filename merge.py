import csv
import os
import re
import copy
import inkex
from lxml import etree
from inkex.command import inkscape

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

class CycleExport(inkex.EffectExtension):

    def add_arguments(self, pars):
        pars.add_argument("--csv_path", type=str, help="Path to CSV file")
        pars.add_argument("--column_name", type=str, help="Column to use for filename")
        pars.add_argument("--output_dir", type=str, help="Folder where output files go")
        pars.add_argument("--enable_substitution", type=inkex.Boolean, default=False, help="Substitute text in SVG")
        pars.add_argument("--preview_columns", type=inkex.Boolean, default=False, help="Preview column headers only")

    def effect(self):
        try:
            csv_path = self.options.csv_path
            col_name = self.options.column_name
            output_dir = self.options.output_dir.strip() or self.absolute_tempdir()
            substitute = self.options.enable_substitution
            preview = self.options.preview_columns

            if not os.path.isfile(csv_path):
                self.msg("❌ CSV file not found: " + csv_path)
                return

            with open(csv_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                # Normalize headers: strip and lowercase
                headers_raw = reader.fieldnames
                if not headers_raw:
                    self.msg("❌ No headers found in CSV.")
                    return

                # Map normalized headers to original ones for value access
                headers_map = {h.strip().lower(): h for h in headers_raw}
                normalized_headers = list(headers_map.keys())

                self.msg("📋 Available columns:")
                for h in headers_raw:
                    self.msg(f"• {h.strip()}")

                if preview:
                    self.msg("✅ Preview mode enabled — no exports were made.")
                    return

                lookup_col = col_name.strip().lower()
                if lookup_col not in headers_map:
                    self.msg(f"❌ Column '{col_name}' not found. (Checked against: {', '.join(normalized_headers)})")
                    return

                actual_col = headers_map[lookup_col]

                if not os.path.isdir(output_dir):
                    self.msg("❌ Output folder does not exist: " + output_dir)
                    return

                for i, row in enumerate(reader):
                    # Use normalized keys and strip cell values
                    row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}
                    
                    raw_name = row.get(actual_col, "").strip()
                    if not raw_name:
                        self.msg(f"⚠️ Row {i+1} has empty value for '{col_name}'. Skipping.")
                        continue

                    file_name = sanitize_filename(raw_name)
                    out_path = os.path.join(output_dir, f"{file_name}.svg")

                    temp_doc = copy.deepcopy(self.document)

                    if substitute:
                        self.perform_substitution(temp_doc, row)

                    with open(out_path, 'wb') as out_file:
                        temp_doc.write(out_file)

                    self.msg(f"✔ Exported: {out_path}")


        except Exception as e:
            import traceback
            self.msg("💥 An error occurred:\n" + traceback.format_exc())


    def perform_substitution(self, doc, row_data):
    # Normalize keys in case user used inconsistent casing or spacing
        normalized_row = {k.strip().lower(): v.strip() for k, v in row_data.items()}

        for elem in doc.iter():
            if elem.text:
                new_text = elem.text
                for key, value in normalized_row.items():
                    new_text = new_text.replace(f"{{{{{key}}}}}", value)
                elem.text = new_text

            for attr_name, attr_value in elem.attrib.items():
                new_attr = attr_value
                for key, value in normalized_row.items():
                    new_attr = new_attr.replace(f"{{{{{key}}}}}", value)
                elem.attrib[attr_name] = new_attr




if __name__ == '__main__':
    CycleExport().run()
