import os
from cudatext import *
from cudax_lib import get_translation

_ = get_translation(__file__)

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'live_word_count.ini')

class Command:
    def __init__(self):
        self._enabled = True
        self._last = None

    def on_open(self, ed):
        if self._enabled:
            ed.set_prop(PROP_RULER, True)
            self._last = None
            self.update(ed)

    def on_caret(self, ed):
        if self._enabled:
            ed.set_prop(PROP_RULER, True)
            self._last = None
            self.update(ed)

    def on_change_slow(self, ed):
        if self._enabled:
            self.update(ed)

    def update(self, ed):
        text = ed.get_text_all()
        words = len(text.split())
        chars = len(text)
        new = f"Words: {words}  |  Chars: {chars}"
        if new != self._last:
            ed.set_prop(PROP_RULER_TEXT, new)
            self._last = new

    def toggle(self):
        if self._enabled: 
            self._enabled = False
            ed.set_prop(PROP_RULER_TEXT, "")
            ed.set_prop(PROP_RULER, False)
        else:
            self._enabled = True
            ed.set_prop(PROP_RULER, True)
            self._last = None
            self.update(ed)   

