try: #Python 3
    from tkinter import *
    from tkinter import ttk, font
    from tkinter import messagebox
except ImportError: #Python 2
    from Tkinter import *
    from Tkinter import ttk, font
    from Tkinter import messagebox
import ctypes

import backend # janar's work imported

katselist=["mamma", "sai", "tuba", "nuga", "laut", "liha", "tuum"]
katse_olemasolev=["janar", "juusu", "jannu", "jussu"]                        #ajutised asjad

töötavad_taimerid=[]

user32 = ctypes.windll.user32
ekraani_laius= round(0.7*user32.GetSystemMetrics(0))
ekraani_kõrgus= round(0.7*user32.GetSystemMetrics(1))

def nulli_kõik():   #vajab täielikku tegemist
    a=1 #lihtsalt, et siin miadgi oleks hetkel :D

stopperi_sekundid=0
stopperi_minutid=0
stopperi_tunnid=0

def stopperi_tiksumine():
    global stopperi_sekundid, stopperi_näidatav_aeg, tiksumise_id, stopperi_minutid, stopperi_tunnid
    stopperi_sekundid+=1
    try:
        stopperi_näidatav_aeg.destroy()
    except:
        pass

    if stopperi_sekundid==60:
        stopperi_minutid+=1
        if stopperi_minutid==60:
            stopperi_tunnid+=1
            stopperi_minutid=0
        stopperi_sekundid=0
        
    stopperi_näidatav_aeg=ttk.Label(raam, text= str(stopperi_tunnid)+" tundi, "+str(stopperi_minutid)+ " minutit, "+str(stopperi_sekundid)+" sekundit.", background=tausta_värv)
    stopperi_näidatav_aeg.grid(column=5, row=1, pady=5, sticky=(W), padx=15, columnspan=2)
    tiksumise_id=raam.after(1000, stopperi_tiksumine)

def käivita_stopper():
    global stopperi_sekundid, stopperi_käivitamise_nupp, stopperi_peatamise_nupp
    stopperi_käivitamise_nupp.destroy()
    stopperi_peatamise_nupp = Button(raam, text="Peata stopper", command=peata_stopper, width=12, bg=nupu_värv, font=headeri_font)
    stopperi_peatamise_nupp.grid(column=4, row=0, ipadx=ekraani_laius*0.1*0.7-70, pady=5, padx=15, sticky=(W))
    stopperi_sekundid-=1
    stopperi_tiksumine()

def peata_stopper():
    global stopperi_käivitamise_nupp, stopperi_peatamise_nupp
    try:
        stopperi_peatamise_nupp.destroy()
    except:
        pass
    stopperi_käivitamise_nupp = Button(raam, text="Käivita stopper", command=käivita_stopper, width=12, bg=nupu_värv, font=headeri_font)
    stopperi_käivitamise_nupp.grid(column=4, row=0, ipadx=ekraani_laius*0.1*0.7-70, pady=5, padx=15, sticky=(W))
    raam.after_cancel(tiksumise_id)

def nulli_stopper():
    global stopperi_sekundid, stopperi_minutid, stopperi_sekundid, stopperi_näidatav_aeg
    peata_stopper()
    stopperi_sekundid=0
    stopperi_minutid=0
    stopperi_tunnid=0
    stopperi_näidatav_aeg.destroy()

