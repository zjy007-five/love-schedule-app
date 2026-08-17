# -*- coding: utf-8 -*-
# 爱心课表APP - 张简逸 ❤️ 余娜

import os, json, random, datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Triangle
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase

Window.size = (400, 720)

# ============ 字体（全局统一） ============
CN_FONT = None
for p in ["msyh.ttc", "C:/Windows/Fonts/msyh.ttc",
          "C:/Windows/Fonts/msyh.ttf", "C:/Windows/Fonts/simhei.ttf"]:
    if os.path.exists(p):
        CN_FONT = p
        break

EMOJI_FONT = None
for p in ["C:/Windows/Fonts/seguiemj.ttf", "C:/Windows/Fonts/seguiemj.ttc"]:
    if os.path.exists(p):
        EMOJI_FONT = p
        break

EMOJI_NAME = None
if EMOJI_FONT:
    try:
        LabelBase.register(name="EmojiFont", fn_regular=EMOJI_FONT)
        EMOJI_NAME = "EmojiFont"
    except Exception:
        EMOJI_NAME = None

if CN_FONT:
    LabelBase.register(name="DefaultFont", fn_regular=CN_FONT)
    DEFAULT_FONT = "DefaultFont"
else:
    DEFAULT_FONT = None

# ============ 配置区（你改这里） ============
GF_NAME = "余娜"
BF_NAME = "张简逸"
SCHOOL = "昌吉学院新城校区"
SEMESTER = "2025-2026学年 第二学期"

# 节次时间
PERIODS = [
    ("第1节", "08:00-08:45"),
    ("第2节", "08:55-09:40"),
    ("第3节", "10:05-10:50"),
    ("第4节", "11:00-11:45"),
    ("午休",  "12:45-14:00"),
    ("第5节", "14:00-14:45"),
    ("第6节", "14:55-15:40"),
    ("第7节", "15:55-16:40"),
    ("第8节", "16:50-17:35"),
    ("第9节", "18:30-19:15"),
]

# 午休配置
LUNCH_BREAK = {
    "start": "12:45",
    "end":   "14:00",
    "notify_start": True,
    "notify_end_before": 5,
}

# 上课提醒
REMINDER = {
    "enabled": True,
    "before_minutes": 10,
    "weekdays_only": True,
}

# 欢迎页停留秒数
WELCOME_AUTO_GO = 3

# 情话池
LOVE_QUOTES = [
    "做这个课表的时候，每一行代码都写满了想你",
    "娜娜宝贝，按时上课，按时想我",
    "希望每次打开课表，都能让你想到我",
    "你的每一节课，都有我在心里陪着你",
    "张简逸在昌吉学院的每一公里外，都在想你",
    "今天也要开开心心上课，平平安安下课",
]

# 课表数据（day: 1=周一~6=周六, row: 0=第1节~9=第9节）
DEFAULT_COURSES = [
    {"day": 1, "row": 0, "name": "商务英语阅读", "room": "南语音室1512", "teacher": "刘老师"},
    {"day": 1, "row": 1, "name": "基础英语", "room": "南1223", "teacher": "陈老师"},
    {"day": 1, "row": 2, "name": "英语语法", "room": "南1215", "teacher": "王老师"},
    {"day": 1, "row": 5, "name": "商务英语视听说", "room": "南语音室1508", "teacher": "赵老师"},
    {"day": 1, "row": 6, "name": "大学体育", "room": "体育场", "teacher": "李老师"},
    {"day": 2, "row": 0, "name": "基础英语", "room": "南1223", "teacher": "陈老师"},
    {"day": 2, "row": 2, "name": "商务英语阅读", "room": "南语音室1512", "teacher": "刘老师"},
    {"day": 2, "row": 3, "name": "英语语法", "room": "南1215", "teacher": "王老师"},
    {"day": 2, "row": 5, "name": "中华民族共同体概论", "room": "南1301", "teacher": "张老师"},
    {"day": 2, "row": 7, "name": "商务英语视听说", "room": "南语音室1508", "teacher": "赵老师"},
    {"day": 3, "row": 0, "name": "商务英语阅读", "room": "南语音室1512", "teacher": "刘老师"},
    {"day": 3, "row": 1, "name": "基础英语", "room": "南1223", "teacher": "陈老师"},
    {"day": 3, "row": 5, "name": "大学体育", "room": "体育场", "teacher": "李老师"},
    {"day": 3, "row": 6, "name": "英语语法", "room": "南1215", "teacher": "王老师"},
    {"day": 4, "row": 0, "name": "中华民族共同体概论", "room": "南1301", "teacher": "张老师"},
    {"day": 4, "row": 2, "name": "基础英语", "room": "南1223", "teacher": "陈老师"},
    {"day": 4, "row": 3, "name": "商务英语视听说", "room": "南语音室1508", "teacher": "赵老师"},
    {"day": 4, "row": 5, "name": "商务英语阅读", "room": "南语音室1512", "teacher": "刘老师"},
    {"day": 5, "row": 1, "name": "英语语法", "room": "南1215", "teacher": "王老师"},
    {"day": 5, "row": 2, "name": "中华民族共同体概论", "room": "南1301", "teacher": "张老师"},
    {"day": 5, "row": 5, "name": "大学体育", "room": "体育场", "teacher": "李老师"},
    {"day": 5, "row": 6, "name": "商务英语视听说", "room": "南语音室1508", "teacher": "赵老师"},
]

