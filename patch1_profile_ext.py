# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# FEATURE 1A: Add profile extension functions BEFORE _renderProfileCard
# ============================================================

OLD_RENDER_START = 'function _renderProfileCard(card,username){\n  var isSelf=(username===state.user);\n  /* Try to get data from localStorage (works for local profiles) */'

NEW_PROFILE_EXT_FUNCS = '''function getProfileExt(username){
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
    toast('Banner uppdaterad! \uD83D\uDDBC\uFE0F','ok');
  };
  reader.readAsDataURL(file);
}
function pinCurrentGame(){
  if(_currentGameIdx<0)return toast('\xD6ppna ett spel f\xF6rst','error');
  var g=GAMES[_currentGameIdx];if(!g)return;
  var ext=getProfileExt(state.user);
  var pins=ext.pinnedGames||[];
  if(pins.find(function(p){return p.f===g.f;}))return toast('Redan pinnead','error');
  pins.unshift({name:g.name,f:g.f,cat:g.cat||''});
  if(pins.length>3)pins.pop();
  setProfileExt({pinnedGames:pins});
  toast('Spel pinneat p\xE5 profilen! \uD83D\uDCCC','ok');
}
function unpinGame(f){
  var ext=getProfileExt(state.user);
  var pins=(ext.pinnedGames||[]).filter(function(p){return p.f!==f;});
  setProfileExt({pinnedGames:pins});
  if(document.getElementById('viewProfileOverlay').classList.contains('open'))viewProfile(state.user);
}
function _renderProfileCard(card,username){
  var isSelf=(username===state.user);
  /* Try to get data from localStorage (works for local profiles) */'''

if OLD_RENDER_START in html:
    html = html.replace(OLD_RENDER_START, NEW_PROFILE_EXT_FUNCS, 1)
    print('SUCCESS: Added profile extension functions before _renderProfileCard')
else:
    print('ERROR: Could not find _renderProfileCard start anchor')
    # Show context
    idx = html.find('function _renderProfileCard')
    if idx >= 0:
        print('Found _renderProfileCard at char', idx)
        print(repr(html[idx:idx+200]))

# ============================================================
# FEATURE 1B: Replace the full _renderProfileCard body
# ============================================================

