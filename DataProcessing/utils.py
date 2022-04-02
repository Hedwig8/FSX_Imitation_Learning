import glob
import os

def csvFilePaths(datasetPath, id='*', manoeuvreQuality='*', manoeuvreName='*', fileTermination=''):
    return glob.glob(f'{datasetPath}/{id}/{manoeuvreQuality}/{manoeuvreName}/*{fileTermination}.csv', recursive=True)

def saveDataFrame2CSV(df, filepath):
    dir, _ = os.path.split(filepath)
    if not os.path.exists(dir):
        os.makedirs(dir)
    df.to_csv(filepath, index=False)