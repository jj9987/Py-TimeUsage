def seconds_conversion(time):
	minutes=int(time/60)
	if(minutes >= 60):
		hours = int(minutes/60)
		minutes = minutes - hours*60
		result = str(hours) + " tundi " + str(minutes) + " minutit " + str(time%60) + " sekundit "
	elif(time < 60): result = str(time) + " sekundit " # less than 60 seconds
	elif(time >= 60 and time < 3600): result = str(minutes) + " minutit " + str(time%60) + " sekundit "
	print(result)

for i in range(5000):
	seconds_conversion(i)
