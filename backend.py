import subprocess
import csv
import os

global startupinfo
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def worker():
	i=0	
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv', stdout=subprocess.PIPE, universal_newlines=True, startupinfo=startupinfo)
	for p in csv.DictReader(p_tasklist.stdout):
		if(p['Image Name'] == "chrome.exe" or p['Image Name'] == "opera.exe"):
			continue
		for item in processes:
			if(item[0] == p['Image Name']):
				item[1] += 1
				continue
		if(i==300): # updates file after every 5 minutes
			with open("applications.txt", "w") as f:
				for item in processes:
					f.write(item[0]+" "+str(item[1])+"\n")
	i+=1

global processes
processes=[]

# opens the file for saving data, creates if can not open
if(os.path.isfile("applications.txt")):
	with open("applications.txt") as f:
		for line in f:
			line=line.split()
			processes.append([line[0],int(line[1])])


def AddNewApplication(processname):
	processes.append([processname,0])
	return True

def GetProcessTime(processname):
	for item in processes:
		if(item[0] == processname):
			return item[1]
	return "Process not found"

def GetProcessStatus(processname):
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                              stdout=subprocess.PIPE,
                              universal_newlines=True, startupinfo=startupinfo)
	for p in csv.DictReader(p_tasklist.stdout):
		if(p['Image Name'] == processname):	return "Töötab"
	return "Ei tööta"