def käivita_taimer():
    global lisaaken, tundide_sisestus_taimerisse, minutite_sisestus_taimerisse, sekundite_sisestus_taimerisse, teadaanne
    lisaaken=Tk()
    lisaaken.bind_all("<Return>", lisa_taimer)
    lisaaken.title("Taimeri loomine")
    lisaaken.geometry('%dx%d+%d+%d' % (300, 200, 0.45*ekraani_laius, 0.45*ekraani_kõrgus))  #määran asukoha andmetega
    taimeri_header = ttk.Label(lisaaken, text="Sisestage aeg, pärast mida te soovite meeldetuletust:")
    taimeri_header.grid(row=0, column=0, columnspan=7, padx=5, pady=10)
    tundide_sisestus_taimerisse = ttk.Entry(lisaaken, width=3)
    tundide_sisestus_taimerisse.grid(row=1, column=0, padx=5, pady=5, sticky=(W))
    tundide_tekst = ttk.Label(lisaaken, text="tundi,")
    tundide_tekst.grid(row=1, column=1, padx=0, pady=5, sticky=(W,E))
    minutite_sisestus_taimerisse = ttk.Entry(lisaaken, width=3)
    minutite_sisestus_taimerisse.grid(row=1, column=2, padx=5, pady=10, sticky=(W))
    minutite_tekst = ttk.Label(lisaaken, text="minutit,")
    minutite_tekst.grid(row=1, column=3, padx=0, pady=5, sticky=(W,E))
    sekundite_sisestus_taimerisse = ttk.Entry(lisaaken, width=3)
    sekundite_sisestus_taimerisse.grid(row=1, column=4, padx=5, pady=10, sticky=(W))
    sekundite_tekst = ttk.Label(lisaaken, text="sekundit")
    sekundite_tekst.grid(row=1, column=5, padx=0, pady=5, sticky=(W,E))
    teksti_küsimine = ttk.Label(lisaaken, text="Sisestage meeldetuletuse sõnum: ")
    teksti_küsimine.grid(row=3, column=0, columnspan=7, padx=5, pady=5)
    teadaanne = ttk.Entry(lisaaken, width=40)
    teadaanne.grid(row=4, column=0, columnspan=7, padx=5, pady=5)
    taimeri_lisamise_nupp = Button(lisaaken, text="Lisa taimer", command=lisa_taimer, width=12)
    taimeri_lisamise_nupp.grid(column=2, columnspan=3, row=5, padx=5, pady=5, sticky=(W))

def lisa_taimer(event=0):
    global lisaaken, tundide_sisestus_taimerisse, minutite_sisestus_taimerisse, sekundite_sisestus_taimerisse, teadaanne
    global töötavad_taimerid
    try:          #kui midagi ei sisestata, siis pannakse sinna lünka 0
        tund=int(tundide_sisestus_taimerisse.get())
    except:
        tund=0
    try:
        minut=int(minutite_sisestus_taimerisse.get())
    except:
        minut=0
    try:
        sekund=int(sekundite_sisestus_taimerisse.get())
    except:
        sekund=0
    if minut==0 and tund==0 and sekund==0:
        messagebox.showerror(message="Sisestaga kuhugi mõni täisarv!", title="Error")
        lisaaken.attributes("-topmost", True)
    elif sekund>=60:
        messagebox.showerror(message="Sekundite arv ei ole sobiv!", title="Error")
        lisaaken.attributes("-topmost", True) #selleks, et veateate korral jääks lisaaken raami ette
        lisaaken.attributes("-topmost", False)#selleks, et lisaaken ei jääks nt browseri ette kui sa poole pealt browseri avad
    elif minut>=60:
        messagebox.showerror(message="Minutite arv ei ole sobiv!", title="Error")
        lisaaken.attributes("-topmost", True)
        lisaaken.attributes("-topmost", False)
    elif type(sekund)==int and type(minut)==int and type(tund)==int:  #Vaatan, et mul oleks vähemalt 1 täisarv
        taimeri_sõnum=teadaanne.get()
        töötavad_taimerid.append(taimeri_sõnum)
        taimeri_listboxi_lisamine(töötavad_taimerid)
        aega_kuvamiseni=tund*3600+minut*60+sekund
        lisaaken.destroy()
        jälgi_taimerit(aega_kuvamiseni, taimeri_sõnum)

def jälgi_taimerit(aeg,sõnum):
    global töötavad_taimerid
    aeg -=1
    if aeg==0:
        raam.attributes("-topmost", True)
        messagebox.showinfo(message=sõnum, title="Meeldetuletus")
        raam.attributes("-topmost", False)
        töötavad_taimerid.remove(sõnum)
        taimeri_listboxi_lisamine(töötavad_taimerid)
    elif sõnum in töötavad_taimerid:
        raam.after(1000,jälgi_taimerit,aeg,sõnum)
    else:
        pass

def eemalda_taimer(event=0):  
    global töötavad_taimerid
    sõnum = taimeri_listbox.get(ANCHOR)
    try:
        töötavad_taimerid.remove(sõnum)
    except:
        pass
    taimeri_listbox.delete(ANCHOR)

