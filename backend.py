import subprocess
import csv
import os
from time import sleep

processes=[]
all_ok=True

# opens the file for saving data, creates if can not open
if(os.path.isfile("applications.txt")):
	with open("applications.txt") as f:
		for line in f:
			line=line.split()
			processes.append([line[0],int(line[1])])
print(processes)

def AddNewApplication(processname):
	processes[processname] = 0
	print(processes)
	return True

def GetProcessTime(processname):
	return processes[processname]

def GetProcessStatus(processname):
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                              stdout=subprocess.PIPE,
                              universal_newlines=True)

	for p in csv.DictReader(p_tasklist.stdout):
		if(p['Image Name'] == processname):	return "Running"

	return "Not running"


i=0

while(all_ok == True):
	i+=1
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                              stdout=subprocess.PIPE,
                              universal_newlines=True)

	for p in csv.DictReader(p_tasklist.stdout):
		if(p['Image Name'] == "chrome.exe"):
			continue
		for item in processes:
			if(item[0] == p['Image Name']):
				item[1] += 1
				continue

	if(i==300): # updates file after every 5 minutes
		with open("applications.txt", "w") as f:
			for item in processes:
				f.write(item[0]+" "+item[1])

	print(processes)
	sleep(1)