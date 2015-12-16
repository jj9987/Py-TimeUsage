import subprocess
import csv
import os

global startupinfo
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def Check_Application(filename):
	error="INFO: No tasks are running which match the specified criteria.\n"
	query = """tasklist /FI "IMAGENAME eq """+filename
	#print(query)
	p_tasklist = subprocess.Popen(query, stdout=subprocess.PIPE, universal_newlines=True, startupinfo=startupinfo)
	result = p_tasklist.communicate()[0]
	if(result == error): 
		for item in processes:
			if(item[0] == filename):
				item[2] = 0
				break
	else:
		for item in processes:
			item[2] = 0 # set running status to 0, will be set to 1 if found later ;)
			if(item[0] == filename):
				item[1] +=1
				item[2] = 1
				break
	#print(result)

global processes
processes=[]

# opens the file for saving data, creates if can not open
if(not os.path.isfile("applications.txt")):
	fail=open("applications.txt",'w')
	fail.close()
else:
	with open("applications.txt") as f:
		for line in f:
			line=line.split()
			processes.append([line[0],int(line[1]),0])


Check_Application("chrome.exe")
def GetProcessTime(processname):
	for item in processes:
		if(item[0] == processname):
			return item[1]
			break
	return "ERROR"

def GetProcessStatus(processname):
	for item in processes:
		if(item[0] == processname):
			if(item[2] == 1): 
				break
				return "Töötab"
	return "Ei tööta"

def SaveData():
	with open("applications.txt", "w") as f:
		for item in processes:
			f.write(item[0]+" "+str(item[1])+"\n")


