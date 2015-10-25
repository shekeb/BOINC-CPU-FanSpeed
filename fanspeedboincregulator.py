#!/usr/bin/env python

# This script will allow older Mac computers to run BOINC at the highest CPU load possible without spinning up the fan. The fan spins up when the CPU gets too hot. At higher spin rates I find the fan to be annoyingly loud.
# This script has been optimized for the early 2008 MacBook (MacBook 4,1) but should work equally well for other Macs as well. It can be easily modified for a Windows system.
# Author: Shekeb Khan

# define a function that can edit the BOINC global preferences file and ask ask BOINC to use this updated file.
def adjustcpuusage(cpudelta):


	# open the current global preferences file 
	file = open('/Library/Application Support/BOINC Data/global_prefs_override.xml', 'r') # open the global prefs file
	data = file.read() # read its data
	file.close()   # close the file, just to be safe. data is still available to manipulate.


	# search for the string defining cpu usage and change it in line with the current fan speed
	searchstart = '<cpu_usage_limit>'
	searchend = '</cpu_usage_limit>'
	s = str(data) # convert data to string so I can more easily manipulate it
	s2 = (s.split(searchstart))[1].split(searchend)[0] # find the characters in s between searchstart and searchend
	s3 = float(s2) # convert s2 to a floating point real number
	currentcpuusageinteger = int(s3) # convert s3 into an integer. can't convert s2 directly into an integer.



	# lets make sure newcpuusageinteger does not go below lowerlimit percent, or above upperlimit percent. set these to what you like.

	cpuusagelowerlimit = 40  # suggested value is 40
	cpuusagedupperlimit = 99  # suggested value is 99

	#print "CPU usage was " + str(currentcpuusageinteger) + " percent."

	
	newcpuusageinteger = currentcpuusageinteger + cpudelta  # we adjust the cpu load here

	if newcpuusageinteger < cpuusagelowerlimit:
		print "Updated CPU usage of " + str(newcpuusageinteger) + " percent is below lower limit of " + str(cpuusagelowerlimit) + " percent."
		newcpuusageinteger = cpuusagelowerlimit
	elif newcpuusageinteger > cpuusagedupperlimit:
		print "Updated CPU usage of " + str(newcpuusageinteger) + " percent is above upper limit of " + str(cpuusagedupperlimit) + " percent."
		newcpuusageinteger = cpuusagedupperlimit
	else:
		print "Updated CPU usage of " + str(newcpuusageinteger) + " percent is between limits of " + str(cpuusagelowerlimit) + " percent and " + str(cpuusagedupperlimit) + " percent." # I'm not sure how to exit an if clause just yet.
	
	#print "CPU usage is now " + str(newcpuusageinteger) + " percent."





	s6 = str(newcpuusageinteger) + ".000000" # add the appropriate number of 0's back to it. newcpuusageinteger may be 1, 2, or 3 digits in lenght.
	adjustcpuusage.s6 = s6 # I'm defining s6 as an attribute of the function so that I can call it outside of the function.


	# lets search for the full string, just to be safe.
	search2 = searchstart + s2 + searchend
	replacewith = searchstart + s6 + searchend

	print "The string:"
	print search2

	print "has been replaced with the string:"
	print replacewith

	print "i.e. processor usage was changed from " + s2 + " to " + s6 + "."





	# update data as newdata
	newdata = s.replace(search2, replacewith)


	# write newdata back to file, going through an intermediate just to be safe.
	newfile = open('/Library/Application Support/BOINC Data/global_prefs_override_2.xml', 'w') # we'll go through an _2 file just to make sure there are no mistakes.
	newfile.write(newdata)
	newfile.close() # close this file just ot be safe.

	# rename the intermediate back to the original file name
	import os
	os.rename ('/Library/Application Support/BOINC Data/global_prefs_override_2.xml', '/Library/Application Support/BOINC Data/global_prefs_override.xml') # we'll rename this _2 to the original, which will overwrite the original.

	import subprocess 

	# now ask BOINC to use this new global prefs
	import os
	owd = os.getcwd() # define owd as the current working directory. We'll need to come back to this.
	from subprocess import call
	os.chdir("/Library/Application Support/BOINC Data") # this will leave us permanently in this new folder unless we change directories again.
	call(["/Applications/BOINC_command_line_version/boinccmd", "--read_global_prefs_override"]) # boinccmd read global override must be run from the folder containing the prefs file	os.chdir("originalpwd")
	print "BOINC has been asked to use this updated value."
	os.chdir(owd) # this will pring us back to the original working directory defined above.


# function ends.





