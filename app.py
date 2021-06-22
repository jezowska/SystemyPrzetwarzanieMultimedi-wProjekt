import sounddevice as sd
import soundfile as sf
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from os import path


class Functions:
    def __init__(self,
                 BREAK=10,
                 DURATION=30,
                 filetypes=(
                     ("wav files", "*.wav"),
                     ("All files", "*"),
                 ),
                 default_samplerate=44100,
                 ):
        self.BREAK = BREAK
        self.DURATION = DURATION
        self.filetypes = filetypes
        self.track_data = np.empty((0, 2))  # tworzenie tablicy o wymiarach 0x2,
                                            # empty tworzy niewyzerowaną tablicę.
                                            # wymiary są 0x2 aby złączyć później dwie różne tablice ze sobą
        self.track_samplerate = default_samplerate
        self.current_track = ""  # ścieżka do wybranego pliku wav, który będzie odtwarzany

    def play_track(self): # za pomocą biblioteki sounddevice odtwarzamy dany plik,
                          # jako argumenty podajemy ścieżkę pliku i ile próbek w ciągu sekundy ma otworzyć
        sd.play(
            self.track_data,
            self.track_samplerate,
        )

    def stop(self):  # funkcja zatrzymująca odtwarzanie
        sd.stop()

    def open_file(self,
                  title="Select file",
                  ):
        # askopenfilename odpowiada za wyświetlanie okienka wyboru pliku
        self.current_track = fd.askopenfilename(
            title=title, # co się wyświelki na okienki
            filetypes=self.filetypes, # jaki typ pliku można wybrać
        )

        # ta funkcja wczytuje do tablicy plik dźwiękowy, always_2d odpowiada za dźwięk stereo
        self.track_data, self.track_samplerate = sf.read(
            self.current_track,
            always_2d=True,
        )

    # sytuacja taka jak w funkcji open_file
    def open_files(self,
                   title="Select files"):
        self.filenames = fd.askopenfilenames(
            title=title,
            filetypes=self.filetypes,
        )

    def combine_files(self,
                      output_name="combined",
                      output_extension=".wav",
                      ):
        output = np.empty((0, 2)) # szkielet tablicy wyjściowej

        for i, f in enumerate(self.filenames): # iterowanie po wczytanych plikach
            data, samplerate = sf.read(
                f,
                always_2d=True,
            )

            timerate = min(
                samplerate*self.DURATION,
                len(data),
            ) # sprawdzamy czy nasz plik jest którszy niż DURATION i wybieramy którszą wartość

            output = np.concatenate((
                output,
                data[:timerate],
            )) # do tablicy output dodajemy kolejny 30 sekundowy fragment

            if i < len(self.filenames) - 1: # sprawdzamy czy to ostatni fragment, który ma być dodany
                output = np.concatenate((
                    output,
                    np.zeros((
                        self.BREAK*samplerate,
                        2,
                    ))
                ))
            ext = path.splitext(output_name)[1] # dobranie odpowiedniego rozszerzenia

            if ext == "":
                output_name += output_extension

            sf.write(
                output_name,
                output,
                samplerate,
            ) # zapisanie pliku wynikowego


class App:
    def __init__(self,
                 title="Tkinter app",
                 resizable=(False, False),
                 geometry="",
                 ):
        # stworzenie okna o danych parametrach
        self.window = tk.Tk()
        self.window.title(title)
        self.window.resizable(*resizable)
        if geometry != "":
            self.window.geometry(geometry)

    def add_button(self,
                   text: str,
                   command,
                   ):
        temp_button = tk.Button(
            self.window,
            text=text,
            command=command,
        ) # dodanie przycisku o danych parametrach do okna
        temp_button.pack()

    # wyświetlanie aplikacji
    def mainloop(self):
        self.window.mainloop()