OLD_RENDER_BODY = '''function _renderProfileCard(card,username){
  var isSelf=(username===state.user);
  /* Try to get data from localStorage (works for local profiles) */
  var uData=JSON.parse(localStorage.getItem("jspel_"+username)||"{}");
  var eq=(uData.settings&&uData.settings.equipped)||{};
  var av=localStorage.getItem("avatar_"+username)||"";
  var level=uData.level||1;
  var coins=isSelf?state.coins:(uData.coins||0);
  var favs=isSelf?state.favorites.length:(uData.favorites||[]).length;
  var friends=JSON.parse(localStorage.getItem("friends_"+username)||"[]");
  var myFriends=state.user?JSON.parse(localStorage.getItem("friends_"+state.user)||"[]"):[];
  var isFriend=myFriends.indexOf(username)>=0;

  /* Banner */
  var bannerStyle=getBannerStyle(eq.effect||null);
  /* Avatar */
  var frameClass=getFrameClass(eq.frame||null);
  var avatarHTML=av
    ?'<img src="'+av+'" class="pc-avatar '+frameClass+'" style="width:72px;height:72px">'
    :'<div class="pc-avatar '+frameClass+'" style="background:var(--p0);width:72px;height:72px">'+username.charAt(0).toUpperCase()+'</div>';
  /* Name effect */
  var nameClass=getNameClass(eq.nameeffect||null);
  /* Badges */
  var badgesHTML="";
  if(eq.badge)badgesHTML+=getBadgeHTML(eq.badge);
  /* Actions */
  var actionsHTML="";
  if(!isSelf&&state.user){
    if(isFriend){
      actionsHTML=\'<button onclick="removeFriend(\\\''+username+\'\\\');closeViewProfile();toast(\\\'V\xE4n borttagen\\\')" style="background:rgba(255,50,50,.2);color:#ff6b6b;border:1px solid rgba(255,50,50,.3);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">\u2715 Ta bort v\xE4n</button>\';
    }else{
      actionsHTML=\'<button onclick="addFriendDirect(\\\''+username+\'\\\');closeViewProfile();toast(\\\'+V\xE4n tillagd \u2728\\\',\\\'ok\\\')" style="background:var(--p0);color:#fff;flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer;border:none">+ L\xE4gg till v\xE4n</button>\';
    }
  }
  if(isSelf){
    actionsHTML=\'<button onclick="closeViewProfile();openProfileOverlay()" style="background:var(--glass);color:var(--w);border:1px solid var(--line);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">\uD83D\uDCDD Redigera profil</button>\';
  }
  actionsHTML+=\'<button onclick="closeViewProfile()" style="background:var(--glass);color:var(--d);border:1px solid var(--line);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">St\xE4ng</button>\';

  /* For own profile, wrap avatar in upload label */
  var avatarWrapHTML=isSelf
    ?\'<label for="pcFileInput" style="cursor:pointer;display:block;position:relative">\'+avatarHTML+\'<div style="position:absolute;bottom:2px;right:2px;width:22px;height:22px;border-radius:50%;background:var(--p0);display:flex;align-items:center;justify-content:center;font-size:10px;border:2px solid var(--bg1)">\uD83D\uDCF7</div></label>\'
    :avatarHTML;
  card.innerHTML=
    \'<div class="pc-banner pc-banner-default" style="\'+bannerStyle+\'">\\'
    +\'<div class="pc-avatar-wrap">\'+avatarWrapHTML+\'</div>\'
    +\'<button class="pc-close" onclick="closeViewProfile()">\u2715</button>\'
    +\'</div>\'
    +\'<div class="pc-body">\'
    +\'<div class="pc-name-row"><span class="pc-username \'+nameClass+\'">\'+username+\'</span></div>\'
    +(badgesHTML?\'<div class="pc-badges">\'+badgesHTML+\'</div>\':\'\')
    +\'<div class="pc-level">Niv\xE5 \'+level+(isSelf?\' \xB7 \uD83E\uDDE0 \'+state.xp+\' XP\':\'\')+''+\'</div>\'
    +\'<div class="pc-divider"></div>\'
    +\'<div class="pc-stats">\'
    +\'<div class="pc-stat"><span>\'+coins+\'</span><small>\uD83D\uDCB0 Mynt</small></div>\'
    +\'<div class="pc-stat"><span>\'+favs+\'</span><small>\u2B50 Favs</small></div>\'
    +\'<div class="pc-stat"><span>\'+friends.length+\'</span><small>\uD83D\uDC65 V\xE4nner</small></div>\'
    +\'</div>\'
    +\'<div class="pc-divider"></div>\'
    +\'<div class="pc-actions">\'+actionsHTML+\'</div>\'
    +(isSelf?\'<input type="file" id="pcFileInput" accept="image/*" style="display:none" onchange="handleAvatarUpload(this);closeViewProfile();">\':\'\')
    +\'</div>\';

  /* If Supabase available, try to enrich with server data */
  if(_sb&&!isSelf){
    _sb.from("accounts").select("username,is_admin").eq("username",username).single().then(function(res){
      if(res.data&&res.data.is_admin){
        var nr=card.querySelector(".pc-name-row");
        if(nr&&!nr.querySelector(".admin-badge")){
          var ab=document.createElement("span");ab.className="pc-badge admin-badge";
          ab.style.cssText="background:#ff6b0022;color:#ff6b00;border:1px solid #ff6b0055";
          ab.textContent="\uD83D\uDEE1\uFE0F Admin";
          nr.appendChild(ab);
        }
      }
    });
  }
}'''

