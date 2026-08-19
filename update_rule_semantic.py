rule_content = """---
name: update-changelog
description: Enforces semantic release version increments (v1.4.3 -> v1.4.4) on every update and full in-app Changelog page maintenance.
---

# Semantic Versioning & Changelog Maintenance Rule

Whenever you make any change or push an update to GitHub:

1. **Increment the Semantic Release Version (`vX.Y.Z`)**:
   - On EVERY SINGLE update/push, increment the semantic release version number (e.g. `v1.4.2` -> `v1.4.3` -> `v1.4.4` -> `v1.4.5`).
   - In `fastapi_app/templates/index.html`:
     - Create a new distinct `<h2 id="v1-4-X">v1.4.X</h2>` section under Release Notes.
     - Move the `(Latest)` label to the new version in the Left Sidebar.
     - Update the Table of Contents (TOC) with the new `v1.4.X Release`.
     - Update the `changelogAnchors` in `main.js` to include the new version anchor.

2. **Increment the Asset Cache-Buster Version (`?v=XX`)**:
   - Increment the asset version query parameter (e.g. `main.js?v=49` -> `main.js?v=50`) in both `fastapi_app/templates/index.html` and `fastapi_app/static/main.js`.

3. **Document All Changes Under the New Version Block**:
   - Add all new features, improvements, UI/UX refinements, and fixes as `<li>` items under the new version block.
   - Categorize each change using badges (`Feature`, `Improvement`, `Fix`, `UI/UX`).

4. **Git Commit Message**:
   - Explicitly mention both the semantic version and commit tag (e.g. `git commit -m "Release: v1.4.3 - Fix Nodes inventory table, add Audit Log search & CSV export (v50)"`).
"""

with open(r'C:\Users\stajyer\.gemini\config\rules\update-changelog.md', 'w', encoding='utf-8') as f:
    f.write(rule_content)

print("Updated rule file with strict semantic version increment requirement")
