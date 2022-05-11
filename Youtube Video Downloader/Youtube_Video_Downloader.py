import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog as dir
import tkinter.font as font
from tkinter import ttk
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from subprocess import call
import os




class MainWindow(tk.Tk):

    def __init__(self):

        super().__init__()

        self.wm_geometry("500x500")

        self.wm_resizable(False,False)

        self.wm_title("Youtube Video Downloader")

        #self.wm_iconbitmap("example.ico")

        #self.example = tk.PhotoImage(file="example.png")                  Any picture that you want can be set to beutify the window
        #self.label = tk.Label(self,image=self.example)
        #self.label.place_configure(x=0,y=0,relheight=1,relwidth=1)

        self.connect_button = tk.Button(
        self,
        text = "Connect",
        command=self.new_window,
        borderwidth=4,
        bg="black",
        fg="white",
        #font=("Courier",10,"bold","italic"),                              Any font that you want can be set to beutify the writing
        height=1,
        width=12,
        state="normal",
        activebackground="black",
        activeforeground="white"
        )

        self.connect_button.place_configure(x=198,y=430)

    def new_window(self):

        self.connect_button["text"] = "Connecting"

        self.connect_button.flash()

        result = call(["ping","www.youtube.com"],shell=True)

        if result == 0:

            downloading_window = DownloadingWindow(self)

            downloading_window.start_downloading_window()

        else:

            messagebox.showerror("Connection Problem","Please try again")

            self.connect_button.configure(text="Connect",state="normal")


