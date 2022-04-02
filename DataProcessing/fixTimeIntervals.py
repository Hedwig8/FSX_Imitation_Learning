import pandas as pd
from utils import csvFilePaths, saveDataFrame2CSV

inputDataset = '../AircraftDataCollector/bin/Release/'
output = './newDataset/'

files = csvFilePaths(inputDataset)

for file in files:
    datafile = pd.read_csv(file)
    size = len(datafile.index)
    step = (datafile['time'].loc[size -1] - datafile['time'].loc[0]) / (size - 1)
    datafile['time'] = (datafile.index.to_series() * step).round().astype(int)
    saveDataFrame2CSV(datafile, output+file[len(inputDataset):])

