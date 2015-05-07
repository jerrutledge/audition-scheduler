# HOW TO USE THIS FILE

# 1. Give it the columns showing what timeslots people have selected. 
# Select those columns from your spreadsheet, 
# copy and paste them into a file in Sublime Text
# and save them in the schedule-files folder
# put this file name here
availabilityFormResponsesFileName = "schedule-files/responses.txt"

# 2. Give it everyone's name and email addresses
# Select the name and email columns from the spreadsheet, 
# copy and paste them into a file in Sublime Text 
# and save them in the schedule-files folder
# put that file name here
namesAndEmailFileName = "schedule-files/Names.txt"

# 3. Give it a file name to output 
# The scheduler generates a .csv file with three columns: 
# 	1 - a name, 
# 	2 - an email,
# 	3 - a day + time,
# You can save this wherever you want, but don't put them in this same folder (use schedule-files)
outputFileName = "schedule-files/TerribleSchedule.csv"


# Limitations

# Thirty minute time slots are the only option, with 10 minute auditions
# only am/pm time supported
# 


# BEGIN ACTUAL CODE
import csv
import time
import datetime
from datetime import timedelta
from dateutil import parser

print "Opening scheduler"

with open(availabilityFormResponsesFileName) as f:
	availabilityFormResponses = f.readlines()

# important arrays:
totalTimeSlots = []
days = []
actualtimes = [] # human readable times
fill = []
scheduledPeople = []

# important constants
numberOfActualSlotsInASlot = 3
timeSlotLengthInMinutes = 10

# figure out what possible timeslots there are
tabSeparatedValues = csv.reader(availabilityFormResponses, delimiter="\t")
i = 0
for row in tabSeparatedValues:
	if i == 0:
		i = 1
		for day in row:
			days.append(day)
		print "Days of auditions:"
		print days

		# initialize totalTimeSlots as a multidimensional array
		totalTimeSlots = [[] for i in range(len(days))]
		actualtimes = [[] for i in range(len(days))]
		fill = [[] for i in range(len(days))]
	else:
		for x in xrange(len(days)):
			timeValues = row[x].split(", ")
			for timeSlot in timeValues:
				if timeSlot != "" and timeSlot not in totalTimeSlots[x]:
					totalTimeSlots[x].append(timeSlot)

# populate the fill variable
for x in xrange(len(days)):
	for timeSlot in totalTimeSlots[x]:
		fill[x].append(0)

		# add human readable times
		separatorLocation = timeSlot.find(" - ")
		timeString = timeSlot[:separatorLocation]
		startTime = parser.parse(timeString)
		for y in xrange(numberOfActualSlotsInASlot):
			advanceTime = startTime + timedelta(minutes=y*timeSlotLengthInMinutes)
			humanReadableTime = format(advanceTime, '%H:%M%p')
			actualtimes[x].append(humanReadableTime)

print totalTimeSlots
print actualtimes
print fill

with open(namesAndEmailFileName) as m:
	nameArray = m.readlines()

# make it just the name (before the tab)
for x in xrange(len(nameArray)):
	separatorLocation = nameArray[x].find("\t")
	nameArray[x] = (nameArray[x])[:separatorLocation]

output = {"Time":"Person"}

for x in xrange(len(days)):
	for time in actualtimes[x]:
		output[days[x]+" at "+time] = "None";

i = 0
for line in availabilityFormResponses:
	j = 0
	for day in xrange(len(days)):
		print "DAY: "+days[day]
		print nameArray[i]
		for availability in totalTimeSlots[day]:
			if nameArray[i] in scheduledPeople:
				print "...is already scheduled"
				break
			if availability in totalTimeSlots[day] and fill[day][j] < numberOfActualSlotsInASlot and line.find(availability) != -1:
				atime = j*numberOfActualSlotsInASlot + fill[day][j]
				print "...is scheduled!"
				output[actualtimes[atime]] = nameArray[i]
				fill[day][j] += 1
				break
			j += 1
		i += 1

print scheduledPeople

for key in sorted(output):
	out = key +", "+ output[key]
	print out
