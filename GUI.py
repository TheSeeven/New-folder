
from multiprocessing.spawn import freeze_support
import tkinter
import PIL
from PIL import ImageTk
from tkinter import *


class Interface:

    def __init__(self):
        self.interface = tkinter.Tk()
        self.pictureReady = ImageTk.PhotoImage(PIL.Image.open("cpu_ready.png"))
        self.pictureBusy = ImageTk.PhotoImage(PIL.Image.open("cpu_busy.png"))
        self.canvas = Label(self.interface, image=self.pictureReady)
        self.results = Label(self.interface, text="", foreground="green")
        self.label_result = Label(self.interface, text="Test results:")
        self.label_result.pack()
        self.results.pack()

        self.interface.minsize(width=500, height=900)
        self.interface.maxsize(width=500, height=900)

        label_repetition = tkinter.Label(
            self.interface, text="How many times the test should be repeated")
        label_dificulty = tkinter.Label(
            self.interface, text="Dificulty of the test")
        label_size = tkinter.Label(
            self.interface, text="Sets the size of the problem (It will use more ram at greater values!)")
        label_cores = tkinter.Label(
            self.interface, text="Number of threads for solving (Warning, high value might make the computer hang!)")

        self.spinbox_repetition = tkinter.Spinbox(
            self.interface, from_=0, to=100)
        self.spinbox_dificulty = tkinter.Spinbox(
            self.interface, from_=0, to=200000)
        self.spinbox_size = tkinter.Spinbox(self.interface, from_=0, to=20000)
        self.spinbox_cores = tkinter.Spinbox(self.interface, from_=0, to=128)

        label_repetition.pack()
        self.spinbox_repetition.pack()

        label_dificulty.pack()
        self.spinbox_dificulty.pack()

        label_size.pack()
        self.spinbox_size.pack()

        label_cores.pack()
        self.spinbox_cores.pack()

        self.button_start = None

        self.canvas.pack()

    def set_button(self, command):
        self.button_start = tkinter.Button(
            text="Start Benchmark", command=command)
        self.button_start.pack()
