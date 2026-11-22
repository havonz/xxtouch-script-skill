# AI Completion Reference
Lua 5.3. Built-ins are globals; do not require app/sys/screen/touch/image/file/http/json/dialog/device/key/mouse/gamepad/pasteboard/thread/utils/webview.
XXT project: main=lua/scripts/main.lua; modules=lua/ or lua/scripts/; resources=res/ via XXT_RES_PATH.
coords: screen/touch follow screen.init(mode); ImageObject uses image-local pixels; no match usually returns -1,-1; wait with sys.msleep(ms).
logs: use nLog(a,b,...) instead of print.

env:
XXT_HOME_PATH,XXT_RES_PATH,XXT_SCRIPTS_PATH,XXT_LUA_PATH,XXT_LIB_PATH,XXT_LOG_PATH,XXT_BIN_PATH,XXT_TESSDATA_PATH,IS_TROLLSTORE_EDITION

global:
nLog(a,b,...)
t=get_elapsed_ms()
j=jbroot(path); path=rootfs(j)
register_atexit(name,fn)
ret,err=proc_dict_run(code)
v=proc_get(key); old=proc_put(key,v)
n=proc_queue_push(key,v); n=proc_queue_push_back(key,v); n=proc_queue_push_front(key,v)
v=proc_queue_pop(key); v=proc_queue_pop_front(key); v=proc_queue_pop_back(key)
n=proc_queue_pop_value(key,v); n=proc_queue_count_value(key,v); list=proc_queue_read(key); n=proc_queue_size(key)

app:
p=app.bundle_path(bid)
p=app.data_path(bid)
name=app.localized_name(bid)
bid=app.front_bid(); pid=app.front_pid(); pid=app.pid_for_bid(bid); ok=app.is_running(bid)
bids=app.bundles(); procs=app.all_procs()
code=app.run(bid); app.close(bid_or_pid); app.quit(bid_or_star)
ok=app.open_url(url)
ok=app.install(path[,force]); ok=app.uninstall(bid)
info=app.group_info(bid); info=app.plugin_info(bid); png=app.png_data_for_bid(bid)
files,err=app.lsof(bid_or_pid); mem=app.used_memory(bid_or_pid)
app.pop_banner(bid,title,body)
ok,old=app.set_tcc(bid,service,state)
info=app.notification_permissions(bid,op[,info]); info=app.local_network_permissions(bid,op[,info])

device:
pct=device.battery_level(); state=device.battery_state()
typ=device.type(); udid=device.udid(); sn=device.serial_number()
name=device.name(); device.set_name(name)
v=device.brightness(); device.set_brightness(v); device.set_volume(v)
device.vibrator(); device.play_sound(path)
device.flash_on(); device.flash_off()
orien=device.front_orien()
device.lock_orien(); device.unlock_orien(); ok=device.is_orien_locked()
device.lock_screen(); device.unlock_screen([pass]); ok=device.is_screen_locked()
device.reset_idle(); device.set_autolock_time(minutes)
device.turn_on_wifi(); device.turn_off_wifi(); device.turn_on_data(); device.turn_off_data()
device.turn_on_bluetooth(); device.turn_off_bluetooth(); device.turn_on_airplane(); device.turn_off_airplane()
ok,status=device.is_vpn_on(); device.turn_on_vpn(); device.turn_off_vpn()
ok,err=device.join_wifi(ssid,pwd[,ms]); ok=device.forget_wifi(ssid)
wifi=device.wifi_info(); mac=device.wifi_mac(); ifs=device.ifaddrs()
device.assistive_touch_on(); device.assistive_touch_off()
device.reduce_motion_on(); device.reduce_motion_off()

