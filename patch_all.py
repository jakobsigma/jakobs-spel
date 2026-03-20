# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
print(f'Original file size: {original_len} chars')

errors = []

def do_replace(label, old, new, html, count=1):
    if old not in html:
        errors.append(f'NOT FOUND: {label}')
        print(f'ERROR - NOT FOUND: {label}')
        print(f'  Looking for: {repr(old[:80])}')
        return html
    if count == 1:
        result = html.replace(old, new, 1)
    else:
        result = html.replace(old, new)
    print(f'OK: {label}')
    return result

# ============================================================
# FEATURE 3: CSS additions (do this first - anchor is clear)
# ============================================================

CSS_ANCHOR = '.gameQuestWidgetFill{height:100%;background:linear-gradient(90deg,var(--p0),var(--p1));border-radius:2px;transition:width .5s;}'

NEW_CSS = '''.gameQuestWidgetFill{height:100%;background:linear-gradient(90deg,var(--p0),var(--p1));border-radius:2px;transition:width .5s;}
.pc-status{font-size:12px;color:var(--d);display:flex;align-items:center;gap:5px;margin:2px 0 4px;}
.pc-status-dot{width:8px;height:8px;border-radius:50%;background:#3ba55c;flex-shrink:0;box-shadow:0 0 6px #3ba55c;}
.pc-bio{font-size:12px;color:var(--m);background:rgba(255,255,255,.04);border-radius:8px;padding:8px 10px;margin:6px 0;border-left:2px solid var(--p0);line-height:1.5;}
.pc-showcase-title{font-size:10px;color:var(--d);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;}
.pc-showcase{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:4px;}
.pc-showcase-item{background:rgba(123,44,255,.12);border:1px solid var(--line);border-radius:10px;padding:6px 10px;font-size:11px;text-align:center;color:var(--m);}
.pc-pins{display:flex;flex-direction:column;gap:4px;margin-bottom:4px;}
.pc-pin-item{background:rgba(123,44,255,.08);border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:12px;color:var(--m);cursor:pointer;transition:background .2s;}
.pc-pin-item:hover{background:rgba(123,44,255,.2);}'''

html = do_replace('CSS additions', CSS_ANCHOR, NEW_CSS, html)

# ============================================================
# FEATURE 6: Announcement banner HTML (after </header>)
# ============================================================

AFTER_HEADER = '</header>\n\n<div class="sidebar"'

ANN_BANNER_HTML = '''</header>

<div id="siteAnnouncementBanner" style="display:none;position:fixed;top:64px;left:0;right:0;z-index:498;background:linear-gradient(90deg,var(--p2),var(--p0));padding:9px 50px 9px 20px;text-align:center;font-size:13px;font-weight:600;color:#fff;box-shadow:0 2px 12px rgba(123,44,255,.4)">
  <span id="siteAnnouncementText"></span>
  <button onclick="dismissSiteAnnouncement()" style="position:absolute;right:14px;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.2);border:none;color:#fff;width:24px;height:24px;border-radius:50%;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center">\u2715</button>
</div>

<div class="sidebar"'''

html = do_replace('Announcement banner HTML', AFTER_HEADER, ANN_BANNER_HTML, html)

# ============================================================
# FEATURE 4: Soundboard HTML (before chatOverlay)
# ============================================================

BEFORE_CHAT = '''<div class="chatOverlay" id="chatOverlay" onclick="if(event.target===this)closeChat()">
  <div class="chatBox">
    <div class="chatHead"><h3 data-i18n="chatTitle">\U0001F4AC Chat</h3><button class="closeBtn" onclick="closeChat()">\u2715</button></div>
    <div class="chatMessages" id="chatMessages"></div>
    <div class="chatInputRow">
      <input type="text" id="chatInput" data-i18n-ph="chatPlaceholder" placeholder="Write a message..." onkeydown="chatKey(event)" maxlength="250">
      <button class="pill primary" onclick="sendChat()" style="padding:8px 14px;flex-shrink:0" data-i18n="sendBtn">Send</button>
    </div>
  </div>
</div>'''

SOUNDBOARD_AND_CHAT = '''<div class="appOverlay" id="soundboardOverlay" onclick="if(event.target===this)closeSoundboardWindow()">
  <div class="appWin" id="soundboardWin" style="width:min(820px,95vw);height:min(620px,92vh)">
    <div class="winBar" id="soundboardWinBar">
      <div class="winBar-title"><span class="winBar-icon">\U0001F3B5</span> Soundboard</div>
      <div class="winBar-controls">
        <button class="winBtn wClose" onclick="closeSoundboardWindow()">\u2715</button>
      </div>
    </div>
    <div class="appBody" style="padding:0">
      <iframe id="soundboardFrame" src="" style="width:100%;height:100%;border:none;display:block" allowfullscreen></iframe>
    </div>
  </div>
</div>

<div class="appOverlay" id="chatOverlay" onclick="if(event.target===this)closeChat()">
  <div class="appWin" id="chatWin" style="width:min(440px,95vw);height:min(540px,88vh);display:flex;flex-direction:column">
    <div class="winBar" id="chatWinBar">
      <div class="winBar-title"><span class="winBar-icon">\U0001F4AC</span> <span data-i18n="chatTitle">Chat</span></div>
      <div class="winBar-controls">
        <button class="winBtn wClose" onclick="closeChat()">\u2715</button>
      </div>
    </div>
    <div style="flex:1;overflow-y:auto;min-height:0" class="chatMessages" id="chatMessages"></div>
    <div class="chatInputRow" style="flex-shrink:0;padding:8px;border-top:1px solid var(--line)">
      <input type="text" id="chatInput" data-i18n-ph="chatPlaceholder" placeholder="Write a message..." onkeydown="chatKey(event)" maxlength="250">
      <button class="pill primary" onclick="sendChat()" style="padding:8px 14px;flex-shrink:0" data-i18n="sendBtn">Send</button>
    </div>
  </div>
</div>'''