def taimeri_listboxi_lisamine(list):
    taimeri_listbox.delete(0,END)
    for element in list:
        taimeri_listbox.insert(END, element)

viimati_klickitud_taimer=0
def hiireklõps(event):
    global töötavad_taimerid, viimati_klickitud_taimer
    if taimeri_listbox.curselection()==viimati_klickitud_taimer:
        taimeri_listbox.selection_clear(0,len(töötavad_taimerid)) # selleks, et highlightimine kohe kaoks
        raam.after(300,taimeri_listboxi_lisamine,töötavad_taimerid)  #selleks, et ma saaksin taimeri listist asju eemaldada
    viimati_klickitud_taimer=taimeri_listbox.curselection()

def radiobutton_job(list,arv):     #teen progrgrammide loetelusse lisamise koha
    if arv==0:
        programmide_lisamise_jutt=ttk.Label(raam, text="Vali jälgimiseks soovitud programm:", background=tausta_värv, font=headeri_font)
    else:
        programmide_lisamise_jutt=ttk.Label(raam, text="Vali eemaldamiseks soovitud programm:", background=tausta_värv, font=headeri_font) 
    programmide_lisamise_jutt.grid(column=4, columnspan=2, row=8, padx=15, pady=5, sticky=(W))
    programmide_listbox=Listbox(raam, height=5, width=int(ekraani_laius*0.06*0.7), selectmode="single")
    programmide_listbox.grid(row=9, column=4, padx=15, columnspan=2, sticky=(W))
    prog_scrollbar=Scrollbar(raam)
    prog_scrollbar.grid(row=9, column=4, columnspan=2, sticky=(E,N,S))
    prog_scrollbar.config(command=programmide_listbox.yview)
    programmide_listbox.config(yscrollcommand=prog_scrollbar.set)
    for element in list:
        programmide_listbox.insert(END, element)

    
#siia siis äkki värvid lisada?
tausta_värv= '#%02x%02x%02x' % (242, 242, 242)
nupu_värv= '#%02x%02x%02x' % (192, 204, 208)
headeri_teksti_värv='blue'


raam=Tk()
raam.configure(bg = tausta_värv)
raam.title("Projekt")
raam.geometry('%dx%d+%d+%d' % (ekraani_laius, ekraani_kõrgus, 0.15*ekraani_laius, 0.15*ekraani_kõrgus))

#pakun välja, et siia võiks kokku kirjutada nt kõik kasutatavad fondid
headeri_font= font.Font(size=10, weight='bold')


raam.bind_all("<Delete>", eemalda_taimer)
raam.bind_all('<1>', hiireklõps)


#Teen kõige ülemise headeri rea:
töötavate_programmide_header = ttk.Label(raam, text="Töötavate programmide nimekiri",font=headeri_font, background=tausta_värv, foreground=headeri_teksti_värv)
programmide_aktiivsuse_header = ttk.Label(raam, text="Programmi aktiivsus", font=headeri_font, background=tausta_värv, foreground=headeri_teksti_värv)
aja_header = ttk.Label(raam, text="Kulunud aeg", font=headeri_font, background=tausta_värv, foreground=headeri_teksti_värv)
töötavate_programmide_header.grid(column=0, row=0, ipadx=ekraani_laius*0.24*0.7-180, pady=20, sticky=(W), padx=15)
programmide_aktiivsuse_header.grid(column=1, row=0, ipadx=ekraani_laius*0.17*0.7-115, pady=20, sticky=(W), padx=15)
aja_header.grid(column=2, row=0, ipadx=ekraani_laius*0.15*0.7-66, pady=20, sticky=(W),padx=15)
kõikide_aegade_nullimise_nupp = Button(raam, text="Nulli ajad", command=nulli_kõik, width=6, font=headeri_font, bg=nupu_värv)
kõikide_aegade_nullimise_nupp.grid(column=3, row=0, ipadx=ekraani_laius*0.1*0.7-70, padx=15, pady=20, sticky=(W))

