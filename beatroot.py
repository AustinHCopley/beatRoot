import tkinter as tk
from tkinter import messagebox
import threading
from PIL import Image, ImageTk
import serial
import time
import pygame
import statistics
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import client_data


class beatRoot:
    def __init__(self, root, ser):
        self.root = root
        self.root.title("beatRoot")
        self.root.configure(background='#d9d9d9')
        self.ser = ser
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_data.ID,
                                                            client_secret=client_data.SECRET,
                                                            redirect_uri=client_data.URI,
                                                            scope='user-read-playback-state,user-modify-playback-state'))

        # creating ui elements
        self.logo = ImageTk.PhotoImage(Image.open("./beatroot.png").resize((586, 511)))
        self.logo_label = tk.Label(root, image=self.logo)

        self.manual_heart = tk.BooleanVar()
        self.heart_check = tk.Checkbutton(root, text="Enter Heartrate", command=self.enable_manual_in, variable=self.manual_heart)
        self.heart_entry = tk.Entry(root, state=tk.DISABLED)
        self.sensor_label = tk.Label(text="Sensor: ")
        self.heartrate_monitor = tk.Label(text="")

        self.song_label = tk.Label(root, text="Enter Song:")
        self.song_entry = tk.Entry(root)

        self.theme_label = tk.Label(root, text="Enter Theme:")
        self.theme_entry = tk.Entry(root)

        self.genre_label = tk.Label(root, text="Enter Genre (Optional):")
        self.genre_entry = tk.Entry(root)

        self.generate_button = tk.Button(root, text="Generate Playlist", background="grey", foreground="#1DD05D", command=self.generate_playlist)

        self.result_label = tk.Label(root, text="")

        # media control
        self.play_img = ImageTk.PhotoImage(Image.open("./play.png").resize((100,114)))
        self.skip_img = ImageTk.PhotoImage(Image.open("./skip.png").resize((162,114)))
        self.rewind_img = ImageTk.PhotoImage(Image.open("./rewind.png").resize((162,114)))
        self.play_button = tk.Button(root, image=self.play_img, command=self.play_song)
        self.skip_button = tk.Button(root, image=self.skip_img, command=self.skip_song)
        self.rewind_button = tk.Button(root, image=self.rewind_img, command=self.rewind_song)

        # grid display
        self.logo_label.grid(row=0, column=2, columnspan=2, padx=5, pady=25)
        self.sensor_label.grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.heartrate_monitor.grid(row=1, column=3, padx=5, pady=5)
        self.heart_check.grid(row=2, column=2, padx=5, pady=5, sticky='e')
        self.heart_entry.grid(row=2, column=3, padx=5, pady=5)
        self.song_label.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.song_entry.grid(row=3, column=3, padx=5, pady=5)
        self.theme_label.grid(row=4, column=2, padx=5, pady=5, sticky="e")
        self.theme_entry.grid(row=4, column=3, padx=5, pady=5)
        self.genre_label.grid(row=5, column=2, padx=5, pady=5, sticky="e")
        self.genre_entry.grid(row=5, column=3, padx=5, pady=5)
        self.generate_button.grid(row=6, column=2, columnspan=2, pady=10)
        self.result_label.grid(row=7, column=2, columnspan=2, pady=10)
        self.rewind_button.grid(row=8, column=0, padx=5, pady=5, sticky='e')
        self.play_button.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky='s')
        self.skip_button.grid(row=8, column=4, padx=5, pady=5, sticky='w')

        self.heartrate = 0
        self.history = []
        self.playlist = []
        self.ptr = 0
        self.themes = ["exercise", "intense focus", "study", "meditation"]
        # define acceptable ranges of bpm for each theme
        self.medi = [40, 80]
        self.study = [60, 100]
        self.focus = [90, 110]
        self.exerc = [100, 165]

        self.sensor_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.sensor_thread.start()

    def enable_manual_in(self):
        if self.manual_heart.get():
            self.heart_entry.config(state=tk.NORMAL)
        else:
            self.heart_entry.config(state=tk.DISABLED)

    def update_heartrate_text(self):
        self.heartrate_monitor.config(text=str(self.heartrate))

    def read_serial(self):
        while True:
            try:
                data = self.ser.readline().decode().strip()
                if data:
                    data = float(data)
                    self.history.append(data)
                    if self.check_hist(data):
                        self.heartrate = data
                        self.root.after(100, self.update_heartrate_text)
                        print(self.heartrate)

            except UnicodeDecodeError as e:
                print(f"Error decoding data: {e}")

            time.sleep(1)

    def check_hist(self, data):
        if len(self.history) >= 5:
            moving_average = statistics.mean(self.history[-5:])
            lower_thresh = max(40, moving_average - 2 * statistics.stdev(self.history))
            upper_thresh = min(180, moving_average + 2 * statistics.stdev(self.history))
        else:
            moving_average = 0
            lower_thresh = 40
            upper_thresh = 180
        self.history = self.history[-15:] if len(self.history) > 15 else self.history 
        return lower_thresh < data < upper_thresh

    def set_playlist(self, song, genre, theme):

        # TODO playlist logic
        if theme.lower() == "exercise":
            song = "exercise"
        elif theme.lower() == "intense focus":
            song = "focus"
        elif theme.lower() == "study":
            song = "study"
        elif theme.lower() == "meditation":
            song = "meditation"
        else:
            messagebox.showerror("Invalid Theme", "choose from: exercise, intense focus, study, meditation")
            return

        # self.playlist = [f"{song} song 1", f"{song} song 2", f"{song} song 3"]
        self.playlist = ["Doomsday - MF DOOM", "Outlier - Snarky Puppy"]
        self.ptr = 0

    def generate_playlist(self):
        song = self.song_entry.get()
        theme = self.theme_entry.get()
        genre = self.genre_entry.get()
        if self.manual_heart.get():
            bpm = int(self.heart_entry.get())
        else:
            bpm = self.heartrate
            print("from sensor")
        print(bpm)

        if not song or not theme:
            messagebox.showerror("Invalid Input", "Please fill in song and theme")
            return
        if not genre:
            genre = ""

        self.set_playlist(song, genre, theme)
        self.result_label.config(text="Playlist:\n" + "\n".join(self.playlist))

    def play_song(self):
        if self.playlist:
            track_uri = self.sp.search(q=self.playlist[self.ptr], type='track')['tracks']['items'][0]['uri']
            self.sp.start_playback(uris=[track_uri])

    def skip_song(self):
        print("skip")
        if self.playlist:
            self.ptr += 1
            self.ptr %= len(self.playlist)
            if self.ptr < len(self.playlist):
                track_uri = self.sp.search(q=self.playlist[self.ptr], type='track')['tracks']['items'][0]['uri']
                self.sp.start_playback(uris=[track_uri])

    def rewind_song(self):
        print("rewind")
        self.sp.previous_track()


if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=0.1)
    pygame.mixer.init()
    root = tk.Tk()
    beat = beatRoot(root, ser)
    root.mainloop()