html = do_replace('Soundboard + Chat HTML', BEFORE_CHAT, SOUNDBOARD_AND_CHAT, html)

# ============================================================
# FEATURE 2: Profile Edit Modal HTML (before </body>)
# ============================================================

BEFORE_BODY_END = '</body>\n</html>'

PROFILE_MODAL_HTML = '''<div class="modal" id="profileEditModal" style="z-index:4000">
  <div class="modalBox" style="width:min(420px,94vw)">
    <h2>\u270F\uFE0F Redigera profil</h2>
    <div class="formGroup">
      <label>Status (max 60 tecken)</label>
      <input id="pemStatus" maxlength="60" placeholder="\U0001F7E2 Online och spelar...">
    </div>
    <div class="formGroup">
      <label>Bio / About me (max 150 tecken)</label>
      <textarea id="pemBio" maxlength="150" placeholder="Ber\xe4tta om dig sj\xe4lv..." style="width:100%;background:rgba(255,255,255,.07);border:1px solid var(--line);border-radius:10px;padding:10px 13px;color:var(--w);font-size:13px;font-family:inherit;resize:vertical;min-height:70px"></textarea>
    </div>
    <div class="formGroup">
      <label>Featured item ID (l\xe4mna tomt f\xf6r inget)</label>
      <input id="pemFeatured" placeholder="t.ex. frame_gold">
    </div>
    <div class="formRow">
      <button class="pill primary" onclick="saveProfileEdit()" style="flex:1">\U0001F4BE Spara</button>
      <button class="pill ghost" onclick="closeProfileEditModal()" style="flex:1">Avbryt</button>
    </div>
  </div>
</div>

</body>
</html>'''

html = do_replace('Profile Edit Modal HTML', BEFORE_BODY_END, PROFILE_MODAL_HTML, html)

# ============================================================
# FEATURE 8: Leaderboard + Achievements panel divs in sidebar
# ============================================================

OLD_PANELS = '''    <div class="sidePanel" id="panel_admin"></div>'''

NEW_PANELS = '''    <div class="sidePanel" id="panel_admin"></div>
    <div class="sidePanel" id="panel_leaderboard"></div>
    <div class="sidePanel" id="panel_achievements"></div>'''

html = do_replace('Add leaderboard+achievements panel divs', OLD_PANELS, NEW_PANELS, html)

# ============================================================
# FEATURE 4+8+10: Sidebar nav buttons
# ============================================================

OLD_NAV_CHAT = '''    <button class="sideNavBtn" onclick="closeSidebar();openChat()"><span class="sideNavIcon">\U0001F4AC</span><span class="sideNavLabel" data-i18n="nav_chat">Chat</span></button>'''

NEW_NAV_CHAT = '''    <button class="sideNavBtn" onclick="openSoundboardWindow()"><span class="sideNavIcon">\U0001F3B5</span><span class="sideNavLabel">Soundboard</span></button>
    <button class="sideNavBtn" onclick="closeSidebar();openChat()"><span class="sideNavIcon">\U0001F4AC</span><span class="sideNavLabel" data-i18n="nav_chat">Chat</span></button>
    <button class="sideNavBtn" onclick="switchSideTab('leaderboard')"><span class="sideNavIcon">\U0001F3C6</span><span class="sideNavLabel">Leaderboard</span></button>
    <button class="sideNavBtn" onclick="switchSideTab('achievements')"><span class="sideNavIcon">\U0001F3C5</span><span class="sideNavLabel">Achievements</span></button>'''

html = do_replace('Add Soundboard+Leaderboard+Achievements nav buttons', OLD_NAV_CHAT, NEW_NAV_CHAT, html)

# ============================================================
# FEATURE 9: Rating HTML in igp-side
# ============================================================

OLD_GAME_SUB_INFO = '      <div id="gameSubInfo" style="font-size:11px;color:var(--d);text-align:center;margin-top:4px"></div>\n    </div>\n  </div>\n</div>'

NEW_GAME_SUB_INFO = '''      <div id="gameSubInfo" style="font-size:11px;color:var(--d);text-align:center;margin-top:4px"></div>
      <div id="igpRating" style="background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin-top:4px">
        <div style="font-size:10px;color:var(--d);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">\u2B50 Betygs\xe4tt</div>
        <div id="igpRatingStars" style="display:flex;align-items:center;gap:2px"></div>
      </div>
    </div>
  </div>
</div>'''

html = do_replace('Rating HTML in igp-side', OLD_GAME_SUB_INFO, NEW_GAME_SUB_INFO, html)

# ============================================================
# JS SECTION: Add all new JS functions
# ============================================================

# Find a good anchor - before function _renderProfileCard
OLD_BEFORE_RENDER = 'function _renderProfileCard(card,username){'

