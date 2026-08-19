content = open('fastapi_app/templates/index.html', encoding='utf-8').read()

NEW_ACTIVITY_VIEW = '''<section id="activity-view" class="view-section" style="display: none;">
  <div style="padding: 24px;">
    <!-- Header -->
    <div style="background: white; border: 1px solid var(--border); border-radius: 12px; padding: 16px 24px; margin-bottom: 16px; display: flex; align-items: center;">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 12px;"><path d="M19 3H5C3.9 3 3 3.9 3 5v14c0 1.1.9 2 2 2h7"></path><path d="M3 16l4-4 4 4"></path><path d="M8 11l3-3 3 3"></path><path d="M22 17c0 0-1.5-2.5-4-2.5S14 17 14 17s1.5 2.5 4 2.5S22 17 22 17z"></path><circle cx="18" cy="17" r="1"></circle></svg>
      <h2 style="font-size: 1.25rem; font-weight: 500; color: var(--text-main); margin: 0;">Activity center</h2>
    </div>

    <!-- Tab Panel -->
    <div style="background: white; border: 1px solid var(--border); border-radius: 12px; overflow: hidden;">
      <!-- Tabs -->
      <div style="display: flex; align-items: center; border-bottom: 1px solid #e5e7eb; padding: 0 24px; gap: 0;">
        <button onclick="switchActivityTab('alarms', this)" id="ac-tab-alarms"
          style="padding: 16px 20px; border: none; background: none; cursor: pointer; font-size: 0.9rem; font-weight: 500; color: #6b7280; border-bottom: 2px solid transparent; margin-bottom: -1px;">
          Alarms
        </button>
        <button onclick="switchActivityTab('jobs', this)" id="ac-tab-jobs"
          style="padding: 16px 20px; border: none; background: none; cursor: pointer; font-size: 0.9rem; font-weight: 500; color: #6b7280; border-bottom: 2px solid transparent; margin-bottom: -1px;">
          Jobs
        </button>
        <button onclick="switchActivityTab('audit', this)" id="ac-tab-audit"
          style="padding: 16px 20px; border: none; background: none; cursor: pointer; font-size: 0.9rem; font-weight: 500; color: var(--primary); border-bottom: 2px solid var(--primary); margin-bottom: -1px;">
          Audit Log
        </button>
        <button onclick="switchActivityTab('watchlists', this)" id="ac-tab-watchlists"
          style="padding: 16px 20px; border: none; background: none; cursor: pointer; font-size: 0.9rem; font-weight: 500; color: #6b7280; border-bottom: 2px solid transparent; margin-bottom: -1px; display: flex; align-items: center; gap: 6px;">
          Watchlists
          <span style="background: #7c3aed; color: white; font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Beta</span>
        </button>
      </div>

      <!-- ALARMS Tab -->
      <div id="ac-content-alarms" style="display: none; padding: 0;">
        <table style="width: 100%; border-collapse: collapse;">
          <thead style="background: #f9fafb; border-bottom: 1px solid #e5e7eb;">
            <tr>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Title</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Severity</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Category</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Cluster</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Hostname</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">When</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Actions</th>
            </tr>
          </thead>
          <tbody id="ac-alarms-tbody">
            <tr><td colspan="7" style="text-align: center; padding: 60px 20px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="display: block; margin: 0 auto 16px;"><path d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"></path></svg>
              <p style="color: #9ca3af; font-size: 0.9rem;">You haven&apos;t received alarms yet. When you do, it&apos;ll show up here.</p>
            </td></tr>
          </tbody>
        </table>
      </div>

      <!-- JOBS Tab -->
      <div id="ac-content-jobs" style="display: none; padding: 0;">
        <table style="width: 100%; border-collapse: collapse;">
          <thead style="background: #f9fafb; border-bottom: 1px solid #e5e7eb;">
            <tr>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Title</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Status</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Cluster</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Started by</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">When</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Duration</th>
              <th style="padding: 12px 20px; text-align: left; font-size: 0.85rem; font-weight: 600; color: #374151;">Actions</th>
            </tr>
          </thead>
          <tbody id="ac-jobs-tbody">
            <tr><td colspan="7" style="text-align: center; padding: 40px; color: #9ca3af;">Yükleniyor...</td></tr>
          </tbody>
        </table>
      </div>

      <!-- AUDIT LOG Tab -->
      <div id="ac-content-audit" style="display: block; padding: 0;">
        <table style="width: 100%; border-collapse: collapse;">
          <thead style="background: #f9fafb; border-bottom: 1px solid #e5e7eb;">
            <tr>
              <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em;">Date</th>
              <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em;">User</th>
              <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em;">Action</th>
              <th style="padding: 12px 24px; text-align: left; font-size: 0.8rem; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em;">Details</th>
            </tr>
          </thead>
          <tbody id="activity-tbody">
            <tr><td colspan="4" style="text-align:center; padding: 20px; color: #6b7280;">Yükleniyor...</td></tr>
          </tbody>
        </table>
      </div>

      <!-- WATCHLISTS Tab -->
      <div id="ac-content-watchlists" style="display: none; padding: 60px 20px; text-align: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5" style="display: block; margin: 0 auto 16px;"><path d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"></path><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
        <p style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 8px;">Watchlists is a Beta feature.</p>
        <p style="color: #d1d5db; font-size: 0.8rem;">Monitor specific metrics and get notified when thresholds are exceeded.</p>
      </div>
    </div>
  </div>
</section>

      '''

# Replace old section
start_idx = 15527
end_idx = 17784

# Find end of section more precisely - right before <!-- OPERATIONAL REPORTS VIEW -->
new_content = content[:start_idx] + NEW_ACTIVITY_VIEW + content[end_idx:]

with open('fastapi_app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replaced activity-view section")
print(f"Old length: {end_idx - start_idx}, New length: {len(NEW_ACTIVITY_VIEW)}")
