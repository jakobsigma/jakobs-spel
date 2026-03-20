# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The buggy line uses '' (empty string concatenation) instead of escaped single quotes
# Found at: '      pinsHTML+=\'<div class="pc-pin-item" onclick="closeViewProfile();openGameByFile(\'\'+p.f+\'\')">🎮 \'+p.name+\'</div>\';'
# The fix: use \' inside the onclick string

OLD_PIN = """      pinsHTML+='<div class="pc-pin-item" onclick="closeViewProfile();openGameByFile(''+p.f+'')">""" + "\U0001F3AE" + """ '+p.name+'</div>';"""

# The correct version uses backslash-escaped single quotes
NEW_PIN = r"""      pinsHTML+='<div class="pc-pin-item" onclick="closeViewProfile();openGameByFile(\''+p.f+'\')">""" + "\U0001F3AE" + r""" '+p.name+'</div>';"""

print('Looking for:', repr(OLD_PIN))

if OLD_PIN in html:
    html = html.replace(OLD_PIN, NEW_PIN, 1)
    print('OK: Fixed pin item onclick quotes')
else:
    print('ERROR: Not found with emoji. Trying without...')
    # Find via position
    idx = html.find('pinsHTML+=\'<div class="pc-pin-item"')
    if idx >= 0:
        end_idx = html.find("+'</div>';", idx)
        if end_idx >= 0:
            found = html[idx:end_idx+10]
            print('Found:', repr(found))
            # Replace specifically
            new_text = "pinsHTML+='<div class=\"pc-pin-item\" onclick=\"closeViewProfile();openGameByFile(\\'' + p.f + '\\')\">\\U0001F3AE '+p.name+'</div>';"
            html = html[:idx] + new_text + html[end_idx+10:]
            print('Fixed via position')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done.')