PROFILE_EXT_JS = '''function getProfileExt(username){
  return JSON.parse(localStorage.getItem('profile_ext_'+username)||'{}');
}
function setProfileExt(data){
  if(!state.user)return;
  var existing=getProfileExt(state.user);
  var merged=Object.assign(existing,data);
  localStorage.setItem('profile_ext_'+state.user,JSON.stringify(merged));
}
function ensureJoinDate(){
  if(!state.user)return;
  var ext=getProfileExt(state.user);
  if(!ext.joinDate){
    setProfileExt({joinDate:new Date().toISOString().split('T')[0]});
  }
}
function openProfileEditModal(){
  var ext=getProfileExt(state.user);
  var mo=document.getElementById('profileEditModal');
  if(!mo)return;
  document.getElementById('pemBio').value=ext.bio||'';
  document.getElementById('pemStatus').value=ext.status||'';
  document.getElementById('pemFeatured').value=ext.featuredItem||'';
  mo.style.display='flex';
}
function closeProfileEditModal(){
  var mo=document.getElementById('profileEditModal');
  if(mo)mo.style.display='none';
}
function saveProfileEdit(){
  var bio=document.getElementById('pemBio').value.trim().slice(0,150);
  var status=document.getElementById('pemStatus').value.trim().slice(0,60);
  var featured=document.getElementById('pemFeatured').value.trim();
  setProfileExt({bio:bio,status:status,featuredItem:featured});
  closeProfileEditModal();
  toast('Profil uppdaterad! \u2728','ok');
}
function handleBannerUpload(input){
  if(!input.files||!input.files[0])return;
  var file=input.files[0];
  if(!file.type.startsWith('image/'))return toast('Bara bildfiler','error');
  if(file.size>3145728)return toast('Max 3MB','error');
  var reader=new FileReader();
  reader.onload=function(e){
    setProfileExt({customBanner:e.target.result});
    toast('Banner uppdaterad! \U0001F5BC\uFE0F','ok');
  };
  reader.readAsDataURL(file);
}
function pinCurrentGame(){
  if(_currentGameIdx<0)return toast('\xd6ppna ett spel f\xf6rst','error');
  var g=GAMES[_currentGameIdx];if(!g)return;
  var ext=getProfileExt(state.user);
  var pins=ext.pinnedGames||[];
  if(pins.find(function(p){return p.f===g.f;}))return toast('Redan pinnead','error');
  pins.unshift({name:g.name,f:g.f,cat:g.cat||''});
  if(pins.length>3)pins.pop();
  setProfileExt({pinnedGames:pins});
  toast('Spel pinneat p\xe5 profilen! \U0001F4CC','ok');
}
function unpinGame(f){
  var ext=getProfileExt(state.user);
  var pins=(ext.pinnedGames||[]).filter(function(p){return p.f!==f;});
  setProfileExt({pinnedGames:pins});
  if(document.getElementById('viewProfileOverlay').classList.contains('open'))viewProfile(state.user);
}
function _renderProfileCard(card,username){'''

html = do_replace('Add profile ext JS + new _renderProfileCard start', OLD_BEFORE_RENDER, PROFILE_EXT_JS, html)

# ============================================================
# FEATURE 1B: Replace _renderProfileCard body
# Find the original body and replace with enhanced version
# ============================================================

# The original _renderProfileCard body - find unique markers
OLD_RENDER_BODY_INNER = '''  var uData=JSON.parse(localStorage.getItem("jspel_"+username)||"{}");
  var eq=(uData.settings&&uData.settings.equipped)||{};
  var av=localStorage.getItem("avatar_"+username)||"";
  var level=uData.level||1;
  var coins=isSelf?state.coins:(uData.coins||0);
  var favs=isSelf?state.favorites.length:(uData.favorites||[]).length;
  var friends=JSON.parse(localStorage.getItem("friends_"+username)||"[]");
  var myFriends=state.user?JSON.parse(localStorage.getItem("friends_"+state.user)||"[]"):[];
  var isFriend=myFriends.indexOf(username)>=0;'''

# Find the block after the opening function declaration
# We need to find and replace from that point to the end of the function
idx_render = html.find('function _renderProfileCard(card,username){\n  var uData')
if idx_render < 0:
    # Try after our replacement
    idx_render = html.find('function _renderProfileCard(card,username){\n  var isSelf')
    print(f'_renderProfileCard body search: idx={idx_render}')

