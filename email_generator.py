import csv

def emailMaker(row):
	if row[1] != "" and row[1] != "None":
		if row[0][:5] == "Satur" or row[0][:5] == "Sunda":
			location = "QNC 1507"
		elif row[0][:5] == "Monda":
			location = "AL 208"
		else:
			location = "nowhere"
		emailText = "Hello "+str(row[1])+",\n\nThanks for signing up for an audition with the Unaccompanied Minors! Your audition is scheduled for "+str(row[0])+" in "+location+"."
		row.append(emailText)
	else:
		row.append("")
	return row

with open('schedule-files/AudSchedule.csv','r') as csvinput:
    with open('schedule-files/TerribleEmailSchedule.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, delimiter="\t")
        reader = csv.reader(csvinput, delimiter="\t")

        newRows = []
        row = next(reader)
        row = emailMaker(row)
        newRows.append(row)

        for row in reader:
            row = emailMaker(row)
            newRows.append(row)

        writer.writerows(newRows)