sys:
sys.msleep(ms)
sys.toast(txt[,rot])
choice=sys.alert(txt[,sec,title,b0,b1,b2])
txt=sys.input_box(desc); txt=sys.input_box(title,desc[,n])
txt,choice=sys.input_box(title,desc,prompt,default,b0,b1,b2[,n])
sys.input_text(txt[,ret])
sys.log(a,b,...)
free=sys.free_disk_space([mount]); mem=sys.available_memory(); info=sys.memory_info()
ver=sys.version(); ver=sys.xtversion(); ver=sys.cfversion()
ts=sys.mtime(); ts=sys.net_time([timeout]); n=sys.rnd()
sys.mkdir_p(dir)
task=sys.task(path[,args...])
task:launch(); task:wait_until_exit(); pid=task:pid(); running=task:is_running(); task:kill()
sys.kill(pid); sys.killall(name)
s=sys.ctlbyname(key); answer=sys.mgcopyanswer(q)
ok=sys.set_user_tracking(ok); ok=sys.user_tracking()

screen:
old=screen.init(mode)
w,h=screen.size(); scale=screen.scale_factor()
screen.keep(); screen.unkeep()
img=screen.image([l,t,r,b])
color=screen.get_color(x,y); r,g,b=screen.get_color_rgb(x,y)
ok=screen.is_colors(colors[,sim])
x,y=screen.find_color(colors[,sim,l,t,r,b])
x,y=screen.find_image(img_or_path[,conf,l,t,r,b]); results=screen.find_image(img,{find_all=true,confidence_threshold=conf},l,t,r,b)
txt,details=screen.ocr_text(l,t,r,b[,opts,bin_opts])
x,y=screen.rotate_xy(x,y,rot); x,y=screen.unrotate_xy(x,y,rot)

touch:
touch.tap(x,y[,delay,wait])
t=touch.on(x,y); t:move(x,y); t:msleep(ms); t:off()
touch.on(x,y):move(x2,y2):msleep(ms):off()
t:step_len(n); t:step_delay(ms); t:press(v)
touch.on(id,x,y); touch.move(id,x,y); touch.off(id,x,y)

image/ImageObject:
img=image.load_file(path); img=image.load_data(data); img=image.new(w,h); ok=image.is(v)
w,h=img:size(); img:destroy()
copy=img:copy(); crop=img:crop([l,t,r,b])
color,alpha=img:get_color(x,y); img=img:set_color(x,y,color)
img=img:binaryzation(colors); img=img:replace_color(from,to[,sim])
x,y=img:find_color(colors[,sim,l,t,r,b]); ok=img:is_colors(colors[,sim])
x,y=big:find_image(small[,conf,l,t,r,b]); results=big:find_image(small,{find_all=true,confidence_threshold=conf},l,t,r,b)
x,y,sim=big:cv_find_image(small); results,vis=img:cv_detect_templates(templates)
img=img:cv_resize(w,h); img=img:cv_binaryzation([threshold])
shapes,vis=img:cv_to_shapes([opts]); shape,vis=img:cv_find_shapes(shapes[,opts])
diff,vis=img:cv_compare_image(other[,opts])
big=big:draw_image(small[,opts])
png=img:png_data(); jpg=img:jpeg_data([quality])
ok=img:save_to_png_file(path); ok=img:save_to_jpeg_file(path[,quality]); ok=img:save_to_album()
txt,details=img:ocr_text([opts,bin_opts]); txt,details=img:apple_ocr([langs]); txt,details=img:paddle_ocr([opts])
txt=img:qr_decode()
img=img:turn_left(); img=img:turn_right()
img=image.new_text_image(txt[,opts])
langs=image.vision_supported_recognition_languages()

file:
ok=file.exists(path)
s,err=file.reads(path); ok,err=file.writes(path,s); ok,err=file.appends(path,s)
files,err=file.list(path[,deep]); files=file.find(pattern)
ok,err=file.copy(from,to[,mode]); ok,err=file.move(from,to[,mode]); ok,err=file.remove(path)
copy/move use the exact final destination, not a containing directory; /a/b/c -> /d/e/c, never just /d/e/. A trailing / does not append the source name.
mode (20250914+): omitted/"" fails if target exists; "overwrite"/"o" replaces the target itself; "merge"/"m" merges directories keeping existing files; "overwrite-merge"/"om"/"mo" merges and overwrites same-name files.
ok,err=file.mkdir_p(dir[,uid,gid,perm])
size,err=file.size(path); attrs,err=file.attrs(path[,field]); attrs,err=file.lattrs(path[,field])
md5,err=file.md5(path); sha1,err=file.sha1(path)
ok,err=file.touch(path[,atime,mtime]); dir,err=file.currentdir(); ok,err=file.chdir(dir)
line,err=file.get_line(path,n); lines,err=file.get_lines(path)
ok,err=file.set_line(path,n,s); ok,err=file.set_lines(path,lines)
ok,err=file.insert_line(path,n,s); ok,err=file.insert_lines(path,n,lines)
ok,err=file.remove_line(path,n); ok,err=file.remove_lines(path,n,count); n,err=file.line_count(path)
ok,err=file.zip(zipPath,files[,pwd]); ok,err=file.unzip(zipPath,outDir[,pwd])