# Find the end of the function - look for the closing pattern
if idx_render >= 0:
    # Find the end - look for the Supabase block end
    end_search = html.find('\n}\n', idx_render + 100)
    # But we need the right closing brace - look for the one after Supabase section
    # Search for pattern: "nr.appendChild(ab);\n        }\n      }\n    });\n  }\n}"
    end_pattern = 'nr.appendChild(ab);\n        }\n      }\n    });\n  }\n}'
    idx_end = html.find(end_pattern, idx_render)
    if idx_end >= 0:
        end_of_func = idx_end + len(end_pattern)
        print(f'Found render body: {idx_render} to {end_of_func}')

        NEW_RENDER_FULL = '''function _renderProfileCard(card,username){
  var isSelf=(username===state.user);
  var uData=JSON.parse(localStorage.getItem("jspel_"+username)||"{}");
  var eq=(uData.settings&&uData.settings.equipped)||{};
  var av=localStorage.getItem("avatar_"+username)||"";
  var ext=getProfileExt(username);
  var level=uData.level||1;
  var coins=isSelf?state.coins:(uData.coins||0);
  var favs=isSelf?state.favorites.length:(uData.favorites||[]).length;
  var friends=JSON.parse(localStorage.getItem("friends_"+username)||"[]");
  var myFriends=state.user?JSON.parse(localStorage.getItem("friends_"+state.user)||"[]"):[];
  var isFriend=myFriends.indexOf(username)>=0;
  /* Banner - custom upload takes priority */
  var bannerStyle=ext.customBanner?'background:url('+ext.customBanner+') center/cover no-repeat;':getBannerStyle(eq.effect||null);
  var frameClass=getFrameClass(eq.frame||null);
  var avatarHTML=av
    ?'<img src="'+av+'" class="pc-avatar '+frameClass+'" style="width:72px;height:72px">'
    :'<div class="pc-avatar '+frameClass+'" style="background:var(--p0);width:72px;height:72px">'+username.charAt(0).toUpperCase()+'</div>';
  var nameClass=getNameClass(eq.nameeffect||null);
  var badgesHTML="";
  if(eq.badge)badgesHTML+=getBadgeHTML(eq.badge);
  /* Status */
  var statusHTML=ext.status?'<div class="pc-status"><span class="pc-status-dot"></span>'+ext.status+'</div>':'';
  /* Bio */
  var bioHTML=ext.bio?'<div class="pc-bio">'+ext.bio+'</div>':'';
  /* Join date */
  var joinHTML=ext.joinDate?'<div style="font-size:10px;color:var(--d);margin-top:2px">\U0001F4C5 Gick med '+ext.joinDate+'</div>':'';
  /* Showcase */
  var showcaseItems=[];
  if(eq.frame)showcaseItems.push('<div class="pc-showcase-item" title="Ram">'+getFrameClass(eq.frame).replace('frame-','')+'<br><small>Ram</small></div>');
  if(eq.badge)showcaseItems.push('<div class="pc-showcase-item">'+getBadgeHTML(eq.badge)+'<br><small>Badge</small></div>');
  if(eq.nameeffect)showcaseItems.push('<div class="pc-showcase-item">\u2728<br><small>Namn-effekt</small></div>');
  if(eq.effect)showcaseItems.push('<div class="pc-showcase-item">\U0001F3A8<br><small>Banner</small></div>');
  var showcaseHTML=showcaseItems.length?'<div class="pc-divider"></div><div class="pc-showcase-title">\U0001F3C6 Showcase</div><div class="pc-showcase">'+showcaseItems.join('')+'</div>':'';
  /* Pinned games */
  var pins=ext.pinnedGames||[];
  var pinsHTML='';
  if(pins.length){
    pinsHTML='<div class="pc-divider"></div><div class="pc-showcase-title">\U0001F4CC Pinnade spel</div><div class="pc-pins">';
    pins.forEach(function(p){
      pinsHTML+='<div class="pc-pin-item" onclick="closeViewProfile();openGameByFile(\''+p.f+'\')">\U0001F3AE '+p.name+'</div>';
    });
    pinsHTML+='</div>';
  }
  /* Actions */
  var actionsHTML="";
  if(!isSelf&&state.user){
    if(isFriend){
      actionsHTML='<button onclick="removeFriend(\''+username+'\');closeViewProfile();toast(\'V\xe4n borttagen\')" style="background:rgba(255,50,50,.2);color:#ff6b6b;border:1px solid rgba(255,50,50,.3);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">\u2715 Ta bort v\xe4n</button>';
    }else{
      actionsHTML='<button onclick="addFriendDirect(\''+username+'\');closeViewProfile();toast(\'+V\xe4n tillagd \u2728\',\'ok\')" style="background:var(--p0);color:#fff;flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer;border:none">+ L\xe4gg till v\xe4n</button>';
    }
  }
  if(isSelf){
    actionsHTML='<button onclick="openProfileEditModal()" style="background:var(--p0);color:#fff;border:none;flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">\u270F\ufe0F Redigera</button>';
    actionsHTML+='<label style="background:var(--glass);color:var(--w);border:1px solid var(--line);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer;text-align:center;display:flex;align-items:center;justify-content:center">\U0001F5BC\uFE0F Banner<input type="file" accept="image/*" style="display:none" onchange="handleBannerUpload(this)"></label>';
  }
  actionsHTML+='<button onclick="closeViewProfile()" style="background:var(--glass);color:var(--d);border:1px solid var(--line);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">St\xe4ng</button>';
  var avatarWrapHTML=isSelf
    ?'<label for="pcFileInput" style="cursor:pointer;display:block;position:relative">'+avatarHTML+'<div style="position:absolute;bottom:2px;right:2px;width:22px;height:22px;border-radius:50%;background:var(--p0);display:flex;align-items:center;justify-content:center;font-size:10px;border:2px solid var(--bg1)">\U0001F4F7</div></label>'
    :avatarHTML;
  card.innerHTML=
    '<div class="pc-banner pc-banner-default" style="'+bannerStyle+'">'
    +'<div class="pc-avatar-wrap">'+avatarWrapHTML+'</div>'
    +'<button class="pc-close" onclick="closeViewProfile()">\u2715</button>'
    +'</div>'
    +'<div class="pc-body">'
    +'<div class="pc-name-row"><span class="pc-username '+nameClass+'">'+username+'</span></div>'
    +statusHTML
    +(badgesHTML?'<div class="pc-badges">'+badgesHTML+'</div>':'')
    +'<div class="pc-level">Niv\xe5 '+level+(isSelf?' \xb7 \U0001F9E0 '+state.xp+' XP':'')+'</div>'
    +joinHTML
    +bioHTML
    +'<div class="pc-divider"></div>'
    +'<div class="pc-stats">'
    +'<div class="pc-stat"><span>'+coins+'</span><small>\U0001F4B0 Mynt</small></div>'
    +'<div class="pc-stat"><span>'+favs+'</span><small>\u2b50 Favs</small></div>'
    +'<div class="pc-stat"><span>'+friends.length+'</span><small>\U0001F465 V\xe4nner</small></div>'
    +'</div>'
    +showcaseHTML
    +pinsHTML
    +'<div class="pc-divider"></div>'
    +'<div class="pc-actions">'+actionsHTML+'</div>'
    +(isSelf?'<input type="file" id="pcFileInput" accept="image/*" style="display:none" onchange="handleAvatarUpload(this);closeViewProfile();">':'')
    +'</div>';
  if(_sb&&!isSelf){
    _sb.from("accounts").select("username,is_admin").eq("username",username).single().then(function(res){
      if(res.data&&res.data.is_admin){
        var nr=card.querySelector(".pc-name-row");
        if(nr&&!nr.querySelector(".admin-badge")){
          var ab=document.createElement("span");ab.className="pc-badge admin-badge";
          ab.style.cssText="background:#ff6b0022;color:#ff6b00;border:1px solid #ff6b0055";
          ab.textContent="\U0001F6E1\uFE0F Admin";nr.appendChild(ab);
        }
      }
    });
  }
}
function openGameByFile(f){
  var idx=GAMES.findIndex(function(g){return g.f===f;});
  if(idx>=0)openGame(idx);
}'''

        html = html[:idx_render] + NEW_RENDER_FULL + html[end_of_func:]
        print('OK: Replaced _renderProfileCard body with enhanced version')
    else:
        errors.append('Could not find end of _renderProfileCard')
        print('ERROR: Could not find end of _renderProfileCard')
