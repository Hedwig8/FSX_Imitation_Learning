import pandas as pd
import glob

import processing

datasetPath = "dataset"
id = "*"
manouvreQuality = "Good"
manoeuvreName = "Immelmann"
manoeuvres = ['TaxiRun&TakeOff', 'Climb', 'Approach', 'Landing', 
                'Roll', 'SteepCurve', 'CubanEight', 'HalfCubanEight', 
                'Immelmann', 'Split-S', 'Hammerhead', 'Tailslide', 'CanopyRoll']

df = pd.DataFrame()

for filename in glob.glob(f'{datasetPath}/{id}/{manouvreQuality}/{manoeuvreName}/*_1.csv', recursive=True):
    dfs = processing.manoeuvre_processing[manoeuvreName](pd.read_csv(filename))
    
    print(dfs.head)
    break
    #with open(os.path.join(datasetPath, filename), 'r') as f:
        #do stuff
        #pass


