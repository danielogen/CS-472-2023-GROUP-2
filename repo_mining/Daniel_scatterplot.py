from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os 
from pathlib import Path
from datetime import datetime
import math
import calendar

# plt.style.use('seaborn')

BASE_DIR = Path(__file__).resolve().parent.parent

if os.path.exists("data"):
    filename = os.path.join(BASE_DIR, "data/file_task2_rootbeer.csv")
else:
    print("Data directory is not available")
    exit(0)

data = pd.read_csv(filename)

# Get the count of unique files
number_of_files = data.Filename.nunique()
# Get the count of unique authors
authors = list(data.Author)
unique_authors = list(data.Author.unique())
number_of_authors = len(unique_authors)

# create list of index of all unique files for our X-axis data
filenames = list(data.Filename)
unique_filenames = list(data.Filename.unique())
x = [unique_filenames.index(i) for i in filenames]

# create Y-axis data from commit date
commit_date = list(data.TouchedOn)
datetime_object = [datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ') for dt in commit_date]

min_date = min(datetime_object)
max_date = max(datetime_object)

# compute the y limit
max_y_value = max_date - min_date

# compute the values of Y in weeks
y = [math.ceil((item - min_date).days / 7) for item in datetime_object]

# Set the figure size
plt.figure(figsize=(10, 5))

# Plot author activities overtime - this answers task task2
plt.scatter(x, y, s=50, c=pd.Categorical(data.Author).codes,
            cmap='tab10', edgecolors='black', linewidths=1, alpha=0.75)
plt.xticks(np.arange(min(x), max(x) + 1, 1))
plt.xlabel('File Index')
plt.ylabel('Weeks')
#plt.show()

# More plots
# 1. Plot authors' tool commits since they joined the project 
bar_data = pd.DataFrame(data['Author'].value_counts(ascending=True))
bar_data = bar_data.reset_index()
bar_data.columns = ['Authors', 'Counts']

plt.figure(figsize=(10, 5))
plt.barh(bar_data.Authors, bar_data.Counts, alpha=0.75, edgecolor="black")
plt.yticks(rotation=45)
plt.xlabel('No. of Commits')
#plt.show()

# 2. Plot overall monthly activities for each developer
x_monthly = [item.month for item in datetime_object]
y_authors = [unique_authors.index(i) for i in authors]

plt.figure(figsize=(10, 5))
plt.scatter(x_monthly, authors, s=50, c=pd.Categorical(data.Author).codes,
            cmap='tab10',linewidths=1, marker="x")
plt.xticks(np.arange(min(x_monthly), max(x_monthly) + 1, 1))
plt.yticks(rotation=45)
plt.xlabel('Month')
plt.ylabel('Authors')
plt.show()

# 3. Aggregate commits by months
plt.figure(figsize=(10, 5))

data['month'] = x_monthly
month_data = pd.DataFrame()
month_data['months'] = list(data.month.unique())
month_data['counts']= list(data.month.value_counts())
month_data['month_name'] = [calendar.month_name[i] for i in list(month_data.months)]
month_data.sort_values(by='months', ascending=True, inplace=True)

plt.plot(month_data.months, month_data.counts, alpha=0.7, color='red', marker="o")
plt.xticks(np.arange(min(month_data.months), max(month_data.months) + 1, 1))
plt.xlabel('Month')
plt.ylabel('No. of Commits')
plt.show()

# 3. Aggregate commits by day of the week

x_weekly = [item.weekday() for item in datetime_object]
data['week'] = x_weekly
week_data = pd.DataFrame()
week_data['weeks'] = list(data.week.unique())
week_data['counts']= list(data.week.value_counts())
week_data['week_name'] = [calendar.day_name[i] for i in list(week_data.weeks)]
week_data.sort_values(by='weeks', ascending=True, inplace=True)

plt.figure(figsize=(10, 5))
plt.plot(week_data.week_name, week_data.counts, alpha=0.75, color='green', marker="X")
plt.xticks(np.arange(min(week_data.weeks), max(week_data.weeks) + 1, 1))
plt.xlabel('Day of Week')
plt.ylabel('Commits')
plt.show()
