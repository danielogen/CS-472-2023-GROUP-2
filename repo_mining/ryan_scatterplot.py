import pandas as pd # Used to easily parse csv file
from matplotlib import pyplot as plt
from datetime import datetime

df = pd.read_csv("data/SRC_file_tracking_rootbeer.csv")

num_files = df['Filename'].nunique()
num_authors = df['Author'].nunique()

filenames = list(df['Filename'])
distinct_files = list(df['Filename'].unique())
distinct_authors = list(df['Author'].unique())

x = []
y = []

for file in filenames:
    x.append(distinct_files.index(file))

# Convert the date strings to datetime objects
dates = list(df['TouchedOnDate'])
format = "%Y-%m-%dT%H:%M:%SZ"
date_time = []

for date in dates:
    date_time.append(datetime.strptime(date, format))

oldest_commit = min(date_time)
newest_commit = max(date_time)

print(newest_commit)

diff = newest_commit - oldest_commit

# Amount of weeks since the commit date (floored in divison)
for date in date_time:
    y.append((date - oldest_commit).days // 7)

# Color code by unique author
plt.scatter(x, y, c=pd.Categorical(df['Author']).codes, cmap='Dark2')
plt.xlabel('File')
plt.ylabel('Weeks')
plt.show()