else:
    errors.append('Could not find _renderProfileCard body start')
    print('ERROR: Could not find _renderProfileCard body start')

# ============================================================
# FEATURE 5: Update openChat/closeChat functions
# ============================================================

OLD_OPEN_CHAT = 'function openChat(){document.getElementById("chatOverlay").classList.add("open");closeSidebar();loadChatMsgs();}'
NEW_OPEN_CHAT = '''function openChat(){
  var ov=document.getElementById("chatOverlay");if(!ov)return;
  _resetWinPos(document.getElementById("chatWin"));
  ov.style.display="flex";
  setTimeout(function(){ov.classList.add("open");},10);
  closeSidebar();loadChatMsgs();
}'''

html = do_replace('Update openChat', OLD_OPEN_CHAT, NEW_OPEN_CHAT, html)

OLD_CLOSE_CHAT = 'function closeChat(){document.getElementById("chatOverlay").classList.remove("open");}'
NEW_CLOSE_CHAT = '''function closeChat(){
  var ov=document.getElementById("chatOverlay");
  if(ov){ov.classList.remove("open");setTimeout(function(){ov.style.display="none";},200);}
}'''

html = do_replace('Update closeChat', OLD_CLOSE_CHAT, NEW_CLOSE_CHAT, html)

# ============================================================
# FEATURE 4: Soundboard JS functions (add near closeInventoryWindow)
# ============================================================

OLD_CLOSE_INV = '''function closeInventoryWindow(){
  var ov=document.getElementById('inventoryOverlay');
  if(ov){ov.classList.remove('open');setTimeout(function(){ov.style.display='none';},200);}
}'''

# If that exact text not found, try alternative
if OLD_CLOSE_INV not in html:
    # Look for it
    idx = html.find('function closeInventoryWindow()')
    if idx >= 0:
        print(f'Found closeInventoryWindow at {idx}: {repr(html[idx:idx+150])}')
    else:
        print('ERROR: closeInventoryWindow not found')

NEW_SOUNDBOARD_AND_CLOSE_INV = '''function closeInventoryWindow(){
  var ov=document.getElementById('inventoryOverlay');
  if(ov){ov.classList.remove('open');setTimeout(function(){ov.style.display='none';},200);}
}
function openSoundboardWindow(){
  var ov=document.getElementById('soundboardOverlay');if(!ov)return;
  _resetWinPos(document.getElementById('soundboardWin'));
  var fr=document.getElementById('soundboardFrame');
  if(fr&&!fr.src.includes('jakobsigma'))fr.src='https://jakobsigma.github.io/Sound-board/';
  ov.style.display='flex';
  setTimeout(function(){ov.classList.add('open');},10);
  closeSidebar();
}
function closeSoundboardWindow(){
  var ov=document.getElementById('soundboardOverlay');
  if(ov){ov.classList.remove('open');setTimeout(function(){ov.style.display='none';},200);}
}'''

html = do_replace('Add Soundboard JS functions', OLD_CLOSE_INV, NEW_SOUNDBOARD_AND_CLOSE_INV, html)

# ============================================================
# FEATURE 6: Announcement JS functions (add near addAnnouncement)
# ============================================================

OLD_ANN_FUNCS = "function addAnnouncement(){var inp=document.getElementById('adminAnnounceInput');if(!inp||!inp.value.trim())return toast('Skriv ett tillk\xe4nnagivande','error');var ann=JSON.parse(localStorage.getItem('admin_announcements')||'[]');ann.unshift(inp.value.trim());if(ann.length>10)ann.pop();localStorage.setItem('admin_announcements',JSON.stringify(ann));inp.value='';toast('Tillagt','ok');renderAdminPanel();}\nfunction removeAnnouncement(i){var ann=JSON.parse(localStorage.getItem('admin_announcements')||'[]');ann.splice(i,1);localStorage.setItem('admin_announcements',JSON.stringify(ann));toast('Borttaget','ok');renderAdminPanel();}"

