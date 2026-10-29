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
        n = ed.get_line_count()
        text = '\n'.join(ed.get_text_line(i) for i in range(n))
        words = len(text.split())
        chars = len(text)
        new = f"Words: {words} | Characters: {chars}"
        if new != self._last:
            ed.set_prop(PROP_CORNER_TEXT, new)
            self._last = new

    def toggle(self):
        self._enabled = not self._enabled
        if self._enabled:
            self._last = None
            self.update(ed)
            app_proc(PROC_EVENTS_SUB, 'cuda_live_word_count;on_change;;')
            app_proc(PROC_EVENTS_SUB, 'cuda_live_word_count;on_open;;')
        else:
            ed.set_prop(PROP_CORNER_TEXT, "")
            app_proc(PROC_EVENTS_UNSUB, 'cuda_live_word_count;on_change;;')
            app_proc(PROC_EVENTS_UNSUB, 'cuda_live_word_count;on_open;;')

