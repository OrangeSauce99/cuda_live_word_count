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
    self._enabled = not self._enabled
    proc = PROC_EVENTS_SUB if self._enabled else PROC_EVENTS_UNSUB
    for event in ('on_open', 'on_change_slow'):
        app_proc(proc, f'live_word_count;{event};;')

    if self._enabled:
        ed.set_prop(PROP_RULER, True)
        self._last = None
        self.update(ed)
    else:
        ed.set_prop(PROP_RULER_TEXT, "")
        ed.set_prop(PROP_RULER, False)

