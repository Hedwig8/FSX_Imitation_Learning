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

# list of pd.DataFrame examples
examples_list = []
for filename in glob.glob(f'{datasetPath}/{id}/{manouvreQuality}/{manoeuvreName}/*_1.csv', recursive=True):
    examples_list.append(pd.read_csv(filename))

# calculate features such as time_diff or altitude_diff inside each df
examples_list = manoeuvre_feature_calculation[manoeuvreName](examples_list)

# returns list of chosen features for X and outputs y
X_list = manoeuvre_dataX[manoeuvreName](examples_list)
y_list = manoeuvre_datay[manoeuvreName](examples_list)
print('dataX and y, before 2input')
# returns np.array of inputs, each a window of X size
X, y = manoeuvre_dataset_2_Xinput[manoeuvreName](X_list, y_list)

model = manoeuvre_model[manoeuvreName](X.shape[1], X.shape[2], y.shape[0])
model.fit(X, y, epochs=100)