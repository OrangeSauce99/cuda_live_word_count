from cudatext import *

class Command:
    def __init__(self):
        self._enabled = False
        self._last = None

    def on_open(self, ed):
        if self._enabled:
            self._last = None
            self.update(ed)

    def on_change(self, ed):
        if self._enabled:
            self.update(ed)

    def update(self, ed):
        words = 0
        chars = 0
        for i in range(ed.get_line_count()):
            line = ed.get_text_line(i)
            words += len(line.split())
            chars += len(line)
        new = f"Words: {words} | Characters: {chars}"
        if new != self._last:
            ed.set_prop(PROP_CORNER_TEXT, new)
            colors = app_proc(PROC_THEME_UI_DICT_GET, '')
            ed.set_prop(PROP_CORNER_COLOR_FONT, colors['EdTextFont']['color'])
            ed.set_prop(PROP_CORNER_COLOR_BACK, colors['EdTextBg']['color'])
            self._last = new

    def toggle(self):
        self._enabled = not self._enabled
        if self._enabled:
            self._last = None
            self.update(ed)
            app_proc(PROC_EVENTS_SUB, 'cuda_live_word_count;on_change,on_open;;')
        else:
            ed.set_prop(PROP_CORNER_TEXT, "")
            app_proc(PROC_EVENTS_UNSUB, 'cuda_live_word_count;on_change,on_open;;')