class DownloadingWindow(tk.Toplevel):

    def __init__(self,master_window:tk.Tk):

        super().__init__(master_window)

        self.master_window = master_window

        self.wm_geometry("500x500")

        self.wm_resizable(False,False)

        self.wm_title("Download")

        self.wm_protocol("WM_DELETE_WINDOW",self.master_window.destroy)

        self.master_window.wm_withdraw()

        self.combobox_style = ttk.Style(self)

        self.combobox_style.theme_create(
        "combostyle",
        parent="alt",
        settings = {"TCombobox":
        {"configure":
        {"selectbackground": "black",
        "fieldbackground": "black",
        "background": "white"
        }}}
        )

        self.combobox_style.theme_use("combostyle")

        self.progressbar_style = ttk.Style(self)

        self.progressbar_style.configure("red.Horizontal.TProgressbar", foreground="black", background="black",troughcolor="red4")

        self.mp4 = tk.IntVar()

        self.mp3 = tk.IntVar()

        self.url = tk.StringVar()

        self.location_of_folder = tk.StringVar()

        self.resolution = tk.StringVar()

        #self.start_downloading_window()       You can also do it like this way if you remove the code on line 61.It does not matter,both are true and both work same

    def __create_resolution_combobox(self):

        resolution_list = ("360p","480p","720p")

        self.resolution_menu = ttk.Combobox(
        self,
        textvariable=self.resolution,
        values=resolution_list,
        state="readonly",
        foreground="white",
        font=("Courier",10,"bold","italic")
        )

        self.resolution_menu.current(2)

        self.resolution_menu.place_configure(x=153,y=155)

    def __create_mp4_checkbutton(self):

        self.mp4_checkbutton = tk.Checkbutton(
        self,
        text="mp4",
        bg="black",
        activebackground="black",
        fg="white",
        activeforeground="white",
        selectcolor="black",
        variable=self.mp4,
        onvalue=1,
        offvalue=0,
        command=self.__mp3_mp4,
        #font=("Courier",10,"bold","italic")
        )

        self.mp4_checkbutton.place_configure(x=37,y=152)

    def __create_mp3_checkbutton(self):

        self.mp3_checkbutton = tk.Checkbutton(
        self,
        text="mp3",
        bg="black",
        activebackground="black",
        fg="white",
        activeforeground="white",
        variable=self.mp3,
        onvalue=1,
        offvalue=0,
        command=self.__mp3_mp4,
        #font=("Courier",10,"bold","italic"),
        selectcolor="black"
        )

        self.mp3_checkbutton.place_configure(x=95,y=152)

    def __create_link_input_entry(self):

        def placeholder(event):

            self.url_entry["state"] = "normal"

            self.url_entry.delete(0,"end")

            self.url_entry.unbind("<Button-1>",id)

        self.url_entry = tk.Entry(
        self,
        justify="left",
        background="black",
        disabledbackground="black",
        borderwidth=5,
        selectforeground="black",
        selectbackground="white",
        textvariable=self.url,
        insertbackground="red",
        fg="white",
        width=66,
        #font=("Courier",10,"bold","italic")
        )

        self.url_entry.place_configure(x=35,y=120)

        self.url_entry.insert(0,"Enter Youtube video url:")

        self.url_entry.configure(state="disabled",disabledforeground="white")

        id = self.url_entry.bind("<Button-1>",placeholder)

    def __create_location_of_folder_entry(self):

        self.location_entry = tk.Entry(
        self,
        justify="left",
        readonlybackground="black",
        fg="white",
        borderwidth=5,
        selectforeground="black",
        textvariable=self.location_of_folder,
        selectbackground="white",
        width=42,
        #font=("Courier",10,"bold","italic")
        )

        self.location_entry.place_configure(x=35,y=265)

        self.location_entry.insert(0,"Location of folder:")

        self.location_entry["state"] = "readonly"

    def __create_browse_button(self):

        self.browse_button = tk.Button(
        self,
        text="Browse",
        command=self.__after_click_on_browse_button,
        borderwidth=4,
        bg="black",
        fg="white",
        #font=("Courier",10,"bold","italic"),
        state="normal",
        activebackground="black",
        activeforeground="white"
        )

        self.browse_button.place_configure(x=313,y=265,height=30)

    def __after_click_on_browse_button(self):

        folder = dir.askdirectory(title="Folder Of MP4-MP3 Files Which To Be Downloaded")

        self.location_of_folder.set(folder)

    def __create_download_button(self):

        self.download_button = tk.Button(
        self,
        text = "Download",
        command=self.__download,
        borderwidth=4,
        bg="black",
        fg="white",
        #font=("Courier",10,"bold","italic"),
        height=1,
        width=12,
        state="normal",
        activebackground="black",
        activeforeground="white",
        disabledforeground="white"
        )

        self.download_button.place_configure(x=198,y=430)

    def start_downloading_window(self):

        self.__create_resolution_combobox()

        self.__create_mp4_checkbutton()

        self.__create_mp3_checkbutton()

        self.__create_link_input_entry()

        self.__create_location_of_folder_entry()

        self.__create_browse_button()

        self.__create_download_button()

    def __mp3_mp4(self):

        if self.mp3.get() == 1 and self.mp4.get() == 1:

            self.resolution_menu.configure(show="",state="readonly")

            return 0

        elif self.mp3.get() == 1 and self.mp4.get() == 0:

            self.resolution_menu.configure(show=" ",state="disabled")

            return 1

        elif self.mp3.get() == 0 and self.mp4.get() == 1:

            self.resolution_menu.configure(show="",state="readonly")

            return 2

        else:

            return 3

    def mp4_to_mp3(self,mp4_file:str,mp3_file:str):

        video = VideoFileClip(mp4_file)

        mp4_audio = video.audio

        mp4_audio.write_audiofile(mp3_file)

        video.close()

        mp4_audio.close()

    def __eliminate_wrong_character(self,path_of_downloaded_file):   #This is for not getting error because of the character while downloading

        eliminate_character = r"\n"

        eliminate_character = eliminate_character.strip("n")

        without_wrong_character = path_of_downloaded_file.split(eliminate_character)

        without_wrong_character.reverse()

        without_wrong_character_list = without_wrong_character[0].split(".")

        without_wrong_character_list.pop()

        path_of_downloaded_file_without_wrong_character = "".join(without_wrong_character_list)

        return path_of_downloaded_file_without_wrong_character   

    def __download(self):

        def progress_bar_percent(stream,chunk,bytes_remaining):

            size_of_file = streams.filesize

            downloaded_byte = size_of_file - bytes_remaining

            percent = int(downloaded_byte / size_of_file * 100)

            pb["value"] = percent

            self.update()

        pb = ttk.Progressbar(self,orient="horizontal", length=285, mode="determinate",style="red.Horizontal.TProgressbar")

        mini_info_window = True

        self.download_button.configure(text="Downloading",state="disabled")

        mp3_mp4_control = self.__mp3_mp4()

        try:

            yt = YouTube(self.url.get(),progress_bar_percent)

        except:

            messagebox.showerror("Connection Error","Try again")

            self.download_button.configure(text="Download",state="normal")

        else:

            stream_filter = yt.streams.filter(progressive=True,file_extension="mp4")

            streams = stream_filter.get_by_resolution(self.resolution.get())

            if mp3_mp4_control == 1 and streams == None:

                mp3_download_resolution_problem = ("720p","480p","360p")

                index = 0

                while streams == None:

                    if streams == None and index == len(mp3_download_resolution_problem):

                        messagebox.showerror("MP3 Download Error","MP3 file cannot be downloaded")

                        break

                    streams = stream_filter.get_by_resolution(self.resolution.set(mp3_download_resolution_problem[index]))

                    index += 1

            if streams == None:

                messagebox.showerror("Downloading Error","There is no video that has audio-video combination tracks at this resolution")

                self.download_button.configure(text="Download",state="normal")

            else:

                if (mp3_mp4_control == 0) and (self.location_of_folder.get().upper().startswith("C") or self.location_of_folder.get().upper().startswith("D") or self.location_of_folder.get().startswith("/")) == True:

                    messagebox.showinfo("Downloading",f"Downloading {yt.title} mp4 and mp3 files...\nLocation to install:{self.location_of_folder.get()}")

                    pb.place_configure(x=106,y=382)

                    path = streams.download(self.location_of_folder.get())

                    pb.destroy()

                    path_without_error = self.__eliminate_wrong_character(path)

                    mp4_file = f"{self.location_of_folder.get()}/" + f"{path_without_error}.mp4"

                    mp3_file = f"{self.location_of_folder.get()}/" + f"{path_without_error}.mp3"

                    self.download_button.configure(text="Download",state="normal")

                    self.mp4_to_mp3(mp4_file,mp3_file)

                elif (mp3_mp4_control == 1) and (self.location_of_folder.get().upper().startswith("C") or self.location_of_folder.get().upper().startswith("D") or self.location_of_folder.get().startswith("/")) == True:

                    messagebox.showinfo("Downloading",f"Downloading {yt.title} mp3 file...\nLocation to install:{self.location_of_folder.get()}")

                    pb.place_configure(x=106,y=382)

                    path = streams.download(self.location_of_folder.get())

                    pb.destroy()

                    path_without_error = self.__eliminate_wrong_character(path)

                    mp4_file = f"{self.location_of_folder.get()}/" + f"{path_without_error}.mp4"

                    mp3_file = f"{self.location_of_folder.get()}/" + f"{path_without_error}.mp3"

                    self.download_button.configure(text="Download",state="normal")

                    self.mp4_to_mp3(mp4_file,mp3_file)

                    os.remove(mp4_file)

                elif (mp3_mp4_control == 2) and (self.location_of_folder.get().upper().startswith("C") or self.location_of_folder.get().upper().startswith("D") or self.location_of_folder.get().startswith("/")) == True:

                    messagebox.showinfo("Downloading",f"Downloading {yt.title} mp4 file...\nLocation to install:{self.location_of_folder.get()}")

                    pb.place_configure(x=106,y=382)

                    streams.download(self.location_of_folder.get())

                    pb.destroy()

                    self.download_button.configure(text="Download",state="normal")

                else:

                    messagebox.showwarning("Warning","Please select one of mp3 or mp4 types or select both if you dont select any of mp3 or mp4 types\nMake sure the path of the folder is correct")

                    self.download_button.configure(text="Download",state="normal")

                    mini_info_window = False

                if mp3_mp4_control < 3 and mini_info_window == True:

                    show = messagebox.askyesno(message="Do you want to see video's information?")

                    if show == True:

                        messagebox.showinfo("Video Info",f"Title: {yt.title}\nDescription: {yt.description}\nDuration: {yt.length} seconds\nPublished Date: {yt.publish_date}")


main_window = MainWindow()

main_window.mainloop()
