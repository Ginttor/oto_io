# oto_io_kivy.py - Version Kivy de oto_io
# Reutiliza la logica del script original (punt, vora, orar->generar_orario).
# Copyright 2026 - Apache 2.0

import os
import random
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

# ---------------------------------------------------------------- datos
ARCH_FILE = "arch.txt"
ORRA_FILE = "orra.txt"

DEFAULT_ORRA = (
    "o:L:6-21.:...;...;...;...;...;...;...;...\n"
    "o:M:6-21.:...;...;...;...;...;...;...;...\n"
    "o:m:6-21.:...;...;...;...;...;...;...;...\n"
    "o:J:6-21.:...;...;...;...;...;...;...;...\n"
    "o:V:6-21.:...;...;...;...;...;...;...;...\n"
    "o:S:6-21.:...;...;...;...;...;...;...;...\n"
    "o:V:6-21.:...;...;...;...;...;...;...;..."
)

def init_files():
    if not os.path.exists(ARCH_FILE):
        open(ARCH_FILE, "w", encoding="utf-8").close()
    if not os.path.exists(ORRA_FILE):
        with open(ORRA_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_ORRA)

def load_arch():
    with open(ARCH_FILE, "r", encoding="utf-8") as f:
        return f.read().split("\n")

def save_arch(arch):
    # Limpieza equivalente al .replace("\n\n", "\n") del original
    arch = [l for l in arch if l.strip() != ""]
    with open(ARCH_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(arch))

def append_arch(line):
    arch = load_arch()
    arch.append(line)
    save_arch(arch)

def load_orra():
    with open(ORRA_FILE, "r", encoding="utf-8") as f:
        return [l for l in f.read().split("\n") if l.strip()]

# ---------------------------------------------------------------- logica
def punt(a):
    """Puerto directo de punt() del original. Usa maxsplit=4 para no perder
    los ':' que pudiera tener el comentario."""
    arch = load_arch()
    if a >= len(arch) or ":" not in arch[a]:
        return
    bnp = arch[a].split(":", 4)
    if len(bnp) < 5:
        return
    try:
        bnpp, bnpt = int(bnp[1]), int(bnp[2])
    except ValueError:
        return
    bnpp += 1
    if bnpp < bnpt:
        arch[a] = bnp[0] + ":" + str(bnpp) + ":" + bnp[2] + ":" + bnp[3] + ":" + bnp[4]
    else:
        if bnp[3] == "":
            arch[a] = ""          # pendiente completada -> se elimina
        elif bnpp <= bnpt:
            arch[a] = bnp[0] + ":" + str(bnpp) + ":" + bnp[2] + ":" + bnp[3] + ":" + bnp[4]
    save_arch(arch)

def vora():
    """Puerto directo de vora(): resetea actividades a 0 y quita horario."""
    arch = load_arch()
    out = []
    for i in arch:
        if i.count("a:") > 0:
            bnp = i.split(":", 4)
            out.append(bnp[0] + ":0:" + bnp[2] + ":" + bnp[3] + ":" + bnp[4])
        elif i.count("o:") > 0:
            continue
        else:
            out.append(i)
    save_arch(out)

def generar_orario():
    """Puerto del branch 'else' de orar(). Reparte actividades
    en los slots de orra.txt según categoria (1/2/3 -> !/!!/!!!)."""
    arch = load_arch()
    if any(l.startswith("o:") and not l.startswith("o:tt:") for l in arch):
        return False  # ya existe horario
    arch = [l for l in arch if not l.startswith("o:")]  # limpiar residuos
    orra = load_orra()

    ahora = datetime.now()
    arch.append("o:tt:" + str(ahora))

    # clasificar actividades por categoria, respetando el orden del original
    oa1, oa2, oa3 = [], [], []
    for x, line in enumerate(arch):
        parts = line.split(":", 4)
        if len(parts) < 5 or parts[0] != "a":
            continue
        try:
            lim, cat = int(parts[2]), int(parts[3])
        except ValueError:
            continue
        if cat == 1:   oa1.append(str(x))
        elif cat == 2: oa2.append(str(x))
        elif cat == 3: oa3.append(str(x))

    oa = oa3 + oa2 + oa1
    oo = list(orra)

    for oa_idx in oa:
        parts = arch[int(oa_idx)].split(":", 4)
        try:
            target, cat = int(parts[2]), int(parts[3])
        except ValueError:
            continue
        w, pss = 0, 0
        while w < target:
            x = random.randint(0, len(oo) - 1)
            lt = oo[x].split(":", 3)       # maxsplit=3 protege los ':'
            if len(lt) < 4:
                break
            slots = lt[3].split(";")
            y = random.randint(0, len(slots) - 1)
            cda = slots[y].count(".") - slots[y].count("!")
            if cda >= cat and ("," + oa_idx) not in slots[y]:
                slots[y] += "," + oa_idx + "!" * cat
                lt[3] = ";".join(slots)
                oo[x] = ":".join(lt)
                w += 1
            pss += 1
            if pss >= 168:
                w += 1

    arch.extend(oo)
    save_arch(arch)
    return True

