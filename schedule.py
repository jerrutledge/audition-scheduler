# HOW TO USE THIS FILE

# 1. Give it the columns showing what timeslots people have selected. 
# Select those columns from your spreadsheet, copy and paste them into a file in Sublime Text and save them
# put the file name here
availabilityFileName = "schedule.txt"

# 2. Give it everyone's name and email addresses
# Select the name and email columns from the spreadsheet, copy and paste them into a file in Sublime Text and save them
# put that file name here
namesAndEmailFileName = "Names.txt"

# 3. Give it a file name to output 
# The scheduler generates a .csv file with three columns: 
# 	1 - a name, 
# 	2 - a time,
# 	3 - email text to that person with their email at the top
outputFileName = "TerribleSchedule.csv"

# BEGIN ACTUAL CODE

print "Opening scheduler"


with open(availabilityFileName) as f:
	sundata = f.readlines()

with open(namesAndEmailFileName) as m:
	nameArray = m.readlines()

# make it just the name (before the tab)
for x in xrange(len(nameArray)):
	separatorLocation = nameArray[x].find("\t")
	nameArray[x] = (nameArray[x])[:separatorLocation]

# figure out what possible timeslots there are
totalTimeSlots = []


timeslots = ("12:00pm - 12:30pm", 
"12:30pm - 1:00pm", 
"1:00pm - 1:30pm", 
"1:30pm - 2:00pm", 
"2:00pm - 2:30pm", 
"2:30pm - 3:00pm", 
"3:00pm - 3:30pm", 
"3:30pm - 4:00pm")

actualtimes = ("12:00pm","12:10pm","12:20pm","12:30pm","12:40pm","12:50pm","1:00pm","1:10pm","1:20pm","1:30pm","1:40pm","1:50pm","2:00pm","2:10pm","2:20pm","2:30pm","2:40pm","2:50pm","3:00pm","3:10pm","3:20pm","3:30pm","3:40pm","3:50pm")

output = {"Time":"Person"}

scheduledPeople = ["Jeremy","Ariana"]

with open("alreadyscheduled.txt") as y:
	schppl = y.readlines()

for peep in schppl:
	scheduledPeople.append(peep)

for time in actualtimes:
	output[time] = "None";

fill = [0,0,0,0,0,0,0,0,0,0,0,0]

i = 0
for line in sundata:
	j = 0
	print nameArray[i]
	for availability in timeslots:
		if nameArray[i] in scheduledPeople:
			print "...is already scheduled"
			break
		if availability in timeslots and fill[j] < 3 and line.find(availability) != -1:
			atime = j*3 + fill[j]
			print "...is scheduled!"
			output[actualtimes[atime]] = nameArray[i]
			fill[j] += 1
			break
		j += 1
	i += 1

for key in sorted(output):
	out = key +", "+ output[key]
	print out
