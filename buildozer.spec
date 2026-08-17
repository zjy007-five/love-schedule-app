[app]
title = 爱心课表
package.name = loveschedule
package.domain = com.zhangjianyi
version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,ttc,json
source.exclude_exts = spec,md,txt
source.exclude_dirs = tests,bin,.git,__pycache__
source.exclude_patterns = build/*,dist/*

requirements = hostpython3==3.10.12,python3==3.10.12,kivy==2.2.1

entrypoint = main.py

orientation = portrait
fullscreen = 0

android.permissions = POST_NOTIFICATIONS,VIBRATE,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.private_storage = True
android.allow_backup = True
android.wakelock = False
android.theme = @android:style/Theme.Material.Light.NoActionBar
android.no_compress = ttf,ttc,png,jpg
android.no-bytecompile = True

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.0
android.archs = arm64-v8a
android.accept_sdk_license = True
android.debug = True
android.release = False
android.apk_sign = True
