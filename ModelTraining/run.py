import pandas as pd
import glob

from featureCalculation import manoeuvre_feature_calculation
from dataConsidered import manoeuvre_dataX, manoeuvre_datay
from models import manoeuvre_model
from dataset2Xinput import manoeuvre_dataset_2_Xinput

datasetPath = "../AircraftDataCollector/bin/Release"
id = "*"
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

X, y = manoeuvre_dataset_2_Xinput[manoeuvreName](X, y)

model = manoeuvre_model[manoeuvreName](X.shape[1], X.shape[2], y.shape[0])
model.fit(X, y, epochs=100)