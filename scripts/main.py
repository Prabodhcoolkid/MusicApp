from tkinter import *
from tkinter import filedialog, messagebox, ttk
from typing import Optional
import threading
import download
import os
import subprocess

class GUI():
    def __init__(self):
        
        ''' Main window '''
        self.window = Tk()
        self.window.title('youtube mp3 downloader')
        self.window.geometry('700x200')
        
        ''' Link input line '''
        self.url_label = Label(self.window, text='Video link(ctrl+v): ',font=(None, 12))
        self.url_label.place(x=40, y=60)
        self.url_entry = Entry(self.window, width=50)
        self.url_entry.place(x=210, y=61)
        
        ''' Path line '''
        self.folder_path = StringVar()
        self.path_label = Label(self.window, text='Save mp3 to: ',font=(None, 12))
        self.path_label.place(x=40, y=90)
        self.path_entry = Entry(self.window, width=50, textvariable=self.folder_path)
        self.path_entry.place(x=210, y=91)
        
        '''Search button'''
        # search a song 
        self.search_label = Label(self.window, text='Search song: ', font=(None, 12))
        self.search_label.place(x=40, y=30)
        self.search_entry = Entry(self.window, width=50)
        self.search_entry.place(x=210, y=31)
        self.search_button = Button(self.window, text='Search', command=self.searched)
        self.search_button.place(x=580, y=25)

        '''Browse button'''
        self.brws_button = Button(self.window, text='Browse', command=self.browse_button)
        self.brws_button.place(x=580, y=85)

        
        self.progress = ttk.Progressbar(self.window, orient = HORIZONTAL)
        self.progress.pack(side=BOTTOM, fill=X)
        
        self.window.mainloop()
        
    def browse_button(self):
        self.folder_path
        self.filename = filedialog.askdirectory()
        self.folder_path.set(self.filename)

    def pressed(self):
        self.progress.start()
        def callback():
            self.url = self.url_entry.get()
            self.dir = str(self.path_entry.get())

            if self.url != None and (self.url.startswith('http') or self.url.startswith('www')):
                
                try:
                    self.down_button['state'] = 'disabled'
                    self.download(self.url, self.dir)
                    self.progress.stop()
                    messagebox.showinfo(title='Success', message='Download complete!')
                    self.down_button['state'] = 'normal'
                except Exception as e:
                    self.progress.stop()
                    messagebox.showerror(title='Server Error', message='\n    please try again    \n')
            else: 
                self.progress.stop()
                messagebox.showerror(title='Error', message='Bad url')

        self.t = threading.Thread(target=callback)
        self.t.start()
    
    def searched(self):
        # get youtube song url based off some keywords -> some API or ai algo, or selenium webdriver
        pass



user_input = input("Add(A) or Download(D):")
if user_input == 'A':
    GUI()
elif user_input == 'D':
    download.download_song_with_y2meta(download.get_links(), path=os.environ.get("DOWNLOAD_FOLDER"))  
    
else:
    pass