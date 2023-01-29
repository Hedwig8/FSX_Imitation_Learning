import pandas as pd
from utils import csvFilePaths, saveDataFrame2CSV

inputDataset = '../ProcessedDataset'
output = '../dataset'

files = csvFilePaths(inputDataset)

def convertN2L(num):
    return 'A' if num == '1' else 'E'

for file in files:
    _, id_session, quality, manoeuvre, name = file.split('\\')
    id_session = id_session.split('_')
    id =  id_session[0]
    if len(id_session) == 1:
        session = '01'
    else: session = id_session[1]
    df = pd.read_csv(file)
    saveDataFrame2CSV(df, f'{output}/{manoeuvre}/{name[:-6]}_{convertN2L(name[-5:-4])}_{id}_{session}_{quality}.csv')