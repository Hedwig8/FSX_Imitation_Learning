import pandas as pd
from utils import csvFilePaths, saveDataFrame2CSV

inputDataset = '../AircraftDataCollector/bin/Release/'
output = './newnewDataset/'

files = csvFilePaths(inputDataset)

steps = {}

for file in files:
    datafile = pd.read_csv(file)
    size = len(datafile.index)
    step = (datafile['time'].loc[size -1] - datafile['time'].loc[0]) / (size - 1)
    step = step * 1000 if datafile['time'].loc[0] > 100000000 else step
    datafile['time'] = (datafile.index.to_series() * step).round().astype(int)
    saveDataFrame2CSV(datafile, output+file[len(inputDataset):])

    #if step < 45 or step > 65 and step < 950: print(step, " - ", file)

    steps[int(step)] = 1 if int(step) not in steps else steps[int(step)]+1

stepslist = list(steps.keys())
stepslist.sort()
for i in stepslist:
    print(i,': ', steps[i])

