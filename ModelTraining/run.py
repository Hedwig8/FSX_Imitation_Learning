import pandas as pd
import glob
import tensorflow as tf

from featureCalculation import manoeuvre_feature_calculation
from dataConsidered import manoeuvre_data
from models import manoeuvre_model
from dataset2Xinput import manoeuvre_dataset_2_Xinput

dataset_path = "../dataset"
id = "*"
manoeuvre_quality = "Good"

# combinations of manoeuvers and control surfaces
manoeuvres_controls = {
    'Immelmann': ['elevator', 'aileron'],
    'SteepCurve': ['elevator', 'aileron', 'rudder'],
    'Split-S': ['elevator', 'aileron'],
    'HalfCubanEight': ['elevator', 'aileron'],
    'Climb': ['elevator'],
    'Approach': ['elevator', 'throttle'],
    
    'TaxiRun&TakeOff': [],
    'Landing': [],
    'Roll': [], #aileron, elevator?
    'CanopyRoll': [], #aileron, elevator?
    'CubanEight': [],
    'HammerHead': [],
    'Tailslide': []
}

# load of all examples from manoeuvre_name 
for manoeuvre_name, value in manoeuvres_controls.items():
    # list of pd.DataFrame examples
    examples_list = []
    for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
        examples_list.append(pd.read_csv(filename))

    # calculate features such as time_diff or altitude_diff inside each df
    examples_list = manoeuvre_feature_calculation[manoeuvre_name](examples_list)
    
    for control_surface in value:
        # returns list of chosen features for X and outputs y
        X_list, y_list = manoeuvre_data[manoeuvre_name][control_surface](examples_list)
        
        # returns np.array of inputs, each a window of X size
        X, y = manoeuvre_dataset_2_Xinput[manoeuvre_name](X_list, y_list)

        model = manoeuvre_model[manoeuvre_name](X, y)
        callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3, mode='min')
        model.fit(X, y, epochs=100, callbacks=[callback])
        model.save(f'trained/{manoeuvre_name}/{control_surface}')