if OLD_ANN_FUNCS not in html:
    # Try to find it
    idx = html.find('function addAnnouncement()')
    if idx >= 0:
        print(f'Found addAnnouncement at {idx}: {repr(html[idx:idx+300])}')
    else:
        print('ERROR: addAnnouncement not found by expected text')

NEW_ANN_FUNCS = '''function showSiteAnnouncements(){
  var ann=JSON.parse(localStorage.getItem('admin_announcements')||'[]');
  var dismissed=JSON.parse(localStorage.getItem('dismissed_announcements')||'[]');
  var active=ann.filter(function(a){return dismissed.indexOf(a)<0;});
  var banner=document.getElementById('siteAnnouncementBanner');
  var textEl=document.getElementById('siteAnnouncementText');
  if(active.length&&banner&&textEl){
    textEl.textContent='\U0001F4E3 '+active[0];
    banner.style.display='block';
    var main=document.querySelector('.main');
    if(main)main.style.paddingTop='44px';
  }else if(banner){
    banner.style.display='none';
    var main=document.querySelector('.main');
    if(main)main.style.paddingTop='';
  }
}
function dismissSiteAnnouncement(){
  var textEl=document.getElementById('siteAnnouncementText');
  if(textEl){
    var text=textEl.textContent.replace('\U0001F4E3 ','');
    var dismissed=JSON.parse(localStorage.getItem('dismissed_announcements')||'[]');
    dismissed.push(text);
    localStorage.setItem('dismissed_announcements',JSON.stringify(dismissed));
  }
  var banner=document.getElementById('siteAnnouncementBanner');
  if(banner)banner.style.display='none';
  var main=document.querySelector('.main');
  if(main)main.style.paddingTop='';
}
function addAnnouncement(){var inp=document.getElementById('adminAnnounceInput');if(!inp||!inp.value.trim())return toast('Skriv ett tillk\xe4nnagivande','error');var ann=JSON.parse(localStorage.getItem('admin_announcements')||'[]');ann.unshift(inp.value.trim());if(ann.length>10)ann.pop();localStorage.setItem('admin_announcements',JSON.stringify(ann));inp.value='';localStorage.removeItem('dismissed_announcements');showSiteAnnouncements();toast('Tillk\xe4nnagivande publicerat! \U0001F4E3','ok');renderAdminPanel();}
function removeAnnouncement(i){var ann=JSON.parse(localStorage.getItem('admin_announcements')||'[]');ann.splice(i,1);localStorage.setItem('admin_announcements',JSON.stringify(ann));toast('Borttaget','ok');showSiteAnnouncements();renderAdminPanel();}'''

html = do_replace('Add announcement JS functions', OLD_ANN_FUNCS, NEW_ANN_FUNCS, html)

# ============================================================
# FEATURE 7: Daily Login Streak JS
# ============================================================

OLD_FINISH_LOGIN = 'function finishLogin(){'

DAILY_STREAK_AND_FINISH = '''function checkDailyStreak(){
  if(!state.user)return;
  var today=new Date().toDateString();
  var key='daily_streak_'+state.user;
  var data=JSON.parse(localStorage.getItem(key)||'{"streak":0,"last":""}');
  var yesterday=new Date(Date.now()-86400000).toDateString();
  if(data.last===today)return;
  if(data.last===yesterday){
    data.streak=(data.streak||0)+1;
  }else{
    data.streak=1;
  }
  data.last=today;
  localStorage.setItem(key,JSON.stringify(data));
  var bonus=Math.min(data.streak*5,50);
  addCoins(bonus,'Daglig inloggning dag '+data.streak);
  setTimeout(function(){
    toast('\U0001F525 Dag '+data.streak+' streak! +'+bonus+' mynt','ok');
  },1500);
  updateHUD();
}
function finishLogin(){'''

html = do_replace('Add checkDailyStreak before finishLogin', OLD_FINISH_LOGIN, DAILY_STREAK_AND_FINISH, html)

# ============================================================
# FEATURE 8: Leaderboard render function (add near switchSideTab area)
# ============================================================

OLD_SWITCH_SIDE = 'function switchSideTab(tab){'

LEADERBOARD_AND_SWITCH = '''function renderLeaderboardPanel(){
  var el=document.getElementById('panel_leaderboard');if(!el)return;
  var users=getAllUsers();
  var ranked=users.map(function(u){
    var d=JSON.parse(localStorage.getItem('jspel_'+u)||'{}');
    return {user:u,coins:d.coins||0,xp:d.xp||0,level:d.level||1};
  }).sort(function(a,b){return b.xp-a.xp;});
  var html='<div class="sideSection"><h4>\U0001F3C6 Topp spelare (XP)</h4>';
  ranked.slice(0,15).forEach(function(r,i){
    var medals=['\U0001F947','\U0001F948','\U0001F949'];
    var medal=medals[i]||'#'+(i+1);
    var isMe=r.user===state.user;
    html+='<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:10px;background:'+(isMe?'rgba(123,44,255,.2)':'rgba(255,255,255,.03)')+';border:1px solid '+(isMe?'var(--p0)':'var(--line)')+';margin-bottom:4px">';
    html+='<span style="font-size:16px;width:24px;text-align:center">'+medal+'</span>';
    html+='<div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:700;color:var(--w);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+r.user+'</div>';
    html+='<div style="font-size:10px;color:var(--d)">Niv\xe5 '+r.level+' \xb7 '+r.xp+' XP</div></div>';
    html+='<span style="font-size:11px;color:var(--p1);font-weight:700">'+r.coins+' \U0001FA99</span>';
    html+='</div>';
  });
  html+='</div>';
  el.innerHTML=html;
}
function switchSideTab(tab){'''

