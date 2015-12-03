import subprocess
import csv
import os
from time import sleep

processes={}
allok=False

# opens the file for saving data, creates if can not open
with open("applications.txt") as f:
	for line in f:
		line=line.split()
		processes[line[0]] = int(line[1])
print(processes)

def AddNewApplication(processname):
	processes[processname] = 0
	print(processes)
	return True

def GetProcessTime(processname):
	return processes[processname]

def GetProcessStatus(processname):
	return "TEST-Running"

p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                              stdout=subprocess.PIPE,
                              universal_newlines=True)

while(allok == True):
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] in processes:
			processes[p['Image Name']] = processes[p['Image Name']]+1

	print(processes)
	sleep(1)