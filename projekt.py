try: #Python 3
    from tkinter import *
    from tkinter import ttk, font
    from tkinter import messagebox
except ImportError: #Python 2
    from Tkinter import *
    from Tkinter import ttk, font
    from Tkinter import messagebox
import ctypes
import subprocess
import csv
import os
import threading
from time import sleep


global startupinfo
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

global processes
processes=[]
töötavad_taimerid=[]

user32 = ctypes.windll.user32
ekraani_laius= round(0.72*user32.GetSystemMetrics(0))
ekraani_kõrgus= round(0.7*user32.GetSystemMetrics(1))

def nulli_kõik():   #vajab täielikku tegemist
    a=1 #lihtsalt, et siin miadgi oleks hetkel :D

stopperi_sekundid=0
stopperi_minutid=0
stopperi_tunnid=0

def lel(string):
    return string

def update_processes():
    count=1
    for i in processes:      
        Check_Application(i[0])
        shown_processes = ttk.Label(raam,text=i[0], background=tausta_värv)
        shown_processes.grid(column=0,row=count,padx=20, sticky=(W))
        shown_processes_status = ttk.Label(raam,text=i[2], background=tausta_värv)
        shown_processes_status.grid(column=1,row=count, padx=20, sticky=(W))
        shown_processes_time = ttk.Label(raam, text=seconds_conversion(i[1]), background=tausta_värv)
        shown_processes_time.grid(column=2, row=count, padx=20, sticky=(W))
        count+=1

def seconds_conversion(time):
    minutes=int(time/60)
    if(minutes >= 60):
        hours = int(minutes/60)
        minutes = minutes - hours*60
        result = str(hours) + " tundi " + str(minutes) + " minutit " + str(time%60) + " sekundit "
    elif(time < 60): result = str(time) + " sekundit " # less than 60 seconds
    elif(time >= 60 and time < 3600): result = str(minutes) + " minutit " + str(time%60) + " sekundit "
    return result

def Check_Application(filename):
    error="INFO: No tasks are running which match the specified criteria.\n"
    query = """tasklist /FI "IMAGENAME eq """+str(filename)+""" " """
    #print(query)
    p_tasklist = subprocess.Popen(query, stdout=subprocess.PIPE, universal_newlines=True, startupinfo=startupinfo)
    result = p_tasklist.communicate()[0]
    if(result == error): 
        for item in processes:
            if(item[0] == filename):
                item[2] = "Ei tööta"
                break
    else:
        for item in processes:
            item[2] = 0 # set running status to 0, will be set to 1 if found later ;)
            if(item[0] == filename):
                item[1] +=1
                item[2] = "Töötab"
                break
    #print(result)

def SaveData():
    with open("applications.txt", "w") as f:
        for item in processes:
            f.write(item[0]+" "+str(item[1])+"\n")

def LoadFile():
    """# opens the file for saving data, creates if can not open
    if(not os.path.isfile("applications.txt")):
        fail=open("applications.txt",'w')
        fail.close()
    else:
        with open("applications.txt") as f:
            for line in f:
                line=line.split()
                processes.append([line[0],int(line[1]),0])
                print("success")"""
    with open("applications.txt") as f:
        for line in f:
            line=line.split()
            processes.append([line[0],int(line[1]),0])

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
    try:
        raam.after_cancel(tiksumise_id) # juhuks kui nullimise nupu vajutades pole stopperit tööle pandud
    except:
        pass

def nulli_stopper():
    global stopperi_sekundid, stopperi_minutid, stopperi_sekundid, stopperi_näidatav_aeg
    peata_stopper()
    stopperi_sekundid=0
    stopperi_minutid=0
    stopperi_tunnid=0
    try: 
        stopperi_näidatav_aeg.destroy()
    except: 
        pass

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


