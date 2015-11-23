from tkinter import *
from tkinter import ttk
import ctypes

def akna_suuruse_saamine():
    global ekraani_laius, ekraani_kõrgus
    user32 = ctypes.windll.user32
    ekraani_laius= round(0.7*user32.GetSystemMetrics(0))
    ekraani_kõrgus= round(0.7*user32.GetSystemMetrics(1))
    return str(ekraani_laius) + "x" +str(ekraani_kõrgus)




raam=Tk()
raam.title("Projekt")
raam.geometry(akna_suuruse_saamine())

