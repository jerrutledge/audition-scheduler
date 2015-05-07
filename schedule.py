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
# Can't handle conflicts & people who don't have auditions


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
			humanReadableTime = format(advanceTime, '%I:%M%p')
			actualtimes[x].append(humanReadableTime)

print totalTimeSlots
print actualtimes
print fill

with open(namesAndEmailFileName) as m:
	nameArray = m.readlines()

# make it just the name (before the tab)
for x in xrange(len(nameArray)):
	nameArray[x] = (nameArray[x])[:-1]

output = {"Time":"Person"}

for x in xrange(len(days)):
	for time in actualtimes[x]:
		output[days[x]+" at "+time] = "None";

# scheduling algorithm
# basically it gives every person their first available choice in order
i = 0 # person whose audition we're scheduling
for line in availabilityFormResponses:
		print nameArray[i]
		for day in xrange(len(days)):
			j = 0 # timeslot on the day we're checking
			for availability in totalTimeSlots[day]:
				if nameArray[i] in scheduledPeople:
					print "...is already scheduled"
					break
				elif availability in totalTimeSlots[day] and fill[day][j] < numberOfActualSlotsInASlot and line.find(availability) != -1:
					atime = j*numberOfActualSlotsInASlot + fill[day][j]
					print "...is scheduled!"
					output[days[day]+" at "+actualtimes[day][atime]] = nameArray[i]
					fill[day][j] += 1
					scheduledPeople.append(nameArray[i])
					break
				j += 1
		i += 1

print scheduledPeople

# Handle people who don't yet have auditions
print "Number of people without auditions: "+str(len(nameArray) - len(scheduledPeople) - 1)
noAuditioners = []
i = 0 # remove header row
for person in nameArray:
	if i == 0:
		i = 1
		continue
	if person not in scheduledPeople:
		print person
		noAuditioners.append(person)

# console schedule
print "Schedule:"
for key in sorted(output):
	out = key +", "+ output[key]
	print out

# write to csv file
with open(outputFileName, 'wb') as csvfile:
	auditionGenerator = csv.writer(csvfile)
	for key in output:
		separatorLocation = output[key].find("\t")

		auditionTime = key
		auditionName = (output[key])[:separatorLocation]
		auditionEmail = (output[key])[separatorLocation+1:]

		auditionGenerator.writerow([auditionTime, auditionName, auditionEmail])

	for fail in noAuditioners:
		separatorLocation = fail.find("\t")

		auditionName = fail[:separatorLocation]
		auditionEmail = fail[separatorLocation+1:]
		auditionGenerator.writerow(["No Scheduled Time", auditionName, auditionEmail])

