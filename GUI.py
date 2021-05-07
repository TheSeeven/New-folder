from multiprocessing.spawn import freeze_support

import tkinter
import PIL
from PIL import ImageTk
from tkinter import *


class Interface:
    def __init__(self):
        self.interface = tkinter.Tk()
        self.interface.title("ProBenchBurner - Idle")
        self.interface.configure(background="black")
        self.interface.resizable(False, False)

        self.pictureReady = ImageTk.PhotoImage(PIL.Image.open("cpu_ready.png"))
        self.pictureBusy = ImageTk.PhotoImage(PIL.Image.open("cpu_busy.png"))

        self.icon_ready = tkinter.PhotoImage(r"cpu_icon_ready.ico")
        self.icon_busy = tkinter.PhotoImage(r"cpu_icon_busy.ico")

        self.canvas = Label(
            self.interface, image=self.pictureReady, padx=7, pady=5, background="black"
        )

        self.label_result = Label(
            self.interface,
            text="Test results:",
            padx=7,
            pady=5,
            background="black",
            foreground="#28cbfc",
            font="Helvetica 13 bold",
        )

        label_repetition = tkinter.Label(
            self.interface,
            text="How many times the test should be repeated",
            background="black",
            foreground="#28cbfc",
            font="Helvetica 13 bold",
        )
        label_dificulty = tkinter.Label(
            self.interface,
            text="Dificulty of the test",
            background="black",
            foreground="#28cbfc",
            font="Helvetica 13 bold",
        )
        label_size = tkinter.Label(
            self.interface,
            text="Sets the size of the problem (It will use more ram at greater values!)",
            background="black",
            foreground="#28cbfc",
            font="Helvetica 13 bold",
        )
        label_cores = tkinter.Label(
            self.interface,
            text="Number of threads for solving (Warning, high value might make the computer hang!)",
            background="black",
            foreground="#28cbfc",
            font="Helvetica 13 bold",
        )

        label_repetition.grid(row=0, column=0, sticky="nsew", padx=7, pady=5)
        label_dificulty.grid(row=2, column=0, sticky="nsew", padx=7, pady=5)
        label_size.grid(row=4, column=0, sticky="nsew", padx=7, pady=5)
        label_cores.grid(row=6, column=0, sticky="nsew", padx=7, pady=5)

        self.spinbox_repetition = tkinter.Spinbox(
            self.interface,
            from_=0,
            to=100,
            font="Helvetica 13 bold",
            background="#303030",
            foreground="white",
        )
        self.spinbox_dificulty = tkinter.Spinbox(
            self.interface,
            from_=0,
            to=200000,
            font="Helvetica 13 bold",
            background="#303030",
            foreground="white",
        )
        self.spinbox_size = tkinter.Spinbox(
            self.interface,
            from_=0,
            to=20000,
            font="Helvetica 13 bold",
            background="#303030",
            foreground="#f5b5b5",
        )
        self.spinbox_cores = tkinter.Spinbox(
            self.interface,
            from_=0,
            to=128,
            font="Helvetica 13 bold",
            background="#303030",
            foreground="#f5b5b5",
        )

        self.spinbox_repetition.grid(row=1, column=0, sticky="nsew", padx=7, pady=5)
        self.spinbox_dificulty.grid(row=3, column=0, sticky="nsew", padx=7, pady=5)
        self.spinbox_size.grid(row=5, column=0, sticky="nsew", padx=7, pady=5)
        self.spinbox_cores.grid(row=7, column=0, sticky="nsew", padx=7, pady=5)

        self.label_result.grid(row=8, column=0, sticky="nsew", padx=7, pady=5)
        self.canvas.grid(row=9, column=0, sticky="nsew", padx=7, pady=5)

        self.button_start = None

        Grid.columnconfigure(self.interface, 0, weight=1)
        for i in range(0, 10):
            Grid.rowconfigure(self.interface, i, weight=1)

    def set_button(self, command):
        self.button_start = tkinter.Button(
            text="Start Benchmark",
            command=command,
            font="Helvetica 13 bold",
            background="#1f7839",
            foreground="#fcfffd",
        )
        self.button_start.grid(row=10, column=0, sticky="nsew", padx=7, pady=5)
