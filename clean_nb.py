import nbformat as nbf

p = "MyNotebook.ipynb"
nb = nbf.read(p, as_version=4)

# remove top-level widget metadata
nb.metadata.pop("widgets", None)
nb.metadata.pop("application/vnd.jupyter.widget-state+json", None)

BAD_MIMES = {
    "application/vnd.jupyter.widget-view+json",
    "application/vnd.jupyter.widget-state+json",
}

for c in nb.cells:
    # drop cell-level widget metadata
    if isinstance(c.get("metadata"), dict):
        c.metadata.pop("widgets", None)

    # nuke ALL code outputs & execution count (safest for GitHub rendering)
    if c.get("cell_type") == "code":
        c["outputs"] = []
        c["execution_count"] = None

    # scrub widget MIME if it appears in attachments or source text
    if isinstance(c.get("attachments"), dict):
        for att in c["attachments"].values():
            if isinstance(att, dict):
                for m in list(att.keys()):
                    if m in BAD_MIMES:
                        att.pop(m, None)

    src = c.get("source", "")
    if isinstance(src, list): src = "".join(src)
    for m in BAD_MIMES:
        src = src.replace(m, "")
    c["source"] = src

nbf.write(nb, p)
print("✅ cleaned", p)