viimati_klickitud_taimeri_koht=0
viimati_klickitud_programmi_koht=0
def hiireklõps(event=0):
    global töötavad_taimerid, viimati_klickitud_taimeri_koht, katselist, katse_olemasolev, viimati_klickitud_programmi_koht, programmide_listbox, after_id
    if taimeri_listbox.curselection()==viimati_klickitud_taimeri_koht:
        taimeri_listbox.selection_clear(0,len(töötavad_taimerid)) # selleks, et highlightimine kohe kaoks
        raam.after(300,taimeri_listboxi_lisamine,töötavad_taimerid)  #selleks, et ma saaksin taimeri listist asju eemaldada
    else:
        kontrollarv=1
    viimati_klickitud_taimeri_koht=taimeri_listbox.curselection()

    try:            #juhuks kui programmide listoxi pole loodud
        #print(programmide_listbox.curselection()==viimati_klickitud_programmi_koht)
        if programmide_listbox.curselection()==viimati_klickitud_programmi_koht:
            if len(katselist)>len(katse_olemasolev):
                pikkus=len(katselist)
            else:
                pikkus=len(katse_olemasolev)
            programmide_listbox.selection_clear(0, pikkus) # selleks, et highlightimine kohe kaoks
            arv=leia_arv()
            if arv==0:
                lisatav_list=katselist
            else:
                lisatav_list=katse_olemasolev
            after_id=raam.after(300,programmide_listboxi_lisamine, lisatav_list)  #selleks, et ma saaksin  normaalselt taimeri listist asju eemaldada
        viimati_klickitud_programmi_koht=programmide_listbox.curselection()    
    except:
        pass

def radiobutton_job(saadud_list):     #teen progrgrammide loetelusse lisamise koha
    global programmide_jutt, programmide_listbox, after_id, prog_scrollbar, nupp, programmi_sisend
    arv=leia_arv()
    try:
        raam.after_cancel(after_id)    #juhuks kui after pole veel välja kutsutud
    except:
        pass
    try:                              #et boldis tekst tuleks korralikult
        programmide_jutt.destroy()
    except:
        pass     
    if arv==0:
        try:
            programmide_listbox.destroy()        #juhuks kui esimene radiobutton on programmide lisamine
            prog_scrollbar.destroy()
            nupp.destroy()
        except:
            try:
                nupp.destroy()
            except:
                pass
        programmide_jutt=ttk.Label(raam, text="Lisa jälgimiseks soovitud programm:", background=tausta_värv, font=headeri_font)
        programmide_jutt.grid(column=4, columnspan=2, row=8, padx=15, pady=5, sticky=(W))
        info=ttk.Label(raam, text="Siia tuleks lisada exe faili nimi soovitavast failist:", background=tausta_värv)
        info.grid(column=4, columnspan=2, row=9, padx=15, pady=5, sticky=(W))        
        programmi_sisend=ttk.Entry(raam, background=tausta_värv, width=int(ekraani_laius*0.059*0.7))
        programmi_sisend.grid(row=10, column=4, columnspan=2, pady=5, padx=15, sticky=(W))
        nupp=Button(raam, text="Lisa programm", command=lambda: lisa_programm(programmi_sisend.get()), width=25, font=headeri_font, bg=nupu_värv)
        nupp.grid(column=4, row= 11, columnspan=2, padx=15, pady=5, sticky=(W))
    else:
        try:
            programmide_listbox.destroy()        #juhuks kui mingi idioot peaks 2 korda samat nuppu vajutama
            prog_scrollbar.destroy()
            programmi_sisend.destroy()
        except:
            try:
                programmi_sisend.destroy()
            except:
                pass
        
        programmide_jutt=ttk.Label(raam, text="Vali eemaldamiseks soovitud programm:", background=tausta_värv, font=headeri_font)
        programmide_jutt.grid(column=4, columnspan=2, row=8, padx=15, pady=5, sticky=(W))
        programmide_listbox=Listbox(raam, height=5, width=int(ekraani_laius*0.06*0.7), selectmode="single", background=listi_värv)
        programmide_listbox.grid(row=9, column=4, padx=15, columnspan=2, sticky=(W))
        prog_scrollbar=Scrollbar(raam, troughcolor='blue')
        prog_scrollbar.grid(row=9, column=4, columnspan=2, sticky=(E,N,S))
        prog_scrollbar.config(command=programmide_listbox.yview)
        programmide_listbox.config(yscrollcommand=prog_scrollbar.set)
        programmide_listbox.delete(0,END)
        for element in saadud_list:
            programmide_listbox.insert(END, element[0])
        try:
            nupp.destroy()
        except:
            pass
        nupp=Button(raam, text="Eemalda programm", command=lambda: eemalda_programm(programmide_listbox.get(ANCHOR)), width=25, font=headeri_font, bg=nupu_värv)
        nupp.grid(column=4, row= 10, columnspan=2, padx=15, pady=5, sticky=(W))

