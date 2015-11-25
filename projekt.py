try: #Python 3
    from tkinter import *
    from tkinter import ttk, font
except ImportError: #Python 2
    from Tkinter import *
    from Tkinter import ttk, font
import ctypes
import time

#hetkel on sisestatud vahemaadeks kindlat arvud, kuid tuleb muuta need ka sültuvaks ekraani suurusest

def akna_suuruse_saamine():
    global ekraani_laius, ekraani_kõrgus
    user32 = ctypes.windll.user32
    ekraani_laius= round(0.7*user32.GetSystemMetrics(0))
    ekraani_kõrgus= round(0.7*user32.GetSystemMetrics(1))
    return str(ekraani_laius) + "x" +str(ekraani_kõrgus)

def näita_aega(sekundid): #näitab aega tundides ja minutites ja sekundites
    tund=0
    minut=0
    sekund=0
    while True:
        if sekundid>=3600:
            tund+=1
            sekundid-=3600
        else:
            break
    while True:
        if sekundid>=60:
            minut+=1
            sekundid-=60
        else:
            break
    sekund+=sekundid
    return str(tund)+" tundi, "+str(minut)+ " minutit, "+str(sekund)+" sekundit."

            
def nulli_kõik():   #vajab täielikku tegemist
    a=1 #lihtsalt, et siin miadgi oleks hetkel :D

stopperi_sekundid=0
def stopperi_tiksumine():
    global stopperi_sekundid, tiksumise_id, stopperi_näidatav_aeg
    stopperi_sekundid+=1
    try:
        stopperi_näidatav_aeg.destroy()
    except:
        pass
    stopperi_näidatav_aeg=ttk.Label(raam, text= näita_aega(stopperi_sekundid))
    stopperi_näidatav_aeg.grid(column=5, row=1, padx=20, pady=5, sticky=(W))
    tiksumise_id=raam.after(1000, stopperi_tiksumine)

def käivita_stopper():
    global stopperi_sekundid, stopperi_käivitamise_nupp, stopperi_peatamise_nupp
    stopperi_käivitamise_nupp.destroy()
    stopperi_peatamise_nupp = Button(raam, text="Peata stopper", command=peata_stopper, width=12, bg=nupu_värv, font=headeri_font)
    stopperi_peatamise_nupp.grid(column=4, row=0, padx=10, pady=5, sticky=(W))
    stopperi_sekundid-=1
    stopperi_tiksumine()

def peata_stopper():
    global stopperi_käivitamise_nupp, stopperi_peatamise_nupp
    stopperi_peatamise_nupp.destroy()
    stopperi_käivitamise_nupp = Button(raam, text="Käivita stopper", command=käivita_stopper, width=12, bg=nupu_värv, font=headeri_font)
    stopperi_käivitamise_nupp.grid(column=4, row=0, padx=10, pady=5, sticky=(W))
    raam.after_cancel(tiksumise_id)

def nulli_stopper():
    global stopperi_sekundid, stopperi_näidatav_aeg
    peata_stopper()
    stopperi_sekundid=0
    stopperi_näidatav_aeg.destroy()
    

    
#siia siis äkki värvid lisada?
tausta_värv= '#%02x%02x%02x' % (242, 242, 242)
nupu_värv= '#%02x%02x%02x' % (192, 204, 208)
headeri_teksti_värv='blue'


raam=Tk()
raam.configure(bg = tausta_värv)
raam.title("Projekt")
raam.geometry(akna_suuruse_saamine())

#pakun välja, et siia võiks kokku kirjutada nt kõik kasutatavad fondid
headeri_font= font.Font(size=10, weight='bold')


#Teen kõige ülemise gridi rea:
töötavate_programmide_header = ttk.Label(raam, text="Töötavate programmide nimekiri ",font=headeri_font, background=tausta_värv, foreground=headeri_teksti_värv)
programmide_aktiivsuse_header = ttk.Label(raam, text="Programmi aktiivsus", font=headeri_font, background=tausta_värv, foreground=headeri_teksti_värv)
aja_header = ttk.Label(raam, text="Kulunud aeg", font=headeri_font, background=tausta_värv, foreground=headeri_teksti_värv)
töötavate_programmide_header.grid(column=0, row=0, padx=30, pady=20, sticky=(W))
programmide_aktiivsuse_header.grid(column=1, row=0, padx=30, pady=20, sticky=(W))
aja_header.grid(column=2, row=0, padx=30, pady=20, sticky=(W))
kõikide_aegade_nullimise_nupp = Button(raam, text="Nulli ajad", command=nulli_kõik, width=10, font=headeri_font, bg=nupu_värv)
kõikide_aegade_nullimise_nupp.grid(column=3, row=0, padx=30, pady=20, sticky=(W))

#teen stopperi:
stopper=ttk.Label(raam, text="Stopper:", font=headeri_font, background=tausta_värv)
stopper.grid(column=4, row=1, padx=20, pady=5,sticky=(W))
stopperi_käivitamise_nupp = Button(raam, text="Käivita stopper", command=käivita_stopper, width=12, bg=nupu_värv, font=headeri_font)
stopperi_käivitamise_nupp.grid(column=4, row=0, padx=20, pady=5, sticky=(W))
stopperi_nullimise_nupp= Button(raam, text="Nulli stopper", command=nulli_stopper, width=12, bg=nupu_värv, font=headeri_font)
stopperi_nullimise_nupp.grid(column=5, row=0, padx=20, pady=5, sticky=(W))




raam.mainloop()