file.path (versions after 20250914):
parts,err=file.path.components(path)
name,err=file.path.last_component(path)
parent,err=file.path.remove_last_component(path)
full,err=file.path.add_component(path,component)
ext,err=file.path.extension(path)
base,err=file.path.remove_extension(path)
full,err=file.path.add_extension(path,extension)
normalized,err=file.path.normalize(path)
resolved,err=file.path.resolve_symlinks(path)
components returns a string array; other results are strings. Invalid path strings return nil,"Invalid path"; add_component also uses this error for an invalid component.
last_component("/")=="/"; remove_last_component("/usr")=="/"; remove_last_component("/")=="/". add_component handles the joining /.
extension returns the final extension without a dot, or "" if absent. remove_extension removes only the last extension and keeps paths without one unchanged.
add_extension appends instead of replacing: file.txt + bak -> file.txt.bak; .txt adds ..txt. Invalid extension strings return nil,"Invalid extension"; an extension containing / may return only nil without an error.
normalize processes . and .. and redundant slashes. resolve_symlinks depends on actual device links; a returned path does not prove existence, and missing/unresolved paths do not necessarily return nil or an error; use file.exists to check.
Path string operations do not create, delete, move, or rename actual files/directories.

http:
code,headers,body=http.get(url[,sec,headers,raw])
code,headers,body=http.post(url[,sec,headers,body,raw])
code,headers,body=http.put(url[,sec,headers,body,raw])
code,headers,body=http.delete(url[,sec,headers,body,raw])
code,headers=http.head(url[,sec,headers,raw])
code,headers,body=http.get{url=url,timeout=sec,headers=headers,params=params,download_file=path,progress=fn}
code,headers,body=http.post{url=url,timeout=sec,headers=headers,params=params,data=data,json=tab,multipart=form,upload_file=path,download_file=save}
code,headers,body=http.put{url=url,headers=headers,params=params,data=data,json=tab,multipart=form,upload_file=path}
code,headers,body=http.delete{url=url,headers=headers,params=params,data=data,json=tab,multipart=form,upload_file=path}
s=http.table_to_form_urlencoded(tab)

json/string/table:
tab=json.decode(s); s=json.encode(tab); json.null
s=string.trim(s); s=string.ltrim(s); s=string.rtrim(s); s=string.atrim(s)
parts=string.split(s,sep); ok=string.starts_with(s,prefix[,pos]); ok=string.ends_with(s,suffix[,len])
s=string.base64_encode(s); s=string.base64_decode(s)
hash=string.md5(s); hash=string.sha1(s); hash=string.hmac_sha1(s,key); hash=string.hmac_sha256(s,key)
s=string.to_hex(s); s=string.from_hex(hex); s=string.random(chars[,n,bytes])
s=string.encode_uri(s); s=string.decode_uri(s); s=string.encode_uri_component(s); s=string.decode_uri_component(s)
cmp=string.compare_version(a,b); s=string.from_gbk(gbk); s=string.strip_utf8_bom(s)
copy=table.deep_copy(tab); s=table.deep_dump(tab); tab=table.load_string(s)

dialog:
dlg=dialog(); dlg=dialog(title[,sec])
dlg:add_label(label); dlg:add_input(label[,default]); dlg:add_switch(label[,default])
dlg:add_range(label,range[,default]); dlg:add_picker(label,options[,default])
dlg:add_radio(label,options[,default]); dlg:add_checkbox(label,options[,defaults])
dlg:add_image(img_or_path); dlg:add_button(title,fn); dlg:add_group(title)
dlg:set_title(title); dlg:set_size(w,h); dlg:set_frame(x,y,w,h); dlg:set_corner_radius(r)
dlg:set_timeout(sec[,submit]); dlg:set_config(name); opts=dlg:load()
ok,opts=dlg:show()