def get_today_info():
    """Vista resumida del horario de hoy (adaptación del branch 'if' de orar())."""
    arch = load_arch()
    sched = [l for l in arch if l.startswith("o:") and not l.startswith("o:tt:")]
    if not sched:
        return None
    idx = datetime.now().weekday()          # 0 = lunes ... 6 = domingo
    if idx >= len(sched):
        return None
    line = sched[idx]
    parts = line.split(":", 3)
    if len(parts) < 4:
        return None
    try:
        start_h, end_h = map(int, parts[2].replace(".", "").split("-"))
    except (ValueError, IndexError):
        return None
    slots = parts[3].split(";")
    cur_h = datetime.now().hour
    hours = list(range(start_h, end_h + 1))
    active, cur_slot = [], None
    for x in range(0, len(hours) - 1, 2):
        k = x // 2
        if k >= len(slots):
            continue
        if hours[x] <= cur_h <= hours[x + 1]:
            cur_slot = (hours[x], hours[x + 1])
            for s in slots[k].replace("!", "").split(","):
                if s.strip():
                    try:
                        active.append(int(s))
                    except ValueError:
                        pass
            break
    return {
        "name": parts[1], "start": start_h, "end": end_h,
        "cur_slot": cur_slot, "active": active,
    }

# ---------------------------------------------------------------- UI
KV = '''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        Label:
            text: 'oto_io (Kivy)'
            font_size: 36
            size_hint_y: 0.15
        Label:
            id: banner
            text: ''
            font_size: 14
            size_hint_y: 0.15
            text_size: self.width, None
            halign: 'center'
        Label:
            id: stats
            text: ''
            font_size: 14
            size_hint_y: 0.1
        Button:
            text: 'Pendientes (p)'
            font_size: 20
            size_hint_y: 0.15
            on_release: app.go('pending')
        Button:
            text: 'Actividades (a)'
            font_size: 20
            size_hint_y: 0.15
            on_release: app.go('activities')
        Button:
            text: 'Horario (o)'
            font_size: 20
            size_hint_y: 0.15
            on_release: app.go('schedule')

<PendingScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 8
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: '< Inicio'
                on_release: app.go('home')
            Button:
                text: 'Nueva pendiente'
                on_release: root.add_pending()
        ScrollView:
            GridLayout:
                id: list_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 6

<ActivitiesScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 8
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: '< Inicio'
                on_release: app.go('home')
            Button:
                text: 'Nueva actividad'
                on_release: root.add_activity()
        ScrollView:
            GridLayout:
                id: list_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 6

<ScheduleScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 8
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: '< Inicio'
                on_release: app.go('home')
            Button:
                text: 'Generar'
                on_release: root.generate()
            Button:
                text: 'Reset'
                on_release: root.reset()
        Label:
            id: title
            text: ''
            size_hint_y: 0.08
            font_size: 18
        ScrollView:
            size_hint_y: 0.55
            Label:
                id: info
                text: ''
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                halign: 'left'
                valign: 'top'
        ScrollView:
            size_hint_y: 0.27
            GridLayout:
                id: actions_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 6
'''

class HomeScreen(Screen):
    def on_enter(self):
        arch = load_arch()
        lines = [l for l in arch if l.strip()]
        self.ids.banner.text = random.choice(lines) if lines else '(archivo vacio)'
        n_p = sum(1 for l in arch if l.startswith("p:"))
        n_a = sum(1 for l in arch if l.startswith("a:"))
        n_o = sum(1 for l in arch if l.startswith("o:") and not l.startswith("o:tt:"))
        self.ids.stats.text = f"p:{n_p}   a:{n_a}   o:{n_o}"

class PendingScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        arch = load_arch()
        grid = self.ids.list_grid
        grid.clear_widgets()
        for i, line in enumerate(arch):
            if not line.startswith("p:"):
                continue
            parts = line.split(":", 4)
            if len(parts) < 5:
                continue
            try:
                cur, lim = int(parts[1]), int(parts[2])
            except ValueError:
                continue
            done = cur >= lim
            row = BoxLayout(size_hint_y=None, height=50, spacing=6)
            lbl = Label(text=f"[{i}] {cur}/{lim}  {parts[4].strip()}",
                        size_hint_x=0.75, halign='left', valign='middle')
            lbl.bind(size=lambda l, v: setattr(l, 'text_size', v))
            if done:
                lbl.color = (0.5, 1, 0.5, 1)
            row.add_widget(lbl)
            btn = Button(text="+1", size_hint_x=0.25, disabled=done)
            btn.bind(on_release=lambda b, idx=i: self.on_punt(idx))
            row.add_widget(btn)
            grid.add_widget(row)

    def on_punt(self, idx):
        punt(idx)
        self.refresh()

    def add_pending(self):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        lim_in = TextInput(hint_text="limite (entero > 0)", input_filter="int", multiline=False)
        com_in = TextInput(hint_text="comentario", multiline=False)
        content.add_widget(lim_in)
        content.add_widget(com_in)
        row = BoxLayout(size_hint_y=0.4, spacing=10)
        ok, cancel = Button(text="OK"), Button(text="Cancelar")
        row.add_widget(ok); row.add_widget(cancel)
        content.add_widget(row)
        pop = Popup(title="Nueva pendiente", content=content, size_hint=(0.8, 0.5))

        def do_ok(*a):
            try:
                lim = int(lim_in.text)
                if lim <= 0:
                    raise ValueError
            except ValueError:
                return
            append_arch(f"p:0:{lim}:: {com_in.text}")
            pop.dismiss()
            self.refresh()

        ok.bind(on_release=do_ok)
        cancel.bind(on_release=pop.dismiss)
        pop.open()

class ActivitiesScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        arch = load_arch()
        grid = self.ids.list_grid
        grid.clear_widgets()
        for i, line in enumerate(arch):
            if not line.startswith("a:"):
                continue
            parts = line.split(":", 4)
            if len(parts) < 5:
                continue
            try:
                cur, lim, cat = int(parts[1]), int(parts[2]), parts[3]
            except ValueError:
                continue
            done = cur >= lim
            row = BoxLayout(size_hint_y=None, height=50, spacing=6)
            lbl = Label(text=f"[{i}] {cur}/{lim} cat={cat}  {parts[4].strip()}",
                        size_hint_x=0.75, halign='left', valign='middle')
            lbl.bind(size=lambda l, v: setattr(l, 'text_size', v))
            if done:
                lbl.color = (0.5, 1, 0.5, 1)
            row.add_widget(lbl)
            btn = Button(text="+1", size_hint_x=0.25, disabled=done)
            btn.bind(on_release=lambda b, idx=i: self.on_punt(idx))
            row.add_widget(btn)
            grid.add_widget(row)

    def on_punt(self, idx):
        punt(idx)
        self.refresh()

    def add_activity(self):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        lim_in = TextInput(hint_text="limite (entero > 0)", input_filter="int", multiline=False)
        cat_in = TextInput(hint_text="categoria 1/2/3", input_filter="int", multiline=False)
        com_in = TextInput(hint_text="comentario", multiline=False)
        content.add_widget(lim_in); content.add_widget(cat_in); content.add_widget(com_in)
        row = BoxLayout(size_hint_y=0.4, spacing=10)
        ok, cancel = Button(text="OK"), Button(text="Cancelar")
        row.add_widget(ok); row.add_widget(cancel)
        content.add_widget(row)
        pop = Popup(title="Nueva actividad", content=content, size_hint=(0.8, 0.5))

        def do_ok(*a):
            try:
                lim = int(lim_in.text)
                cat = int(cat_in.text)
                if lim <= 0 or cat not in (1, 2, 3):
                    raise ValueError
            except ValueError:
                return
            append_arch(f"a:0:{lim}:{cat}: {com_in.text}")
            pop.dismiss()
            self.refresh()

        ok.bind(on_release=do_ok)
        cancel.bind(on_release=pop.dismiss)
        pop.open()

class ScheduleScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        arch = load_arch()
        info = get_today_info()
        if info is None:
            self.ids.title.text = ""
            has = any(l.startswith("o:") and not l.startswith("o:tt:") for l in arch)
            self.ids.info.text = ("(sin horario generado aun)" if not has
                                  else "(sin informacion para hoy)")
            self.ids.actions_grid.clear_widgets()
            return
        lines = [f"Hoy: {info['name']}  ({info['start']}h - {info['end']}h)"]
        if info["cur_slot"]:
            lines.append(f"Slot actual: {info['cur_slot'][0]}h - {info['cur_slot'][1]}h")
        else:
            lines.append("(fuera de rango horario)")
        lines.append("")
        for idx in info["active"]:
            if 0 <= idx < len(arch) and ":" in arch[idx]:
                lines.append(f"  [{idx}] {arch[idx]}")
        self.ids.title.text = f"Horario de hoy ({info['name']})"
        self.ids.info.text = "\n".join(lines)

        grid = self.ids.actions_grid
        grid.clear_widgets()
        for idx in info["active"]:
            if 0 <= idx < len(arch) and ":" in arch[idx]:
                row = BoxLayout(size_hint_y=None, height=45, spacing=6)
                row.add_widget(Label(text=arch[idx], size_hint_x=0.75))
                btn = Button(text="+1", size_hint_x=0.25)
                btn.bind(on_release=lambda b, i=idx: self.on_punt(i))
                row.add_widget(btn)
                grid.add_widget(row)

    def on_punt(self, idx):
        punt(idx)
        self.refresh()

    def generate(self):
        if not generar_orario():
            self._toast("Ya existe un horario. Usa 'Reset' primero.")
        self.refresh()

    def reset(self):
        vora()
        self.refresh()

    def _toast(self, msg):
        Popup(title="Info", content=Label(text=msg),
              size_hint=(0.7, 0.25)).open()

class OtoApp(App):
    def build(self):
        init_files()
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PendingScreen(name="pending"))
        sm.add_widget(ActivitiesScreen(name="activities"))
        sm.add_widget(ScheduleScreen(name="schedule"))
        return sm

    def go(self, name):
        self.root.current = name

if __name__ == "__main__":
    OtoApp().run()