COLORS = ["#FFB3BA","#FFDFBA","#FFFFBA","#BAFFC9","#BAE1FF",
          "#E0BBE4","#FEC8D8","#D4F0F0","#FFD3B6","#C9F5D3",
          "#FFC4E1","#C8E6C9","#FFF9C4","#B3E5FC","#E1BEE7"]
HEART_COLORS = [(1,0.4,0.5,0.9),(1,0.6,0.7,0.85),(0.95,0.5,0.6,0.9),
                (1,0.75,0.8,0.85),(0.9,0.45,0.55,0.9),(1,0.65,0.75,0.8)]

# ============ 工具函数 ============
def load_courses():
    path = "course_data.json"
    if not os.path.exists(path):
        return list(DEFAULT_COURSES)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and data and isinstance(data[0], dict) and "name" in data[0]:
            return data
    except Exception:
        pass
    return list(DEFAULT_COURSES)

def hm_to_min(s):
    h, m = int(s.split(":")[0]), int(s.split(":")[1])
    return h * 60 + m

def now_min():
    n = datetime.datetime.now()
    return n.hour * 60 + n.minute

def now_weekday():
    return datetime.datetime.now().weekday() + 1

# ============ 画爱心 ============
def draw_heart(widget, x, y, size, color_rgba):
    s = size
    with widget.canvas:
        Color(*color_rgba)
        Ellipse(pos=(x - s*0.35, y), size=(s*0.6, s*0.6))
        Ellipse(pos=(x + s*0.05, y), size=(s*0.6, s*0.6))
        w = s * 0.7
        h = s * 0.7
        Triangle(points=[x - w/2, y + s*0.15, x + w/2, y + s*0.15, x, y - h*0.9])

class FallingHeart(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint = (None, None)
        self.size = (dp(28), dp(28))
        self.color = random.choice(HEART_COLORS)
        self.bind(pos=self._redraw)
        self._redraw()
    def _redraw(self, *a):
        self.canvas.clear()
        draw_heart(self, self.center_x, self.center_y, self.width*0.9, self.color)

def spawn_heart(root, wh):
    h = FallingHeart()
    h.x = random.randint(int(dp(10)), int(Window.width - dp(40)))
    h.y = wh + dp(20)
    root.add_widget(h)
    dur = random.uniform(5, 9)
    sway = random.uniform(-dp(30), dp(30))
    anim = Animation(x=h.x+sway, duration=dur/2) + Animation(x=h.x-sway, duration=dur/2)
    main = Animation(y=-dp(60), duration=dur) & anim
    main = main + Animation(opacity=0, duration=0.5)
    main.bind(on_complete=lambda *x: root.remove_widget(h))
    main.start(h)

# ============ 课程卡片 ============
class CourseCard(Button):
    def __init__(self, course, color, **kw):
        kw.setdefault("size_hint", (1, None))
        kw.setdefault("height", dp(58))
        kw.setdefault("background_color", (0,0,0,0))
        kw.setdefault("text", "")
        if DEFAULT_FONT:
            kw.setdefault("font_name", DEFAULT_FONT)
        super().__init__(**kw)
        self.course = course
        with self.canvas.before:
            Color(*self.hex2(color))
            self.rect = RoundedRectangle(radius=[dp(10)]*4)
        self.bind(size=self._upd, pos=self._upd)
        self.text = f"[b]{course['name']}[/b]\n{course['room']}  {course['teacher']}"
        self.markup = True
        self.font_size = sp(11)
        self.color = (0.3, 0.1, 0.2, 1)
    def _upd(self, *a):
        self.rect.pos = self.pos
        self.rect.size = self.size
    def hex2(self, h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16)/255 for i in (0,2,4)) + (1,)

