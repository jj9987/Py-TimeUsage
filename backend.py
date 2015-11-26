import subprocess
import csv
#from os import getpid
import os


p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                              stdout=subprocess.PIPE,
                              universal_newlines=True)

pythons_tasklist = []
for p in csv.DictReader(p_tasklist.stdout):
	#print(p)
	if p['Image Name'] == 'python.exe':
		pythons_tasklist.append(p)

print(pythons_tasklist)


"""with open("/proc/{}/stat".format(getpid())) as f:
    data = f.read()

foreground_pid_of_group = data.rsplit(" ", 45)[1]
is_in_foreground = str(getpid()) == foreground_pid_of_group"""

"""
pid = os.getpid()
print(pid)

if "+" in subprocess.check_output(["ps", "-o", "stat=", "-p", str(pid)]):
	print("Running in foreground")
else:
	print("Running in background")"""

#pids = []
#a = os.popen("tasklist").readlines()

"""for x in a:
	print(x)
	try:
		pids.append(int(x[29:34]))
	except:
		pass
for each in pids:
	print(each)
	"""

""" + CREATE FILE IN FORM OF PROCESS: TIME RUN IN FG : TIME RUN IN BG """

processes=[]

def CreateFile():
	print("hi")

def LoadFile():
	print("hola")

def AddNewApplication(processname):
	processes += [processname,0]
	return True

def GetProcessTime(processname):
	return "0"

def GetProcessStatus(processname):
	return "TEST-Running"


