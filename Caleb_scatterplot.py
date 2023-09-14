import pandas as pd
import math
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

data = pd.read_csv("data/detailed_file_rootbeer.csv")
files = list(data['Filename'])
uniqueFiles = list(data['Filename'].unique())
authors = list(data['Author'])
uniqueAuthors = list(data['Author'].unique())
dates = list(data['Date'])

# Manage weeks
earliestDate = datetime.fromisoformat(dates[-1])
for i, date in enumerate(dates):
  dates[i] = math.floor((datetime.fromisoformat(date)-earliestDate) / timedelta(weeks=1))

# Manage filenames
for i, filename in enumerate(files):
  files[i] = uniqueFiles.index(filename)

plt.figure(figsize=(10,5))
plt.scatter(files, dates, c=pd.Categorical(data.Author).codes, cmap='tab10', linewidths=1, alpha=1)
plt.xticks(range(0, max(files)+1, 1))
plt.title('Author File Touches')
plt.xlabel('files')
plt.ylabel('weeks')

plt.show()