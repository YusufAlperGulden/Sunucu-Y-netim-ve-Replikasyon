rule_content = """---
name: update-changelog
description: Enforces version number increments on every GitHub push and documentation in the in-app Changelog page.
---

# Versioning & Changelog Maintenance Rule

Whenever you prepare and push an update to GitHub:

1. **Increment the Version Number (`?v=XX`)**:
   - On EVERY SINGLE git push, increment the asset version query parameter (e.g. `main.js?v=48` -> `main.js?v=49`) in both `fastapi_app/templates/index.html` and `fastapi_app/static/main.js`.
   - Never push an update without bumping this version number.

2. **Update the In-App Changelog**:
   - You MUST update the `changelog-view` section inside `fastapi_app/templates/index.html`.
   - Add a new `<li>` entry describing the change clearly.
   - Categorize each change using standard badges (`Feature`, `Improvement`, `Fix`, `UI/UX`).
   - Ensure the change is added under the active version block (e.g. `v1.4.2`) or create a new release section if a new milestone is reached.
   - Ensure Table of Contents (TOC) navigation links and anchor IDs (`id="whats-new"`, `id="release-cycle"`, etc.) remain synchronized.

3. **Git Commit Message**:
   - Mention the version number in the commit message (e.g. `git commit -m "Feature: ... (v49)"`).
"""

with open(r'C:\Users\stajyer\.gemini\config\rules\update-changelog.md', 'w', encoding='utf-8') as f:
    f.write(rule_content)

print("Successfully updated update-changelog.md rule file")
