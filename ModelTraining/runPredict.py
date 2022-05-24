import zmq
import pandas as pd
import numpy as np

from loadModel import load_models, load_scalers
from predictProcessing import manoeuvre_predict_processing
from dataConsidered import manoeuvre_data
from dataset2input import manoeuvre_window_size

def pandas2numpy(X_list, manoeuvre):
    if manoeuvre == 'Climb' or manoeuvre == 'SteepCurve':
        return np.array(X_list[0])
    return np.array([X_list[0]])

#models
manoeuvres_controls = {
    #'Immelmann': ['elevator', 'aileron'],
    'SteepCurve': ['elevator', 'aileron', 'rudder'],
    #'Split-S': ['elevator', 'aileron'],
    #'HalfCubanEight': ['elevator', 'aileron'],
    'Climb': ['elevator'],
    #'Approach': ['elevator', 'throttle'],
    #'AltitudeChanger': ['elevator'],
    
    #'TaxiRun&TakeOff': [],
    #'Landing': [],
    #'Roll': [], #aileron, elevator?
    #'CanopyRoll': [], #aileron, elevator?
    #'CubanEight': [],
    #'HammerHead': [],
    #'Tailslide': []
}

models = load_models(manoeuvres_controls)
scalers = load_scalers(manoeuvres_controls)

# stored inputs
dataset = None

# server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:65432")
print("Ready to accept")

while True:
    comm_data = socket.recv_json() # block execution, program needs too be shut down with task manager
    if not comm_data:
        print("not data")
        break
    manoeuvre_name = comm_data['Manoeuvre']
    for dataframe in comm_data['Input']:
        new_input = {key:[value] for (key,value) in dataframe.items()}
        new_df = pd.DataFrame.from_dict(new_input)
        dataset = pd.concat([dataset, new_df], ignore_index=True)

    outputs = {'elevator': 10, 'aileron': 10, 'rudder': 10, 'throttle': 10}
    window_size = manoeuvre_window_size[manoeuvre_name]
    if(len(dataset.index) > window_size):
        df_window = dataset[-window_size-1:].copy()

        X = [] # different parameters and parameters number
        if manoeuvre_name == 'SteepCurve':
            X = manoeuvre_predict_processing[manoeuvre_name](df_window, comm_data['TARGET_HEADING'])
        elif manoeuvre_name == 'HalfCubanEight':
            X = manoeuvre_predict_processing[manoeuvre_name](df_window, comm_data['TARGET_ALTITUDE'], comm_data['TARGET_MAX_ALTITUDE'])
        else:
            X = manoeuvre_predict_processing[manoeuvre_name](df_window, comm_data['TARGET_ALTITUDE']) 

        for surface in manoeuvres_controls[manoeuvre_name]:
            X_surface, y = manoeuvre_data[manoeuvre_name][surface]([X]) 
            X_surface = pandas2numpy(X_surface, manoeuvre=manoeuvre_name)

            # apply reshape to scale the data
            reshaped_X = X_surface
            original_shape = X_surface.shape
            if len(original_shape) == 3:
                reshaped_X = np.reshape(X_surface, (-1, original_shape[1] * original_shape[2]))
            scaled_X = scalers[manoeuvre_name][surface].transform(reshaped_X)
            if len(original_shape) == 3:
                scaled_X = np.reshape(scaled_X, original_shape)

            outputs[surface] = float(models[manoeuvre_name][surface].predict(scaled_X)[0][0])
    print(outputs)

    socket.send_json(outputs)