def leia_arv():
    if var.get()==2:
        return 0
    elif var.get()==1:
        return 1

        
def lisa_programm(nimi):
    processes.append([nimi,0])
    programmi_sisend.delete(0,END)
    
    
def eemalda_programm(nimi):
    for item in processes:
        if item[0] == nimi:
            processes.remove(item)


    
#siia siis äkki värvid lisada?
tausta_värv= '#%02x%02x%02x' % (200, 250, 200)
nupu_värv= '#%02x%02x%02x' % (150, 244, 208)
headeri_teksti_värv='blue'
listi_värv='#%02x%02x%02x' % (220, 255, 220)


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
töötavate_programmide_header.grid(column=0, row=0, ipadx=ekraani_laius*0.23*0.7-183, pady=20, sticky=(W), padx=15)
programmide_aktiivsuse_header.grid(column=1, row=0, ipadx=ekraani_laius*0.15*0.7-120, pady=20, sticky=(W), padx=15)
aja_header.grid(column=2, row=0, ipadx=ekraani_laius*0.09*0.7-66, pady=20, sticky=(W),padx=15)
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
taimeri_listbox=Listbox(raam, height=5, width=int(ekraani_laius*0.06*0.7), selectmode="single", background=listi_värv)
taimeri_listbox.grid(row=6, column=4, padx=15, columnspan=2, sticky=(W))
scrollbar=Scrollbar(raam, background=listi_värv)
scrollbar.grid(row=6, column=4, columnspan=2, sticky=(E,N,S))
scrollbar.config(command=taimeri_listbox.yview)
taimeri_listbox.config(yscrollcommand=scrollbar.set)

#teen programmide lisamiseks ja eemaldamiseks radiobuttonid
var=IntVar()
nupp_eemalda=Radiobutton(raam, text="Eemalda programme",value=1, variable=var, command=lambda: radiobutton_job(processes), bg=tausta_värv)
nupp_eemalda.grid(row=7, column=5, padx=15, pady=5, columnspan=2, sticky=(W))
nupp_lisa=Radiobutton(raam, text="Lisa programme", value=2, variable=var, command=lambda: radiobutton_job([]), bg=tausta_värv)
nupp_lisa.grid(row=7, column=4, padx=15, pady=5, sticky=(W))

stopperi_näidatav_aeg3=ttk.Label(raam, text= "2 tundi, 30 minutit, 25 sekundit.")

nulli=Button(raam, text="Nulli", command=nulli_stopper, width=8, bg=nupu_värv, font=headeri_font)
nulli.grid(column=3, row=1, pady=5)

class Updater (threading.Thread):
    def __init__(self, threadID, name, counter, event):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.stopped = event
    def run(self):
        while not self.stopped.wait(0.5):
            update_processes()
    def stop(self):
        self.stopped.set()

global thread1, stopFlag
stopFlag = threading.Event()
thread1 = Updater(1,"Thread-1",1,stopFlag)
#thread2.start()

LoadFile()
Check_Application("chrome.exe")
update_processes()

def callback(): # callback when closing application from X
    if messagebox.askokcancel("Välju", "Kas sa soovid programmi sulgeda?"):
        raam.destroy()
        #SaveData()
        stopFlag.set()


raam.protocol("WM_DELETE_WINDOW", callback)

raam.mainloop()


#SaveData()