# ============ Emoji标签 ============
class EmojiLabel(Label):
    def __init__(self, text_cn="", text_emoji="", **kw):
        kw.setdefault("markup", True)
        if EMOJI_NAME and text_emoji:
            txt = f"[font={EMOJI_NAME}]{text_emoji}[/font]{text_cn}"
        else:
            txt = text_emoji + text_cn
        kw["text"] = txt
        if DEFAULT_FONT:
            kw.setdefault("font_name", DEFAULT_FONT)
        super().__init__(**kw)

# ============ 提醒引擎 ============
class ReminderEngine:
    def __init__(self, courses, popup_fn):
        self.courses = courses
        self.popup_fn = popup_fn
        self.done_today = set()
        self.last_date = datetime.date.today()
    def check(self):
        today = datetime.date.today()
        if today != self.last_date:
            self.done_today.clear()
            self.last_date = today
        if REMINDER["weekdays_only"] and now_weekday() > 5:
            return
        current = now_min()
        lunch_start = hm_to_min(LUNCH_BREAK["start"])
        lunch_end = hm_to_min(LUNCH_BREAK["end"])
        if LUNCH_BREAK["notify_start"] and current == lunch_start and "lunch_start" not in self.done_today:
            self.done_today.add("lunch_start")
            self.popup_fn("午休时间到", f"去吃饭休息吧~\n{LUNCH_BREAK['start']}~{LUNCH_BREAK['end']}\n张简逸提醒你:按时吃饭")
        end_before = LUNCH_BREAK.get("notify_end_before", 0)
        if end_before > 0:
            warn_t = lunch_end - end_before
            if current == warn_t and "lunch_end_warn" not in self.done_today:
                self.done_today.add("lunch_end_warn")
                self.popup_fn("午休快结束啦", "该准备去上下午的课了哦~ 张简逸在等你下课")
        if not REMINDER["enabled"]:
            return
        wd = now_weekday()
        if wd > 6:
            return
        for r, (label, time_str) in enumerate(PERIODS):
            if "午休" in label:
                continue
            start_str = time_str.split("-")[0]
            notify_t = hm_to_min(start_str) - REMINDER["before_minutes"]
            key = f"class_{wd}_{r}"
            if current == notify_t and key not in self.done_today:
                matched = [c for c in self.courses
                           if isinstance(c, dict) and c.get("day")==wd and c.get("row")==r]
                if matched:
                    self.done_today.add(key)
                    c = matched[0]
                    self.popup_fn(f"还有{REMINDER['before_minutes']}分钟上课啦",
                                  f"[b]{c['name']}[/b]\n{c['room']}\n{c['teacher']}\n{time_str}")

# ============ 弹出窗口 ============
def make_popup(title, msg):
    content = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(12))
    lbl = Label(text=msg, font_size=sp(14), color=(0.4,0.1,0.3,1),
               font_name=DEFAULT_FONT or "", markup=True, halign="center", valign="middle")
    lbl.bind(texture_size=lambda s,v: s.setter("size")(s,(s.width,v[1]+dp(20))))
    lbl.size_hint = (1, None)
    lbl.height = sp(60)
    btn = Button(text="我知道啦", size_hint=(1,0.35), background_color=(1,0.5,0.7,1))
    if DEFAULT_FONT:
        btn.font_name = DEFAULT_FONT
    btn.font_size = sp(14)
    content.add_widget(lbl)
    content.add_widget(btn)
    popup = Popup(title=title, content=content, size_hint=(0.85,0.4),
                  auto_dismiss=False, title_color=(0.4,0.1,0.3,1))
    if DEFAULT_FONT:
        popup.title_font = DEFAULT_FONT
    btn.bind(on_release=popup.dismiss)
    return popup