# find out the current fan speed of the mac using utility iStats,
from subprocess import check_output
import time
starttime=time.time()
while True:
	print ""
	print ""
	print ""
	print ""
	istatsoutput = check_output(["istats", "fan", "speed"]) # run command istats fan speed in a shell and assign its output to the string istatsoutput
	currentspeed = float(istatsoutput[13:19])  # grabs characters 13 to 19 of string istatsoutput as a floating point real number


	# determine if current fan speed is greater than speed limit I have imposed (to keep fan noise down). And use the function if necessary.
	speedlimit = 2250 # assign a speed limit for the fan. we will adjust the boinc processur usage to make sure this speed limit is not exceeped.
	if currentspeed > (speedlimit + 3800):
		print "Current fan speed of " + str(currentspeed) + " RPM is greater than " + str(speedlimit + 3800) + " RPM."
		print "Reducing BOINC load by 5 percent."
		adjustcpuusage(-5)  # reduce CPU load by 10 percentage points (but not below lower limit defined in function)

	elif  (speedlimit + 2000) < currentspeed <= (speedlimit + 3800):
		print "Current fan speed of " + str(currentspeed) + " RPM is > " + str(speedlimit + 2000) + " and <= " + str(speedlimit + 3800) + " RPM."
		print "Reducing BOINC load by 4 percent."
		adjustcpuusage(-4)  # reduce CPU load by 5 percentage points (but not below lower limit defined in function)

	elif  (speedlimit + 1000) < currentspeed <= (speedlimit + 2000):
		print "Current fan speed of " + str(currentspeed) + " RPM is > " + str(speedlimit + 1000) + " and <= " + str(speedlimit + 2000) + " RPM."
		print "Reducing BOINC load by 3 percent."
		adjustcpuusage(-3)  # reduce CPU load by 3 percentage points (but not below lower limit defined in function)

	elif  (speedlimit + 50) < currentspeed <= (speedlimit + 1000):
		print "Current fan speed of " + str(currentspeed) + " RPM is > " + str(speedlimit + 50) + " and <= " + str(speedlimit + 1000) + " RPM."
		print "Reducing BOINC load by 1 percent."
		adjustcpuusage(-1)  # reduce CPU load by 1 percentage points (but not below lower limit defined in function)

	elif  (speedlimit - 50) <= currentspeed <= (speedlimit + 50):
		print "Current fan speed of " + str(currentspeed) + " RPM is > " + str(speedlimit - 50) + " and <= " + str(speedlimit + 50) + " RPM."
		print "Leaving BOINC load unchanged."
		#adjustcpuusage(1)  # increase CPU load by 1 percentage points (but not above upper limit defined in function)

	

	elif  (speedlimit - 150) <= currentspeed < (speedlimit - 50):
		print "Current fan speed of " + str(currentspeed) + " RPM is less than " + str(speedlimit - 50) + " and greather than or equal to " + str(speedlimit - 150) + " RPM."
		print "Increasing BOINC load by 1 percent."
		adjustcpuusage(1)  # increase CPU load by 1 percentage points (but not above upper limit defined in function)


	elif  (speedlimit - 500) <= currentspeed < (speedlimit - 150):
		print "Current fan speed of " + str(currentspeed) + " RPM is less than " + str(speedlimit - 150) + " and greather than or equal to " + str(speedlimit - 500) + " RPM."
		print "Increasing BOINC load by 1 percent."
		adjustcpuusage(1)  # increase CPU load by 1 percentage points (but not above upper limit defined in function)


	elif  currentspeed < (speedlimit - 500):
		print "Current fan speed of " + str(currentspeed) + " RPM is less than " + str(speedlimit - 500) + " RPM."
		print "Increasing BOINC load by 1 percent."
		adjustcpuusage(1)  # increase CPU load by 1 percentage points (but not above upper limit defined in function)

	else:
		print "Current fan speed of " + str(currentspeed) + " RPM is equal to speed limit of " + str(speedlimit) + " RPM."
		print "Leaving BOINC load unchanged."

	# print "did newcpuusageinteger get pulled out of the function and is it printed below? :"
	# print adjustcpuusage.s6

	localtime = time.strftime('%a, %Y/%m/%d %H:%M:%S') # returns the time in format 'Sun, yyyy/mm/dd hh:mm:ss'.
	print "Current time is: ", localtime
	delay = 300 # time in seconds until the next reading.
	nextreading = delay-((time.time() - starttime) % delay) 
	totalruntime = time.time() - starttime # seconds
	totalruntimehours = totalruntime / (60 * 60) # minutes
	totalruntimedays = totalruntime / (60 * 60 * 24) # days
	nextreadingrounded = '{0:.{1}f}'.format(nextreading,1) # this bit rounds nextreading to 1 digit past the decimal point
	totalruntimerounded = '{0:.{1}f}'.format(totalruntime,1) # this bit rounds totalruntime to 1 digit past the decimal point
	totalruntimehoursrounded = '{0:.{1}f}'.format(totalruntimehours,1)
	totalruntimedaysrounded = '{0:.{1}f}'.format(totalruntimedays,1)
	

	with open("BOINCfanlog.csv", "a") as logfile:
		logfile.write("\n" + localtime[0:3] + "," + localtime[5:24] + "," + str(currentspeed) + "," + adjustcpuusage.s6) # \n starts a new line, \t puts in a tab

	print "Log file BOINCfanlog.csv has now been updated."



	print "Now waiting for " + str(nextreadingrounded) + " seconds. Have been running for " + str(totalruntimerounded) + " seconds (/ " + str(totalruntimehoursrounded) + " hours / " + str(totalruntimedaysrounded) + " days). Press control+c to end."
	print ""
	time.sleep(nextreading)

