NEW_RENDER_BODY = r'''function _renderProfileCard(card,username){
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
  var joinHTML=ext.joinDate?'<div style="font-size:10px;color:var(--d);margin-top:2px">\uD83D\uDCC5 Gick med '+ext.joinDate+'</div>':'';
  /* Showcase - equipped cosmetics */
  var showcaseItems=[];
  if(eq.frame)showcaseItems.push('<div class="pc-showcase-item" title="Ram">'+getFrameClass(eq.frame).replace('frame-','')+'<br><small>Ram</small></div>');
  if(eq.badge)showcaseItems.push('<div class="pc-showcase-item">'+getBadgeHTML(eq.badge)+'<br><small>Badge</small></div>');
  if(eq.nameeffect)showcaseItems.push('<div class="pc-showcase-item">\u2728<br><small>Namn-effekt</small></div>');
  if(eq.effect)showcaseItems.push('<div class="pc-showcase-item">\uD83C\uDFA8<br><small>Banner</small></div>');
  var showcaseHTML=showcaseItems.length?'<div class="pc-divider"></div><div class="pc-showcase-title">\uD83C\uDFC6 Showcase</div><div class="pc-showcase">'+showcaseItems.join('')+'</div>':'';
  /* Pinned games */
  var pins=ext.pinnedGames||[];
  var pinsHTML='';
  if(pins.length){
    pinsHTML='<div class="pc-divider"></div><div class="pc-showcase-title">\uD83D\uDCCC Pinnade spel</div><div class="pc-pins">';
    pins.forEach(function(p){
      pinsHTML+='<div class="pc-pin-item" onclick="closeViewProfile();openGameByFile(\''+p.f+'\')">&#127918; '+p.name+'</div>';
    });
    pinsHTML+='</div>';
  }
  /* Actions */
  var actionsHTML="";
  if(!isSelf&&state.user){
    if(isFriend){
      actionsHTML='<button onclick="removeFriend(\''+username+'\');closeViewProfile();toast(\'V\u00E4n borttagen\')" style="background:rgba(255,50,50,.2);color:#ff6b6b;border:1px solid rgba(255,50,50,.3);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">\u2715 Ta bort v\u00E4n</button>';
    }else{
      actionsHTML='<button onclick="addFriendDirect(\''+username+'\');closeViewProfile();toast(\'+V\u00E4n tillagd \u2728\',\'ok\')" style="background:var(--p0);color:#fff;flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer;border:none">+ L\u00E4gg till v\u00E4n</button>';
    }
  }
  if(isSelf){
    actionsHTML='<button onclick="openProfileEditModal()" style="background:var(--p0);color:#fff;border:none;flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">\u270F\uFE0F Redigera</button>';
    actionsHTML+='<label style="background:var(--glass);color:var(--w);border:1px solid var(--line);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer;text-align:center;display:flex;align-items:center;justify-content:center">\uD83D\uDDBC\uFE0F Banner<input type="file" accept="image/*" style="display:none" onchange="handleBannerUpload(this)"></label>';
  }
  actionsHTML+='<button onclick="closeViewProfile()" style="background:var(--glass);color:var(--d);border:1px solid var(--line);flex:1;padding:9px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer">St\u00E4ng</button>';
  var avatarWrapHTML=isSelf
    ?'<label for="pcFileInput" style="cursor:pointer;display:block;position:relative">'+avatarHTML+'<div style="position:absolute;bottom:2px;right:2px;width:22px;height:22px;border-radius:50%;background:var(--p0);display:flex;align-items:center;justify-content:center;font-size:10px;border:2px solid var(--bg1)">\uD83D\uDCF7</div></label>'
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
    +'<div class="pc-level">Niv\u00E5 '+level+(isSelf?' \u00B7 \uD83E\uDDE0 '+state.xp+' XP':'')+'</div>'
    +joinHTML
    +bioHTML
    +'<div class="pc-divider"></div>'
    +'<div class="pc-stats">'
    +'<div class="pc-stat"><span>'+coins+'</span><small>\uD83D\uDCB0 Mynt</small></div>'
    +'<div class="pc-stat"><span>'+favs+'</span><small>\u2B50 Favs</small></div>'
    +'<div class="pc-stat"><span>'+friends.length+'</span><small>\uD83D\uDC65 V\u00E4nner</small></div>'
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
          ab.textContent="\uD83D\uDEE1\uFE0F Admin";nr.appendChild(ab);
        }
      }
    });
  }
}
function openGameByFile(f){
  var idx=GAMES.findIndex(function(g){return g.f===f;});
  if(idx>=0)openGame(idx);
}'''

# Find the second occurrence of _renderProfileCard (the original one, after we inserted the new prefix functions)
# We need to find the existing body and replace it
# The OLD_RENDER_BODY uses escaped quotes. Let me instead find it by searching for key unique strings.

# Since we already replaced the start in step 1A (adding prefix), the current html has TWO calls to _renderProfileCard.
# The first is the wrapper from step 1A where we inserted the original start.
# Wait - we replaced the START of _renderProfileCard, not the body.
# Let's find the current state and replace the correct version.

# Actually in step 1A we kept the OLD start of _renderProfileCard intact (the new code was inserted BEFORE it).
# So now there are two "function _renderProfileCard" in html - that's wrong!
# Let me reconsider: in step 1A, I replaced OLD_RENDER_START with NEW_PROFILE_EXT_FUNCS which ENDS with the original OLD_RENDER_START text.
# So the result is: new functions + original _renderProfileCard start. That's correct - only one _renderProfileCard.

# Now replace the whole original _renderProfileCard with the new version.
# The original starts with: function _renderProfileCard(card,username){
# We need to find and replace the whole body.

import re

# Find the whole old function
pattern = r'function _renderProfileCard\(card,username\)\{[\s\S]*?^  if\(_sb&&!isSelf\)\{[\s\S]*?^\}\s*\n'
m = re.search(pattern, html, re.MULTILINE)
if m:
    html = html[:m.start()] + NEW_RENDER_BODY + '\n' + html[m.end():]
    print('SUCCESS: Replaced _renderProfileCard with enhanced version')
else:
    print('ERROR: Could not find _renderProfileCard body via regex')
    # Try simpler approach - find the start line and the openGameByFile that should come after
    idx = html.find('function _renderProfileCard(card,username){')
    if idx >= 0:
        print('Found at char', idx)
        # Find end by looking for the closing pattern
        end_marker = '\n}\nfunction openGame'
        end_idx = html.find(end_marker, idx)
        if end_idx >= 0:
            print('Found end at', end_idx)
            html = html[:idx] + NEW_RENDER_BODY + html[end_idx:]
            print('SUCCESS: Replaced via alternative method')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Patch 1 (Profile Extension functions + enhanced _renderProfileCard) written.')
