import subprocess
import sys

#subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", """(Get-Process | ft Name,@{label="Elapsed Time";expression={[System.Math]::Round(((Get-Date)-$_.StartTime).totalseconds)}})"""])
#subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", """New-TimeSpan -Start (get-process winamp).StartTime"""])

filename="winamp.exe"

query = """New-TimeSpan -Start (get-process """+filename[0:-4]+""").StartTime"""
p_tasklist = subprocess.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", query], stdout=sys.stdout)
newresult = sys.stdout.flush()
print(p_tasklist)
output = p_tasklist.communicate()[0]
print(output)
result=output.split()
print(result)