key:
key.down(code); key.up(code); key.press(code); key.send_text(txt[,delay,shift_delay])
ok,err=key.input_text(txt[,need_enter]) -- 20260816+

hardware keyboard (20260805+):
kbd,err=key.connect_keyboard([props]); kbd,err=key.connect_global_keyboard([props]); kbd=key.get_global_keyboard(); ok,err=key.disconnect_global_keyboard()
ok,err=kbd:down(code); ok,err=kbd:down(usagePage,usageID); ok,err=kbd:up(code); ok,err=kbd:up(usagePage,usageID)
ok,err=kbd:press(code[,ms]); ok,err=kbd:press(usagePage,usageID[,ms]); ok,err=kbd:send_text(txt[,delay,shiftDelay])
connected=kbd:is_connected(); props=kbd:get_properties(); ok,err=kbd:disconnect()

hardware mouse (20260805+):
m,err=mouse.connect([props]); ok,err=m:move(dx,dy); ok,err=m:down(button); ok,err=m:up(button); ok,err=m:click(button[,ms]); ok,err=m:scroll(dx,dy)
connected=m:is_connected(); props=m:get_properties(); ok,err=m:disconnect()
move dx,dy=-2047..2047; scroll dx,dy=-127..127; button=1..32 or left/right/middle/back/forward

hardware gamepad (20260805+):
pad,err=gamepad.connect([props]); ok,err=pad:down(button); ok,err=pad:up(button); ok,err=pad:press(button[,ms]); ok,err=pad:set_stick(stick,x,y); ok,err=pad:set_dpad(x,y); ok,err=pad:reset()
connected=pad:is_connected(); props=pad:get_properties(); ok,err=pad:disconnect()
button=1..32 or name; stick=left/right with x,y=-1..1; dpad x,y=-1/0/1

hardware props: VendorID,ProductID,VersionNumber,Product,Manufacturer,Transport,SerialNumber,LocationID

pasteboard/plist/thread:
s=pasteboard.read([uti]); ok=pasteboard.write(s[,uti]); ok=pasteboard.write_items(items[,opts]); pasteboard.clear()
tab=plist.read(path); ok=plist.write(path,tab); tab=plist.load(data); data=plist.dump(tab); data=plist.data_convert(data,fmt)
id=thread.current_id(); id=thread.dispatch(fn[,err_fn]); thread.wait(id[,sec]); thread.kill(id)
thread.register_event(name,fn); thread.unregister_event(name)

utils/webview/xui/xpp/dm/alert:
uuid=utils.gen_uuid(); args=utils.launch_args(); ok=utils.is_launch_via_app()
ts=utils.date_from_format(fmt,s[,opts]); s=utils.date_to_format(fmt,ts[,opts])
img=utils.qr_encode(txt[,opts]); utils.video_to_album(path); utils.add_contacts(list); utils.remove_all_contacts()
webview.show(html_or_url[,opts]); webview.eval(js); webview.frame(x,y,w,h); webview.hide(); webview.destroy()
xui.show(file); xui.setup(file); xui.reload(); xui.dismiss(); v=xui.get(key); xui.set(key,v); tab=xui.read(); xui.write(tab); xui.clear()
info=xpp.info(); p=xpp.bundle_path(); p=xpp.resource_path(rel)
dm=require("dm"); dm.SetPath(dir); dm.SetDict(i,file); dm.LoadDict(i,file); dm.UseDict(i)
txt=dm.Ocr(l,t,r,b,color_format,sim); x,y=dm.FindStr(l,t,r,b,str,color_format,sim); x,y=dm.FindMatrix(l,t,r,b,hex,w,h,sim)
alerthelper.setRules(rules); alerthelper.clearRules()
xxtouch events: thread.register_event("xxtouch.call_callback",fn); thread.register_event("xxtouch.activator_callback",fn); thread.register_event("xxtouch.hid_event",fn)
