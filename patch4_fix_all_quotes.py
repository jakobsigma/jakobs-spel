# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and fix all the broken onclick strings in _renderProfileCard
# The pattern is: ''+ variable +'' when it should be \\'+ variable +\\'

# Fix 1: removeFriend onclick
OLD1 = "actionsHTML='<button onclick=\"removeFriend(''+username+'');closeViewProfile();toast('V\xe4n borttagen')"
NEW1 = "actionsHTML='<button onclick=\"removeFriend(\\'' + username + '\\');closeViewProfile();toast(\\'V\xe4n borttagen\\')"

if OLD1 in html:
    html = html.replace(OLD1, NEW1, 1)
    print('OK: Fixed removeFriend onclick')
else:
    print('ERROR: removeFriend onclick not found as expected')
    # Look for it
    import re
    m = re.search(r"actionsHTML='<button onclick=\"removeFriend\([^)]+\)", html)
    if m:
        print('Found:', repr(m.group()))

# Fix 2: addFriendDirect onclick
OLD2 = "actionsHTML='<button onclick=\"addFriendDirect(''+username+'');closeViewProfile();toast('+V\xe4n tillagd \u2728','ok')"
NEW2 = "actionsHTML='<button onclick=\"addFriendDirect(\\'' + username + '\\');closeViewProfile();toast(\\'+V\xe4n tillagd \u2728\\',\\'ok\\')"

if OLD2 in html:
    html = html.replace(OLD2, NEW2, 1)
    print('OK: Fixed addFriendDirect onclick')
else:
    print('ERROR: addFriendDirect onclick not found as expected')
    import re
    m = re.search(r"actionsHTML='<button onclick=\"addFriendDirect\([^)]+\)", html)
    if m:
        print('Found:', repr(m.group()))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done.')
