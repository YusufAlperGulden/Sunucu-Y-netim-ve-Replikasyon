import re

html_path = 'fastapi_app/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# For all backups
old_all_backups = """<table class="data-table">
                        <thead>
                            <tr>
                                <th>Cluster</th>
                                <th>Status</th>
                                <th>Size</th>
                                <th>Type</th>
                                <th>Created</th>
                                <th>Completed</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>PostgreSQL-HA-Cluster</td>
                                <td><span class="status-badge status-online">Completed</span></td>
                                <td>15 GB</td>
                                <td>Full</td>
                                <td>2024-03-15 02:00</td>
                                <td>2024-03-15 02:45</td>
                                <td>
                                    <button class="btn-icon">↺</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>"""

new_all_backups = """<table class="data-table">
                        <thead>
                            <tr>
                                <th>Cluster</th>
                                <th>Status</th>
                                <th>Size</th>
                                <th>Type</th>
                                <th>Created</th>
                                <th>Completed</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="all-backups-tbody">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>"""

content = content.replace(old_all_backups, new_all_backups)

# For schedules
old_schedules = """<table class="data-table">
                        <thead>
                            <tr>
                                <th>Schedule</th>
                                <th>Type</th>
                                <th>Cluster</th>
                                <th>Retention</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Daily at 02:00 AM</td>
                                <td>Full Backup</td>
                                <td>PostgreSQL-HA-Cluster</td>
                                <td>7 days</td>
                                <td><button class="btn-icon">✎</button></td>
                            </tr>
                        </tbody>
                    </table>"""

new_schedules = """<table class="data-table">
                        <thead>
                            <tr>
                                <th>Schedule</th>
                                <th>Type</th>
                                <th>Cluster</th>
                                <th>Retention</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="schedules-tbody">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>"""

content = content.replace(old_schedules, new_schedules)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated HTML table bodies for backups")
