import os
from cudatext import *
from cudax_lib import get_translation

_ = get_translation(__file__)

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'live_word_count.ini')

class Command:
    def __init__(self):
        self._enabled = False
        self._last = None

    def on_open(self, ed):
        if self._enabled:
            ed.set_prop(PROP_RULER, True)
            self._last = None
            self.update(ed)

    def on_change(self, ed):
        if self._enabled:
            self.update(ed)

    def update(self, ed):
        n = ed.get_line_count()
        text = '\n'.join(ed.get_text_line(i) for i in range(n))
        words = len(text.split())
        chars = len(text)
        new = f"Words: {words}  |  Chars: {chars}"
        if new != self._last:
            ed.set_prop(PROP_RULER_TEXT, new)
            self._last = new

    def toggle(self):
        self._enabled = not self._enabled
        if self._enabled:
            ed.set_prop(PROP_RULER, True)
            self._last = None
            self.update(ed)
            app_proc(PROC_EVENTS_SUB, 'live_word_count;on_change;;')
        else:
            ed.set_prop(PROP_RULER_TEXT, "")
            ed.set_prop(PROP_RULER, False)
            app_proc(PROC_EVENTS_UNSUB, 'live_word_count;on_change;;')
            
