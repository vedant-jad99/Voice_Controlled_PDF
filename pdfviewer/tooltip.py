from tkinter import *


class ToolTip(object):

    def __init__(self, icon, text):
        self.waittime = 500
        self.wraplength = 180
        self.icon = icon
        self.text = text
        self.icon.bind("<Enter>", self.enter)
        self.icon.bind("<Leave>", self.leave)
        self.icon.bind("<ButtonPress>", self.leave)
        self.idx = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.idx = self.icon.after(self.waittime, self.showtip)

    def unschedule(self):
        idx = self.idx
        self.idx = None
        if idx:
            self.icon.after_cancel(idx)

    def showtip(self, event=None):
        x, y, cx, cy = self.icon.bbox("insert")
        x += self.icon.winfo_rootx() + 25
        y += self.icon.winfo_rooty() + 20
        self.tw = Toplevel(self.icon)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background="#323232",fg='white', relief='solid', borderwidth=1,
                      wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