html = do_replace('Add renderLeaderboardPanel before switchSideTab', OLD_SWITCH_SIDE, LEADERBOARD_AND_SWITCH, html)

# ============================================================
# FEATURE 8: Update renders object to include leaderboard
# ============================================================

OLD_RENDERS = "var renders={favoriter:renderFavsPanel,teman:renderThemePanel,quests:renderQuestsPanel,butik:renderShopPanel,instaellningar:renderSettingsPanel,profil:renderProfilePanel,admin:renderAdminPanel,updates:renderUpdatesPanel,inventory:renderInventoryPanel};"

NEW_RENDERS = "var renders={favoriter:renderFavsPanel,teman:renderThemePanel,quests:renderQuestsPanel,butik:renderShopPanel,instaellningar:renderSettingsPanel,profil:renderProfilePanel,admin:renderAdminPanel,updates:renderUpdatesPanel,inventory:renderInventoryPanel,leaderboard:renderLeaderboardPanel,achievements:function(){renderAchievementsPanel(document.getElementById('panel_achievements'));}};"

html = do_replace('Update renders object', OLD_RENDERS, NEW_RENDERS, html)

# ============================================================
# FEATURE 9: Game rating JS functions (add before openGame)
# ============================================================

OLD_OPEN_GAME = 'function openGame(i){'

RATING_AND_OPEN_GAME = '''function rateGame(idx,stars){
  if(!state.user)return toast('Logga in f\xf6r att betygs\xe4tta','error');
  var key='rating_'+idx+'_'+state.user;
  localStorage.setItem(key,stars);
  var allKey='ratings_'+idx;
  var all=JSON.parse(localStorage.getItem(allKey)||'{}');
  all[state.user]=stars;
  localStorage.setItem(allKey,JSON.stringify(all));
  updateGameRatingDisplay(idx);
  toast('Betyg sparat: '+'\u2605'.repeat(stars),'ok');
}
function getGameRating(idx){
  var all=JSON.parse(localStorage.getItem('ratings_'+idx)||'{}');
  var vals=Object.values(all).map(Number);
  if(!vals.length)return{avg:0,count:0,myRating:0};
  var avg=vals.reduce(function(a,b){return a+b;},0)/vals.length;
  return{avg:Math.round(avg*10)/10,count:vals.length,myRating:parseInt(localStorage.getItem('rating_'+idx+'_'+(state.user||''))||'0')};
}
function updateGameRatingDisplay(idx){
  var info=getGameRating(idx);
  var el=document.getElementById('igpRatingStars');
  if(!el)return;
  var html='';
  for(var s=1;s<=5;s++){
    var filled=s<=(info.myRating||Math.round(info.avg));
    html+='<span onclick="rateGame('+idx+','+s+')" style="cursor:pointer;font-size:20px;color:'+(filled?'#ffd700':'rgba(255,255,255,.3)')+'">&#9733;</span>';
  }
  if(info.count)html+='<span style="font-size:11px;color:var(--d);margin-left:6px">'+info.avg+' ('+info.count+')</span>';
  el.innerHTML=html;
}
function openGame(i){'''

html = do_replace('Add rating JS + openGame start', OLD_OPEN_GAME, RATING_AND_OPEN_GAME, html)

# ============================================================
# FEATURE 9: Call updateGameRatingDisplay in openGame after setTimeout
# ============================================================

OLD_OPEN_GAME_END = 'updateQuests();saveState();setTimeout(updateGameQuestWidget,200);}'

NEW_OPEN_GAME_END = 'updateQuests();saveState();setTimeout(updateGameQuestWidget,200);setTimeout(function(){updateGameRatingDisplay(i);},100);checkAchievements();}'

html = do_replace('Add rating display + achievement check in openGame', OLD_OPEN_GAME_END, NEW_OPEN_GAME_END, html)

# ============================================================
# FEATURE 10: Achievements system JS
# ============================================================

OLD_ADD_COINS = 'function addCoins(n,reason){'

