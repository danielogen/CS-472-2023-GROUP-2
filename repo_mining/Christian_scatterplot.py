import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

seenFiles = []
seenAuthors = []
dates = []
commitWeeks = []
xData = []
colors = []
# Script assumes Christian_authorsFileTouches.py finished and used this relative path
fileInputPath = 'data/authorsFileTouches_rootbeer.csv'

# Get the data from the csv
with open(fileInputPath, mode ='r') as file:
       rows = csv.reader(file, delimiter=',')
       # Skip header line
       next(file)
       for row in rows:
              compareFilename = row[0]
              # If filename was unseen, add it and note the author/filename
              if compareFilename not in seenFiles:
                     seenFiles.append(compareFilename)
              # Store the x coordinate
              xData.append(seenFiles.index(compareFilename))
              # Similar process for authors
              compareAuthor = row[1]
              if compareAuthor not in seenAuthors:
                     seenAuthors.append(compareAuthor)
              # Store the point's color
              colors.append(seenAuthors.index(compareAuthor))
              # Process dates
              dates.append(datetime.strptime(row[2], '%Y-%m-%dT%H:%M:%SZ'))

       # Get min and max dates
       minDate = min(dates)
       maxDate = max(dates)
       totalTime = maxDate - minDate
       weekCnt = totalTime.days / 7
       weekCnt = int(totalTime.total_seconds())
       weekCnt = weekCnt / 604800
       # Calculate weeks for each commit
       for date in dates:
              tempDate = date - minDate
              weekElement = tempDate.days / 7
              weekElement = int(tempDate.total_seconds())
              weekElement = weekElement / 604800
              commitWeeks.append(weekElement)

# Plot setup and presentation
plt.style.use('classic')
fig, ax = plt.subplots(figsize=(15,10))
ax.scatter(xData, commitWeeks, s=80, c=colors)
ax.set(xlim=(-1, len(seenFiles)+1), xticks=np.arange(0, len(seenFiles)+1, 2), xlabel="File Number",
       ylim=(-25, weekCnt+25), yticks=np.arange(0, weekCnt+25, 50), ylabel="Weeks")
plt.show()