# ============ 欢迎页 ============
class WelcomeScreen(FloatLayout):
    def __init__(self, on_enter, **kw):
        super().__init__(**kw)
        self.on_enter = on_enter
        with self.canvas.before:
            Color(1,0.88,0.93,1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._bgupd, pos=self._bgupd)
        self.heart_root = FloatLayout(size_hint=(1,1), pos=(0,0))
        self.add_widget(self.heart_root)
        Clock.schedule_interval(lambda dt: spawn_heart(self.heart_root, Window.height), 0.3)
        center = BoxLayout(orientation="vertical", size_hint=(0.9,0.65),
                          pos_hint={"center_x":0.5,"center_y":0.5}, spacing=dp(12))
        center.add_widget(EmojiLabel(text_cn="", text_emoji="💖", font_size=sp(48), color=(1,0.3,0.5,1)))
        center.add_widget(EmojiLabel(text_cn=f" {GF_NAME}的爱心课表", text_emoji="💕",
                                     font_size=sp(22), color=(1,0.35,0.55,1), bold=True))
        center.add_widget(EmojiLabel(text_cn=f"{BF_NAME} 想你了", text_emoji="❤️",
                                     font_size=sp(14), color=(0.9,0.3,0.5,1)))
        quote = Label(text=random.choice(LOVE_QUOTES), font_size=sp(12), color=(0.7,0.3,0.5,1),
                     font_name=DEFAULT_FONT or "", halign="center", valign="middle",
                     text_size=(dp(280),None), size_hint=(1,None))
        quote.height = sp(40)
        btn = Button(text="点我进入课表", size_hint=(0.7,0.15), pos_hint={"center_x":0.5},
                    background_color=(1,0.5,0.7,1), font_size=sp(14), color=(1,1,1,1))
        if DEFAULT_FONT:
            btn.font_name = DEFAULT_FONT
        btn.bind(on_release=lambda x: self._go())
        tip = Label(text=f"{WELCOME_AUTO_GO}秒后自动进入...", font_size=sp(10),
                   color=(0.8,0.5,0.6,1), font_name=DEFAULT_FONT or "")
        center.add_widget(Label(size_hint=(1,0.01), text=""))
        center.add_widget(quote)
        center.add_widget(Label(size_hint=(1,0.01), text=""))
        center.add_widget(btn)
        center.add_widget(tip)
        self.add_widget(center)
        self.auto_event = Clock.schedule_once(lambda dt: self._go(), WELCOME_AUTO_GO)
    def _go(self):
        try:
            self.auto_event.cancel()
        except Exception:
            pass
        self.on_enter()
    def _bgupd(self, *a):
        self.bg.pos = self.pos
        self.bg.size = self.size

