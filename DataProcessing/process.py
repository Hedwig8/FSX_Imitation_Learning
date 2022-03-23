import pandas as pd
import os
import glob

datasetPath = "../"
manoeuvrePath = "DataProcessing"
df = pd.DataFrame()

for filename in glob.glob(f'{datasetPath}{manoeuvrePath}**/*.txt', recursive=True):
    print(filename)
    #with open(os.path.join(datasetPath, filename), 'r') as f:
        #do stuff
        #pass


