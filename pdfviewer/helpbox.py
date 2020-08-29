from tkinter import *
from PIL import Image, ImageTk
from pdfviewer.config import *
import os

class HelpBox(Frame):

    def __init__(self, master, **kw):
        Frame.__init__(self, master, **kw)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        Label(self, text="Iris-PDFViewer", anchor='nw', width=100,
              font="OpenSans 22 bold", fg='white', bg=BACKGROUND_COLOR, bd=2).grid(row=0, column=0, padx=20, pady=20)

        Label(self, text="Made by IRIS", anchor='nw', width=100,
              font="OpenSans 10 bold", fg='#00ffff', bg=BACKGROUND_COLOR, bd=2).grid(row=2, column=0, padx=20, pady=20)

        text_frame = Frame(self, height=440, width=550, bg='#0d7377', bd=2, relief=SUNKEN)
        text_frame.grid(row=1, column=0)
  

        text_frame.grid_propagate(False)

        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        text_box = Text(text_frame, borderwidth=4, relief="sunken", bg='#323232',
                        fg='white', font="OpenSans 12", wrap='word')

        help_file = os.getcwd()+"/help.txt"

        with open(help_file, 'r') as infile:
            texts = infile.read()
        texts = [text + '\n\n\n' for text in texts.split('\n\n\n')]

        text_box.insert('1.0', texts[0])
        texts = texts[1:]

        paths = ['darkmode.png',
                 'voice.png']
        icon_dir = os.getcwd() + "/icons"
        self.images = [ImageTk.PhotoImage(Image.open(os.path.join(icon_dir, path))) for path in paths]

        for text, image in zip(texts, self.images):
            text_box.image_create(END, image=image)
            text_box.insert(END, ' ' + text)

        self.images.extend([ImageTk.PhotoImage(Image.open(os.path.join(icon_dir, path)))
                            for path in ['prev_file.png', 'next_file.png']])

        text_box.image_create(END, image=self.images[-2])
        text_box.image_create(END, image=self.images[-1])
        text_box.insert(END, ' ' + texts[-2])

        text_box.insert(END, texts[-1].split('\n\n')[0] + '\n')
        toolbar_image = icon_dir + "/toolbar.png"
        self.images.append(ImageTk.PhotoImage(Image.open(os.path.join(ROOT_PATH, toolbar_image))))
        text_box.image_create(END, image=self.images[-1])
        text_box.insert(END, '\n\n' + '\n\n'.join(texts[-1].split('\n\n')[1:]))

        text_box.config(state=DISABLED)
        text_box.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scroll_bar = Scrollbar(text_frame, command=text_box.yview, bg=BACKGROUND_COLOR)
        scroll_bar.grid(row=0, column=1, sticky='nsew')

        text_box['yscrollcommand'] = scroll_bar.set
