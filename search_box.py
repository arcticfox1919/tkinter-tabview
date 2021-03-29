import tkinter as tk
from tkinter import Toplevel, Listbox
from tkinter import Entry
from tkinter import StringVar


class SearchBox(Entry):

    def __init__(self, master=None, callback=None, lines=8, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.str_var = tk.StringVar()
        self["textvariable"] = self.str_var
        self.str_var.trace('w', self._callback)
        self.window = None
        self.lines = lines
        self.callback = callback
        self.master = master
        self.list_var = StringVar()
        self.prev_text = ""

    def _callback(self, *_):
        current_text = self.str_var.get()
        if current_text != self.prev_text:
            self.prev_text = current_text
            self.callback(current_text)

    def update(self, item_list):
        if item_list and self.window:
            self.list_var.set(item_list)
        elif not item_list and self.window:
            self._hide()
        elif item_list and not self.window:
            self._show()
            self.list_var.set(item_list)

    def _show(self):
        self.window = Toplevel()
        self.window.transient(self.master)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", 1)
        self.window.attributes("-alpha", 0.9)
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 6
        self.window.wm_geometry("+%d+%d" % (x, y))
        self._create_list()
        # self.window.mainloop()

    def _listbox_click(self, event):
        widget = event.widget
        cur_item = widget.get(widget.curselection())
        self.str_var.set(cur_item)
        self._hide()

    def _create_list(self):
        list_box = Listbox(self.window, selectmode=tk.SINGLE, listvariable=self.list_var, height=self.lines)
        list_box.bind('<<ListboxSelect>>', self._listbox_click)
        list_box.pack(fill=tk.BOTH, expand=tk.YES)

    def _hide(self):
        if self.window:
            self.window.destroy()
            self.window = None
