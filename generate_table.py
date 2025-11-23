#!/usr/bin/env python3
import os

# Change these to match your repo
repo_url = "https://github.com/xs2ranjeet/interview_prep"
branch    = "main"

rows = []
for root, dirs, files in os.walk("."):
    # skip hidden folders, .git, and workflows directory
    # print(f"{root}")
    if root.startswith("./.") or root.startswith("./.github") or root.startswith(".\\.git"):
        continue
    for f in files:
        if f == "generate_table.py":
            continue
        filepath = os.path.join(root, f).replace("\\", "/")
        display_path = filepath[2:] if filepath.startswith("./") else filepath
        github_link = f"{repo_url}/blob/{branch}/{display_path}"
        rows.append(f"| `{display_path}` | [Link]({github_link}) |")

rows.sort()
with open("FILES_TABLE.md", "w", encoding="utf-8") as fh:
    fh.write("# Files in This Repository\n\n")
    fh.write("| File | Link |\n")
    fh.write("|------|------|\n")
    fh.write("\n".join(rows) + "\n")

print("Generated FILES_TABLE.md containing links table.")
