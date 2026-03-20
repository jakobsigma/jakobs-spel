# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

OLD = '</header>\n\n<div class="sideOverlay"'

NEW = '''</header>

<div id="siteAnnouncementBanner" style="display:none;position:fixed;top:64px;left:0;right:0;z-index:498;background:linear-gradient(90deg,var(--p2),var(--p0));padding:9px 50px 9px 20px;text-align:center;font-size:13px;font-weight:600;color:#fff;box-shadow:0 2px 12px rgba(123,44,255,.4)">
  <span id="siteAnnouncementText"></span>
  <button onclick="dismissSiteAnnouncement()" style="position:absolute;right:14px;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.2);border:none;color:#fff;width:24px;height:24px;border-radius:50%;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center">\u2715</button>
</div>

<div class="sideOverlay"'''

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print('OK: Added announcement banner HTML')
else:
    print('ERROR: anchor not found')
    idx = html.find('</header>')
    print(repr(html[idx:idx+150]))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done.')
