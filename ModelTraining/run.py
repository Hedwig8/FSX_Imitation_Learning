import pandas as pd
import glob

from featureCalculation import manoeuvre_feature_calculation
from dataConsidered import manoeuvre_dataX, manoeuvre_datay
from models import manoeuvre_model

datasetPath = "../DataProcessing/newnewDataset"
id = "01_02"
manouvreQuality = "Good"
manoeuvreName = "Immelmann"
manoeuvres = ['TaxiRun&TakeOff', 'Climb', 'Approach', 'Landing', 
                'Roll', 'SteepCurve', 'CubanEight', 'HalfCubanEight', 
                'Immelmann', 'Split-S', 'Hammerhead', 'Tailslide', 'CanopyRoll']

df = pd.DataFrame()

for filename in glob.glob(f'{datasetPath}/{id}/{manouvreQuality}/{manoeuvreName}/*_1.csv', recursive=True):
    df = pd.concat([df, pd.read_csv(filename)], ignore_index=True)

df = manoeuvre_feature_calculation[manoeuvreName](df)
X = manoeuvre_dataX[manoeuvreName](df)
y = manoeuvre_datay[manoeuvreName](df)

print(X)
model = manoeuvre_model[manoeuvreName](X, y)