ACHIEVEMENTS_AND_ADD_COINS = '''var ACHIEVEMENTS=[
  {id:'first_game',name:'F\xf6rsta spelet',desc:'Spela ditt f\xf6rsta spel',icon:'\U0001F3AE',check:function(){return(state.gamesPlayed||0)>=1;}},
  {id:'games_10',name:'10 spel',desc:'Spela 10 spel',icon:'\U0001F579\uFE0F',check:function(){return(state.gamesPlayed||0)>=10;}},
  {id:'games_100',name:'Spelentusiast',desc:'Spela 100 spel',icon:'\U0001F3C5',check:function(){return(state.gamesPlayed||0)>=100;}},
  {id:'coins_100',name:'Rik',desc:'Samla 100 mynt',icon:'\U0001F4B0',check:function(){return state.coins>=100;}},
  {id:'coins_1000',name:'Rikaste',desc:'Samla 1000 mynt',icon:'\U0001F911',check:function(){return state.coins>=1000;}},
  {id:'favs_5',name:'Samlare',desc:'Ha 5 favoriter',icon:'\u2b50',check:function(){return state.favorites.length>=5;}},
  {id:'level_5',name:'Niv\xe5 5',desc:'N\xe5 niv\xe5 5',icon:'\U0001F31F',check:function(){return state.level>=5;}},
  {id:'level_10',name:'Veteran',desc:'N\xe5 niv\xe5 10',icon:'\U0001F48E',check:function(){return state.level>=10;}},
  {id:'streak_7',name:'En vecka',desc:'7 dagars inloggningsstreak',icon:'\U0001F525',check:function(){var d=JSON.parse(localStorage.getItem('daily_streak_'+(state.user||''))||'{"streak":0}');return(d.streak||0)>=7;}},
];
function checkAchievements(){
  if(!state.user)return;
  var earned=JSON.parse(localStorage.getItem('achievements_'+state.user)||'[]');
  var newOnes=[];
  ACHIEVEMENTS.forEach(function(a){
    if(earned.indexOf(a.id)<0&&a.check()){
      earned.push(a.id);newOnes.push(a);
    }
  });
  if(newOnes.length){
    localStorage.setItem('achievements_'+state.user,JSON.stringify(earned));
    newOnes.forEach(function(a,i){
      setTimeout(function(){toast(a.icon+' Achievement unlocked: '+a.name,'ok');},i*1200);
    });
  }
}
function renderAchievementsPanel(el){
  if(!el)return;
  var earned=JSON.parse(localStorage.getItem('achievements_'+(state.user||'')||'[]'));
  var html='<div class="sideSection"><h4>\U0001F3C5 Achievements ('+earned.length+'/'+ACHIEVEMENTS.length+')</h4>';
  ACHIEVEMENTS.forEach(function(a){
    var done=earned.indexOf(a.id)>=0;
    html+='<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:10px;background:rgba(255,255,255,.03);border:1px solid var(--line);margin-bottom:5px;opacity:'+(done?'1':'.45')+'">';
    html+='<span style="font-size:22px">'+a.icon+'</span>';
    html+='<div><div style="font-size:13px;font-weight:700;color:var(--w)">'+a.name+'</div><div style="font-size:11px;color:var(--d)">'+a.desc+'</div></div>';
    if(done)html+='<span style="margin-left:auto;color:#3ba55c;font-size:16px">\u2713</span>';
    html+='</div>';
  });
  html+='</div>';
  el.innerHTML=html;
}
function addCoins(n,reason){'''

html = do_replace('Add Achievements JS + addCoins start', OLD_ADD_COINS, ACHIEVEMENTS_AND_ADD_COINS, html)

# ============================================================
# FEATURE 10: Call checkAchievements in addCoins
# ============================================================

OLD_ADD_COINS_BODY = '  state.coins+=n;state.xp+=Math.floor(n/2);\n  saveState();updateHUD();\n  toast("+"+n+" mynt \u2014 "+reason);\n}'

NEW_ADD_COINS_BODY = '  state.coins+=n;state.xp+=Math.floor(n/2);\n  saveState();updateHUD();\n  toast("+"+n+" mynt \u2014 "+reason);\n  checkAchievements();\n}'

html = do_replace('Call checkAchievements in addCoins', OLD_ADD_COINS_BODY, NEW_ADD_COINS_BODY, html)

# ============================================================
# FEATURE 7+10+6: Call init functions in finishLogin
# ============================================================

OLD_FINISH_LOGIN_END = '  var broadcast=JSON.parse(localStorage.getItem("broadcast")||"null");\n  if(broadcast&&broadcast.msg){setTimeout(function(){toast("\U0001F4E2 "+broadcast.msg,5000);},500);}\n}'

NEW_FINISH_LOGIN_END = '  var broadcast=JSON.parse(localStorage.getItem("broadcast")||"null");\n  if(broadcast&&broadcast.msg){setTimeout(function(){toast("\U0001F4E2 "+broadcast.msg,5000);},500);}\n  ensureJoinDate();\n  checkDailyStreak();\n  showSiteAnnouncements();\n}'

html = do_replace('Add ensureJoinDate+checkDailyStreak+showSiteAnnouncements in finishLogin', OLD_FINISH_LOGIN_END, NEW_FINISH_LOGIN_END, html)

# ============================================================
# FEATURE 5+4: makeDraggable calls for chat and soundboard windows
# ============================================================

OLD_DRAGGABLE = '  var pCard=document.getElementById(\'profileCard\');\n  if(pCard)makeDraggable(pCard,pCard);'

NEW_DRAGGABLE = '''  var pCard=document.getElementById('profileCard');
  if(pCard)makeDraggable(pCard,pCard);
  var chatWin=document.getElementById('chatWin');
  var chatBar=document.getElementById('chatWinBar');
  if(chatWin&&chatBar)makeDraggable(chatWin,chatBar);
  var sbWin=document.getElementById('soundboardWin');
  var sbBar=document.getElementById('soundboardWinBar');
  if(sbWin&&sbBar)makeDraggable(sbWin,sbBar);'''

html = do_replace('Add makeDraggable for chat+soundboard', OLD_DRAGGABLE, NEW_DRAGGABLE, html)

# ============================================================
# FEATURE 6: Call showSiteAnnouncements in init (after renderGames at startup)
# ============================================================

OLD_INIT_ELSE = '  }else{\n    renderGames();\n    switchSideTab("favoriter");\n  }'

NEW_INIT_ELSE = '  }else{\n    renderGames();\n    switchSideTab("favoriter");\n    showSiteAnnouncements();\n  }'

html = do_replace('Call showSiteAnnouncements in init else branch', OLD_INIT_ELSE, NEW_INIT_ELSE, html)

# ============================================================
# Write the file
# ============================================================

print(f'\nNew file size: {len(html)} chars (was {original_len})')
print(f'Errors: {len(errors)}')
for e in errors:
    print(f'  - {e}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done writing index.html')