# ============ 课表主界面 ============
class ScheduleScreen(FloatLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.courses = load_courses()
        self.color_map = {}
        for c in self.courses:
            if isinstance(c, dict) and c.get("name") not in self.color_map:
                self.color_map[c["name"]] = COLORS[len(self.color_map) % len(COLORS)]

        # 背景
        with self.canvas.before:
            Color(1,0.92,0.94,1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bg_update = lambda s, *x: self._set_bg(s)
        self.bind(size=self.bg_update, pos=self.bg_update)

        # 顶栏
        self.top_bar = BoxLayout(size_hint=(1,None), height=dp(120),
                               pos_hint={"top":1}, orientation="vertical",
                               padding=[dp(10),dp(12),dp(10),dp(6)])
        with self.top_bar.canvas.before:
            Color(1,0.42,0.6,1)
            self.tb_rect = RoundedRectangle(radius=[0,0,dp(18),dp(18)])
        self.tb_update = lambda s, *x: self._set_tb(s)
        self.top_bar.bind(size=self.tb_update, pos=self.tb_update)
        self.top_bar.add_widget(EmojiLabel(text_cn=f" {GF_NAME}的爱心课表 ", text_emoji="💕",
                                           font_size=sp(20), color=(1,1,1,1), bold=True))
        self.top_bar.add_widget(Label(text=SCHOOL, font_size=sp(13), color=(1,0.92,0.95,1),
                                      font_name=DEFAULT_FONT or ""))
        self.top_bar.add_widget(EmojiLabel(text_cn=f" {BF_NAME}爱{GF_NAME}  ·  {SEMESTER} ",
                                           text_emoji="❤️", font_size=sp(11), color=(1,0.9,0.95,1)))
        self.add_widget(self.top_bar)

        # 课表网格
        self.sv = ScrollView(size_hint=(1,None), height=dp(540),
                             pos_hint={"center_x":0.5,"top":0.74})
        self.grid = GridLayout(cols=7, rows=11, size_hint_y=None, spacing=dp(3), padding=[dp(6),dp(4)])
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.build_grid()
        self.sv.add_widget(self.grid)
        self.add_widget(self.sv)

        # 底栏
        self.bottom = BoxLayout(size_hint=(1,None), height=dp(60), pos_hint={"bottom":1})
        with self.bottom.canvas.before:
            Color(1,0.42,0.6,1)
            self.bb_rect = RoundedRectangle(radius=[dp(18),dp(18),0,0])
        self.bb_update = lambda s, *x: self._set_bb(s)
        self.bottom.bind(size=self.bb_update, pos=self.bb_update)
        self.bottom.add_widget(EmojiLabel(text_cn=" 做这个课表的时候，每一行代码都写满了想你 ",
                                           text_emoji="💕", font_size=sp(12), color=(1,1,1,1)))
        self.add_widget(self.bottom)

        # 爱心层
        self.heart_root = FloatLayout(size_hint=(1,1), pos=(0,0))
        self.heart_root.opacity = 0.7
        self.heart_root.bind(on_touch_down=lambda *a: False)
        self.add_widget(self.heart_root)
        Clock.schedule_interval(lambda dt: spawn_heart(self.heart_root, Window.height), 0.6)

        # 启动提醒
        self.engine = ReminderEngine(self.courses, self._show_notify)
        Clock.schedule_interval(lambda dt: self.engine.check(), 30)

    def _set_bg(self, s):
        self.bg.pos = s.pos
        self.bg.size = s.size

    def _set_tb(self, s):
        self.tb_rect.pos = s.pos
        self.tb_rect.size = s.size

    def _set_bb(self, s):
        self.bb_rect.pos = s.pos
        self.bb_rect.size = s.size

    def _show_notify(self, title, msg):
        popup = make_popup(title, msg)
        popup.open()

    def build_grid(self):
        for d in ["", "周一","周二","周三","周四","周五","周六"]:
            self.grid.add_widget(Label(text=d, font_size=sp(13), bold=True,
                                     color=(1,0.42,0.6,1), size_hint_y=None, height=dp(36),
                                     font_name=DEFAULT_FONT or ""))
        for r in range(10):
            if r == 4:
                self.grid.add_widget(EmojiLabel(text_cn=f" 午休 {LUNCH_BREAK['start']}-{LUNCH_BREAK['end']}",
                                               text_emoji="🍱", font_size=sp(12), color=(0.8,0.3,0.5,1),
                                               size_hint_y=None, height=dp(48)))
            else:
                p = PERIODS[r]
                self.grid.add_widget(Label(text=f"{p[0]}\n{p[1]}", font_size=sp(10),
                                         color=(0.5,0.3,0.4,1), size_hint_y=None, height=dp(60),
                                         font_name=DEFAULT_FONT or ""))
            for day in range(1, 7):
                if r == 4:
                    cell = Label(text=f"{LUNCH_BREAK['start']}\n{LUNCH_BREAK['end']}",
                                font_size=sp(11), color=(0.8,0.3,0.5,1), size_hint_y=None, height=dp(48),
                                font_name=DEFAULT_FONT or "")
                    with cell.canvas.before:
                        Color(1,0.88,0.92,1)
                        cell._r = RoundedRectangle(radius=[dp(8)]*4)
                    cell._upd = lambda s, *x: self._set_rect(s)
                    cell.bind(size=cell._upd, pos=cell._upd)
                else:
                    cell = self._day_cell(day, r)
                self.grid.add_widget(cell)

    def _set_rect(self, s):
        s._r.pos = s.pos
        s._r.size = s.size

    def _day_cell(self, day, row_idx):
        box = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(60), spacing=dp(2))
        with box.canvas.before:
            Color(1,0.97,0.98,1)
            box._r = RoundedRectangle(radius=[dp(8)]*4)
        box._upd = lambda s, *x: self._set_box_rect(s)
        box.bind(size=box._upd, pos=box._upd)
        for c in self.courses:
            if isinstance(c, dict) and c.get("day")==day and c.get("row")==row_idx:
                card = CourseCard(course=c, color=self.color_map.get(c["name"], COLORS[0]))
                card.bind(on_release=lambda btn, cc=c: self.show_detail(cc))
                box.add_widget(card)
        return box

    def _set_box_rect(self, s):
        s._r.pos = s.pos
        s._r.size = s.size

    def show_detail(self, c):
        popup = make_popup(f"{BF_NAME}想你了", f"[b]{c['name']}[/b]\n📍 {c['room']}\n👤 {c['teacher']}")
        popup.open()

# ============ App ============
class LoveScheduleApp(App):
    def build(self):
        Window.clearcolor = (1,0.94,0.96,1)
        self.sm = FloatLayout(size_hint=(1,1))
        self.show_welcome()
        return self.sm
    def show_welcome(self):
        self.sm.clear_widgets()
        self.sm.add_widget(WelcomeScreen(on_enter=self.show_schedule))
    def show_schedule(self):
        self.sm.clear_widgets()
        self.sm.add_widget(ScheduleScreen())

if __name__ == "__main__":
    LoveScheduleApp().run()
