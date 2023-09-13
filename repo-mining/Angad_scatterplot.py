import csv
import datetime
import matplotlib.pyplot as plt

# List of colors for the scatter plot
plotColors = [
    '#282a36', # black
    '#44475a', # dark grey
    '#6272a4', # light grey
    '#8be9fd', # cyan
    '#50fa7b', # green
    '#ffb86c', # orange
    '#ff79c6', # pink
    '#bd93f9', # purple
    '#ff5555', # red
    '#f1fa8c', # yellow
    '#3b87d4', # dark blue
]

# Reading the data in CSV file
def readCSV(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        
        # reading all the rows in the CSV file
        data = [row for row in reader]
        
        # creating empty list for weeks, files, and authors
        weeks = []
        files = []
        authors = []
        
        # creating a set of unique files
        uniqueFiles = set()
        for row in data:
            uniqueFiles.add(row[0])

        # mapping files to numbers
        fileNumber = {}
        for indx, file in enumerate(uniqueFiles, start=1):
            fileNumber[file] = indx
        
        # mapping dates to weeks
        for row in data:
            dateStr = row[2]
            dateObj = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
            weekNum = dateObj.isocalendar()[1]
            
            # appending to lists
            weeks.append(weekNum)
            files.append(fileNumber[row[0]])
            authors.append(row[1])
        
    return weeks, files, authors

# Generate the scatter plot
def scatterPlotGenerator(weeks, files, authors):
    # Creating a list of unique authors
    uniqueAuthors = list(set(authors))
    
    # Mapping colors to unique authors
    authColorMap = {}
    for i in range(len(uniqueAuthors)):
        authColorMap[uniqueAuthors[i]] = plotColors[i % len(plotColors)]
    
    # Plot each data point
    for i in range(len(weeks)):
        week = weeks[i]
        file = files[i]
        author = authors[i]
        color = authColorMap[author]
    
        plt.scatter(file, week, color=color)
    
    plt.xlabel('file')
    plt.ylabel('weeks')
    plt.title('rootbeer repo scatterplot')
    plt.tight_layout()
    plt.show()

weeks, files, authors = readCSV('data/authors_and_dates_rootbeer.csv')
scatterPlotGenerator(weeks, files, authors)