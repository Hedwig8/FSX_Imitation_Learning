import zmq
import pandas as pd
import numpy as np

from loadModel import load_models
from predictProcessing import manoeuvre_predict_processing
from dataConsidered import manoeuvre_data

def pandas2numpy(X_list):
    #X_final = np.empty(shape=(0, X_list[0].shape[0], X_list[0].shape[1]), dtype=np.float32)
    return np.array([X_list[0]])

#models
manoeuvres_controls = {
    'Immelmann': ['elevator', 'aileron'],
    'SteepCurve': ['elevator', 'aileron', 'rudder'],
    'Split-S': ['elevator', 'aileron'],
    'HalfCubanEight': ['elevator', 'aileron'],
    'Climb': ['elevator'],
    'Approach': ['elevator', 'throttle'],
    
    #'TaxiRun&TakeOff': [],
    #'Landing': [],
    #'Roll': [], #aileron, elevator?
    #'CanopyRoll': [], #aileron, elevator?
    #'CubanEight': [],
    #'HammerHead': [],
    #'Tailslide': []
}

models = load_models(manoeuvres_controls)

# stored inputs
dataset = None

# server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:65432")
print("Ready to accept")

while True:
    comm_data = socket.recv_json()
    if not comm_data:
        print("not data")
        break
                    
    manoeuvre_name = comm_data['Manoeuvre']

    new_input = {key:[value] for (key,value) in comm_data['Input'].items()}
    new_df = pd.DataFrame.from_dict(new_input)
    dataset = new_df if dataset is None else pd.concat([dataset, new_df])

    outputs = {'elevator': 10, 'aileron': 10, 'rudder': 10, 'throttle': 10}
    if(len(dataset.index) > 15):
        df_16 = dataset[-16:]
        X = manoeuvre_predict_processing[manoeuvre_name](df_16, comm_data['TARGET_ALTITUDE']) 

        for surface in manoeuvres_controls[manoeuvre_name]:
            X_surface, y = manoeuvre_data[manoeuvre_name][surface]([X]) 
            X_surface = pandas2numpy(X_surface)
            
            outputs[surface] = float(models[manoeuvre_name][surface].predict(X_surface)[0][0])
    print(outputs)

    socket.send_json(outputs)