#teen stopperi:
stopper=ttk.Label(raam, text="Stopper:", font=headeri_font, background=tausta_värv)
stopper.grid(column=4, row=1, ipadx=ekraani_laius*0.01, pady=5, padx=15, sticky=(W))
#selleks, et nupud ei liiguks:
stopperi_aja_koht=ttk.Label(raam, text="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", foreground=tausta_värv, background=tausta_värv)
tühi_rida=Label(raam, background=tausta_värv, text="aaaaaaaaaaaaaaa", foreground=tausta_värv).grid(row=0, column=6)
tühi_rida=Label(raam, background=tausta_värv, text="aaaaaaaaaaaaaaaa", foreground=tausta_värv).grid(row=0, column=7)
stopperi_aja_koht.grid(column=5, row=1, columnspan=3, pady=5, padx=15, sticky=(W))
stopperi_käivitamise_nupp = Button(raam, text="Käivita stopper", command=käivita_stopper, width=12, bg=nupu_värv, font=headeri_font)
stopperi_käivitamise_nupp.grid(column=4, row=0, ipadx=ekraani_laius*0.1*0.7-70, pady=5, padx=15, sticky=(W))
stopperi_nullimise_nupp= Button(raam, text="Nulli stopper", command=nulli_stopper, width=12, bg=nupu_värv, font=headeri_font)
stopperi_nullimise_nupp.grid(column=5, row=0, pady=5, sticky=(W), padx=15)

#teen taimeri
taimeri_lisamise_nupp=Button(raam, text="Lisa taimer", command=käivita_taimer, width=12, bg=nupu_värv, font=headeri_font)
taimeri_lisamise_nupp.grid(column=4, row=3, pady=5, padx=15, sticky=(W))
taimeri_eemaldamise_nupp=Button(raam, text="Eemalda taimer", command=eemalda_taimer, width=13, bg=nupu_värv, font=headeri_font)
taimeri_eemaldamise_nupp.grid(column=5, row=3, pady=5, padx=15, sticky=(W))
taimeri_tekst=ttk.Label(raam, text="Hetkel töös olevad taimerid:", background=tausta_värv)
taimeri_tekst.grid(row=5, column=4, columnspan=2, sticky=(W), padx=0)
taimeri_listbox=Listbox(raam, height=5, width=int(ekraani_laius*0.06*0.7), selectmode="single")
taimeri_listbox.grid(row=6, column=4, padx=15, columnspan=2, sticky=(W))
scrollbar=Scrollbar(raam)
scrollbar.grid(row=6, column=4, columnspan=2, sticky=(E,N,S))
scrollbar.config(command=taimeri_listbox.yview)
taimeri_listbox.config(yscrollcommand=scrollbar.set)

#teen programmide lisamiseks ja eemaldamiseks radiobuttonid
var=IntVar()
nupp_eemalda=Radiobutton(raam, text="Eemalda programme",value=2, variable=var, command=lambda: radiobutton_job(katse_olemasolev,1))
nupp_eemalda.grid(row=7, column=5, padx=15, pady=5, columnspan=2, sticky=(W))
nupp_lisa=Radiobutton(raam, text="lisa programme", value=1, variable=var, command=lambda: radiobutton_job(katselist,0))
nupp_lisa.grid(row=7, column=4, padx=15, pady=5, sticky=(W))

                      

#testiks

# I broke some shit. will fix some time.
"""
shown_processes=[]
shown_processes_status=[]
shown_processes_time=[]
for i in backend.processes:
    process_name=
    shown_processes[i] = ttk.Label(raam,text=backend.GetProcessName(processes[i][0]))
    shown_processes[i].grid(column=0,row=i,padx=20,pady=5,sticky=(W))
    shown_processes_status[i] = ttk.Label(raam,text=backend.GetProcessStatus(backend.processes[i][0]))
    shown_processes_status[i].grid(column=1,row=i, pady=5, sticky=(W))
    shown_processes_time[i] = ttk.Label(raam, text=str(backend.processes[i][1]))
    shown_processes_time[i].grid(column=2, row=i, pady=5, sticky=(W))"""


stopperi_näidatav_aeg3=ttk.Label(raam, text= "2 tundi, 30 minutit, 25 sekundit.")

nulli=Button(raam, text="Nulli", command=nulli_stopper, width=8, bg=nupu_värv, font=headeri_font)
nulli.grid(column=3, row=1, pady=5)

raam.mainloop()
