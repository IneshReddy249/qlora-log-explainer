import nbformat as nbf
from pathlib import Path

p = Path("MyNotebook.ipynb")
nb = nbf.read(p, as_version=4)

# Remove top-level widget metadata (two common forms)
nb.metadata.pop("widgets", None)
nb.metadata.pop("application/vnd.jupyter.widget-state+json", None)

WIDGET_MIMES = {
    "application/vnd.jupyter.widget-view+json",
    "application/vnd.jupyter.widget-state+json",
}

for cell in nb.cells:
    # Drop any cell-level widget metadata
    if isinstance(cell.get("metadata"), dict):
        cell.metadata.pop("widgets", None)

    # Keep outputs, but strip only widget-specific MIME from them
    if cell.cell_type == "code" and "outputs" in cell:
        cleaned = []
        for out in cell.outputs:
            # If this output has a 'data' dict, remove widget MIME keys only
            data = out.get("data")
            if isinstance(data, dict):
                for m in list(data.keys()):
                    if m in WIDGET_MIMES:
                        data.pop(m, None)
                # If after removal the data becomes empty, skip this output
                if not data:
                    continue
            cleaned.append(out)
        cell.outputs = cleaned

    # Also scrub widget MIME from attachments (rare, but safe)
    if isinstance(cell.get("attachments"), dict):
        for att in cell.attachments.values():
            if isinstance(att, dict):
                for m in list(att.keys()):
                    if m in WIDGET_MIMES:
                        att.pop(m, None)

    # Optional: if widget MIME literal strings are in source text, drop them
    src = cell.get("source", "")
    if isinstance(src, list):
        src = "".join(src)
    for m in WIDGET_MIMES:
        if m in src:
            src = src.replace(m, "")
    cell["source"] = src

nbf.write(nb, p)
print("✅ Cleaned widgets but kept normal outputs:", p)
