import io
import pdfplumber
import PyPDF2
import threading
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
import PIL.ImageOps   

from pdfviewer.config import *
from pdfviewer.hoverbutton import HoverButton
from pdfviewer.helpbox import HelpBox
from pdfviewer.menubox import MenuBox
from pdfviewer.display_canvas import DisplayCanvas
# Python program to translate 
# speech to text and text to speech 
  
  
import speech_recognition as sr 
import pyttsx3  
  
# Initialize the recognizer  
r = sr.Recognizer()  
  
# Function to convert text to 
# speech 
def SpeakText(command): 
      
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait() 
MyText=""  

mode=0
mode2=0
class PDFViewer(Frame):
    def listener(self):
        # Exception handling to handle 
        # exceptions at the runtime 
        global mode2
        while(mode2):
            try:         
                # use the microphone as source for input. 
                with sr.Microphone() as source2: 
                    
                    # wait for a second to let the recognizer 
                    # adjust the energy threshold based on 
                    # the surrounding noise level  
                    r.adjust_for_ambient_noise(source2, duration=0.2) 
                    
                    #listens for the user's input  
                    audio2 = r.listen(source2) 
                    
                    # Using ggogle to recognize audio 
                    MyText = r.recognize_google(audio2) 
                    MyText = MyText.lower()
                    # if MyText=='open files':
                    #     obj._open_file()

                    print("Did you say "+MyText) 
                    SpeakText(MyText)
                    if MyText.find('file')!=-1:
                        self._open_file()
                    if MyText.find('directory')!=-1:
                        self._open_dir()
                    if MyText.find('previous file')!=-1:
                        self._prev_file()
                    if MyText.find('next file')!=-1:
                        self._next_file()        
                    if MyText.find('previous page')!=-1:
                        self._prev_page()
                    if MyText.find('next page')!=-1:
                        self._next_page()
                    if MyText.find('voice')!=-1:
                        self._voice_mode
                        
                    if MyText.find('zoom in')!=-1:
                        self._zoom_in()
                    if MyText.find('zoom out')!=-1:
                        self._zoom_out()
                    if MyText.find('fit to screen')!=-1:
                        self._fit_to_screen()
                    if MyText.find('rotate')!=-1:
                        self.rotate()    
                    if MyText.find('dark')!=-1:
                        if mode==0:
                            self._dark_mode()
                    if MyText.find('light')!=-1:
                        if mode==1:
                            self._dark_mode()    
                    if MyText.find('open help')!=-1:
                        self._help()            
                    if MyText.find('exit')!=-1:
                        break
                    else:
                        print("NON RECOGNIZABLE")                         

            except sr.RequestError as e: 
                print("Could not request results; {0}".format(e)) 
                
            except sr.UnknownValueError: 
                print("unknown error occured")
        print('Exitted voice mode')        
    
    def _voice_mode(self):
        global mode2
        if mode2==0:
            mode2=1
            print('Started voice mode')
        else:
            mode2=0
        self.start_thread()

    def start_thread(self):
        threading.Thread(target=self.listener).start()    
        


    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.pdf = None
        self.page = None
        self.paths = list()
        self.pathidx = -1
        self.total_pages = 0
        self.pageidx = 0
        self.scale = 1.0
        self.rotate = 0
        self.save_path = None
        #self._voice_mode()
        self._init_ui()
        # self.command = command
        # print(command)

    def _init_ui(self):
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        h = hs - 100
        w = int(h / 1.414) + 100
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master.title("IRIS PDFViewer")

        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(0, weight=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        self.configure(bg=BACKGROUND_COLOR, bd=0)

        tool_frame = Frame(self, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        pdf_frame = Frame(self, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)

        tool_frame.grid(row=0, column=0, sticky='news')
        pdf_frame.grid(row=0, column=1, sticky='news')

        # Tool Frame
        tool_frame.columnconfigure(0, weight=1)
        tool_frame.rowconfigure(0, weight=0)
        tool_frame.rowconfigure(1, weight=1)
        tool_frame.rowconfigure(2, weight=0)
        tool_frame.rowconfigure(3, weight=2)

        options = MenuBox(tool_frame, image_path=os.path.join(ROOT_PATH, 'icons/options.png'))
        options.grid(row=0, column=0)

        options.add_item('Open Files...', self._open_file)
        options.add_item('Open Directory...', self._open_dir, seperator=True)
        options.add_item('Next File', self._next_file)
        options.add_item('Previous File', self._prev_file, seperator=True)
        options.add_item('Help...', self._help, seperator=True)
        options.add_item('Exit', self.master.quit)

        tools = Frame(tool_frame, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        tools.grid(row=2, column=0)

        HoverButton(tools, image_path=os.path.join(ROOT_PATH, 'icons/darkmode.png'), command=self._dark_mode,
                    width=50, height=50, bg=BACKGROUND_COLOR, bd=0, tool_tip="Dark Mode",
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(pady=2)

        HoverButton(tools, image_path=os.path.join(ROOT_PATH, 'icons/voice.png'), command=self._voice_mode,
                    width=50, height=50, bg=BACKGROUND_COLOR, bd=0, tool_tip="Voice Control",
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(pady=2)
  

        file_frame = Frame(tools, width=50, height=50, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        file_frame.pack(pady=2)

        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)

        HoverButton(file_frame, image_path=os.path.join(ROOT_PATH, 'icons/prev_file.png'), command=self._prev_file,
                    width=25, height=50, bg=BACKGROUND_COLOR, bd=0, tool_tip="Previous File",
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).grid(row=0, column=0)
        HoverButton(file_frame, image_path=os.path.join(ROOT_PATH, 'icons/next_file.png'), command=self._next_file,
                    width=25, height=50, bg=BACKGROUND_COLOR, bd=0, tool_tip="Next File",
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).grid(row=0, column=1)

        HoverButton(tool_frame, image_path=os.path.join(ROOT_PATH, 'icons/help.png'), command=self._help,
                    width=50, height=50, bg=BACKGROUND_COLOR, bd=0, tool_tip="Help",
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).grid(row=3, column=0, sticky='s')

        # PDF Frame
        pdf_frame.columnconfigure(0, weight=1)
        pdf_frame.rowconfigure(0, weight=0)
        pdf_frame.rowconfigure(1, weight=0)

        page_tools = Frame(pdf_frame, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        page_tools.grid(row=0, column=0, sticky='news')

        page_tools.rowconfigure(0, weight=1)
        page_tools.columnconfigure(0, weight=1)
        page_tools.columnconfigure(1, weight=0)
        page_tools.columnconfigure(2, weight=2)
        page_tools.columnconfigure(3, weight=0)
        page_tools.columnconfigure(4, weight=1)

        nav_frame = Frame(page_tools, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        nav_frame.grid(row=0, column=1, sticky='ns')

        HoverButton(nav_frame, image_path=os.path.join(ROOT_PATH, 'icons/first.png'),
                    command=self._first_page, bg=BACKGROUND_COLOR, bd=0, tool_tip='First Page',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=LEFT, expand=True)
        HoverButton(nav_frame, image_path=os.path.join(ROOT_PATH, 'icons/prev.png'),
                    command=self._prev_page, bg=BACKGROUND_COLOR, bd=0,tool_tip='Previous Page',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=LEFT, expand=True)

        self.page_label = Label(nav_frame, bg=BACKGROUND_COLOR, bd=0, fg='white', font='Arial 8',
                                text="Page {} of {}".format(self.pageidx, self.total_pages))
        self.page_label.pack(side=LEFT, expand=True)

        HoverButton(nav_frame, image_path=os.path.join(ROOT_PATH, 'icons/next.png'),
                    command=self._next_page, bg=BACKGROUND_COLOR, bd=0,tool_tip='Next Page',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=LEFT, expand=True)
        HoverButton(nav_frame, image_path=os.path.join(ROOT_PATH, 'icons/last.png'),
                    command=self._last_page, bg=BACKGROUND_COLOR, bd=0,tool_tip='Last Page',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=LEFT, expand=True)

        zoom_frame = Frame(page_tools, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        zoom_frame.grid(row=0, column=3, sticky='ns')

        HoverButton(zoom_frame, image_path=os.path.join(ROOT_PATH, 'icons/rotate.png'),
                    command=self._rotate, bg=BACKGROUND_COLOR, bd=0,tool_tip='Rotate',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=RIGHT, expand=True)
        HoverButton(zoom_frame, image_path=os.path.join(ROOT_PATH, 'icons/fullscreen.png'),
                    command=self._fit_to_screen, bg=BACKGROUND_COLOR, bd=0,tool_tip='Fit Screen',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=RIGHT, expand=True)

        self.zoom_label = Label(zoom_frame, bg=BACKGROUND_COLOR, bd=0, fg='white', font='Arial 8',
                                text="Zoom {}%".format(int(self.scale * 100)))
        self.zoom_label.pack(side=RIGHT, expand=True)

        HoverButton(zoom_frame, image_path=os.path.join(ROOT_PATH, 'icons/zoomout.png'),
                    command=self._zoom_out, bg=BACKGROUND_COLOR, bd=0,tool_tip='Zoom-In',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=RIGHT, expand=True)
        HoverButton(zoom_frame, image_path=os.path.join(ROOT_PATH, 'icons/zoomin.png'),
                    command=self._zoom_in, bg=BACKGROUND_COLOR, bd=0,tool_tip='Zoom-Out',
                    highlightthickness=0, activebackground=HIGHLIGHT_COLOR).pack(side=RIGHT, expand=True)

        canvas_frame = Frame(pdf_frame, bg=BACKGROUND_COLOR, bd=1, relief=SUNKEN)
        canvas_frame.grid(row=1, column=0, sticky='news')

        self.canvas = DisplayCanvas(canvas_frame, page_height=h-42, page_width=w-70)
        self.canvas.pack()

        self.grid(row=0, column=0, sticky='news')

        self.master.minsize(height=h, width=w)
        self.master.maxsize(height=h, width=w)

    def _reject(self):
        if self.pdf is None:
            return
        self.pathidx = min(self.pathidx + 1, len(self.paths))
        if self.pathidx == len(self.paths):
            self._reset()
            return
        self._load_file()

    def _reset(self):
        self.canvas.clear()
        self.pdf = None
        self.page = None
        self.paths = list()
        self.pathidx = -1
        self.total_pages = 0
        self.pageidx = 0
        self.scale = 1.0
        self.rotate = 0
        self.page_label.configure(text="Page {} of {}".format(self.pageidx, self.total_pages))
        self.zoom_label.configure(text="Zoom {}%".format(int(self.scale * 100)))
        self.master.title("PDFViewer")

    def _zoom_in(self):
        if self.pdf is None:
            return
        if self.scale == 2.5:
            return
        self.scale += 0.1
        self._update_page()

    def _zoom_out(self):
        if self.pdf is None:
            return
        if self.scale == 0.1:
            return
        self.scale -= 0.1
        self._update_page()

    def _fit_to_screen(self):
        if self.pdf is None:
            return
        if self.scale == 1.0:
            return
        self.scale = 1.0
        self._update_page()

    def _rotate(self):
        if self.pdf is None:
            return
        self.rotate = (self.rotate - 90) % 360
        self._update_page()

    def _next_page(self):
        if self.pdf is None:
            return
        if self.pageidx == self.total_pages:
            return
        self.pageidx += 1
        self._update_page()

    def _prev_page(self):
        if self.pdf is None:
            return
        if self.pageidx == 1:
            return
        self.pageidx -= 1
        self._update_page()

    def _last_page(self):
        if self.pdf is None:
            return
        if self.pageidx == self.total_pages:
            return
        self.pageidx = self.total_pages
        self._update_page()

    def _first_page(self):
        if self.pdf is None:
            return
        if self.pageidx == 1:
            return
        self.pageidx = 1
        self._update_page()

    def _next_file(self):
        if self.pdf is None:
            return
        if self.pathidx == len(self.paths) - 1:
            messagebox.showwarning("Warning", "Reached the end of list")
            return
        self.pathidx += 1
        self._load_file()

    def _prev_file(self):
        if self.pdf is None:
            return
        if self.pathidx == 0:
            messagebox.showwarning("Warning", "Reached the end of list")
            return
        self.pathidx -= 1
        self._load_file()

    def _dark_mode(self):
        global mode
        if self.pdf is None:
            return
        if mode==1:
            mode=0
        else:
            mode=1
        self._update_page()
    

    def _update_page(self):
        global mode
        page = self.pdf.pages[self.pageidx - 1]
        self.page = page.to_image(resolution=int(self.scale * 80))
        image = self.page.original.rotate(self.rotate)
        inverted_image = PIL.ImageOps.invert(image)
        print(image)
        if mode==0:
            self.canvas.update_image(image)
        else:
            self.canvas.update_image(inverted_image)
        self.page_label.configure(text="Page {} of {}".format(self.pageidx, self.total_pages))
        self.zoom_label.configure(text="Zoom {}%".format(int(self.scale * 100)))



    def _load_file(self):
        path = self.paths[self.pathidx]
        filename = os.path.basename(path)
        if filename.split('.')[-1].lower() in ['jpg', 'png']:
            path = self._image_to_pdf(path)
        try:
            self.pdf = pdfplumber.open(path)
            self.total_pages = len(self.pdf.pages)
            self.pageidx = 1
            self.scale = 1.0
            self.rotate = 0
            self._update_page()
            self.master.title("PDFViewer : {}".format(path))
        except (IndexError, IOError, TypeError):
            self._reject()

    def _open_file(self):
        paths = filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf'),
                                                       ('JPG files', '*.jpg'),
                                                       ('PNG files', '*.png'),
                                                       ('all files', '.*')],
                                            initialdir=os.getcwd(),
                                            title="Select files", multiple=True)
        if not paths or paths == '':
            return
        paths = [path for path in paths if os.path.basename(path).split('.')[-1].lower() in ['pdf', 'jpg', 'png']]
        self.paths = self.paths[:self.pathidx + 1] + list(paths) + self.paths[self.pathidx + 1:]
        self.total_pages = len(self.paths)
        self.pathidx += 1
        self._load_file()

    def _open_dir(self):
        dir_name = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Directory Containing Invoices")
        if not dir_name or dir_name == '':
            return
        paths = os.listdir(dir_name)
        paths = [os.path.join(dir_name, path) for path in paths
                 if os.path.basename(path).split('.')[-1].lower() in ['pdf', 'jpg', 'png']]
        self.paths.extend(paths)
        if not self.paths:
            return
        self.total_pages = len(self.paths)
        self.pathidx += 1
        self._load_file()



    def _help(self):
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w, h = 600, 600
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        help_frame = Toplevel(self)
        help_frame.title("Help")
        help_frame.configure(width=w, height=h, bg=BACKGROUND_COLOR, relief=SUNKEN)
        help_frame.geometry('%dx%d+%d+%d' % (w, h, x, y))
        help_frame.minsize(height=h, width=w)
        help_frame.maxsize(height=h, width=w)
        help_frame.rowconfigure(0, weight=1)
        help_frame.columnconfigure(0, weight=1)
        HelpBox(help_frame, width=w, height=h, bg=BACKGROUND_COLOR, relief=SUNKEN).grid(row=0, column=0)
