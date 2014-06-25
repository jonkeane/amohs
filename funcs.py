import csv

# this is not zip safe, see: http://stackoverflow.com/questions/1011337/relative-file-paths-in-python-packages
from os import path
resources_dir = path.join(path.dirname(__file__), 'resources')

##### read in csvs containing information about the prosodic model notation system. #####
def read_csv_data(path):
    """Reads CSV from given path and Return list of dict with Mapping"""
    data = csv.reader(open(path))
    # Read the column names from the first line of the file
    fields = data.next()
    data_lines = []
    for row in data:
        items = dict(zip(fields, row))
        data_lines.append(items)
    return data_lines

def dictToCols(dictObject):
    outCols = {}
    for col in dictObject[0].keys():
        outCols[col] = []
    for row in dictObject:
        for col in dictObject[0].keys():
            outCols[col].append(row[col])
    return outCols

def dictColMapper(dictObject, baseCol):
    outCols = {}
    for row in dictObject:
        outCols[row[baseCol]] = {}
        for col in dictObject[0].keys():
            if col != baseCol:
                outCols[row[baseCol]][col] = row[col]
    return outCols
