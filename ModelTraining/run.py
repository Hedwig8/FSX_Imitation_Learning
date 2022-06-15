import pandas as pd
import glob
import tensorflow as tf
from sklearn.model_selection import train_test_split
import json
import time
from sklearn.preprocessing import MinMaxScaler
from joblib import dump
import numpy as np

from featureCalculation import manoeuvre_feature_calculation
from dataConsidered import manoeuvre_data
from models import manoeuvre_model
from dataset2input import manoeuvre_dataset_2_input, manoeuvre_window_size

from evaluation import manoeuvre_evaluation

dataset_path = "../ProcessedDataset"
id = "*"
manoeuvre_quality = "Good"

trained_models_path = "../TrainedModels"

# combinations of manoeuvers and control surfaces
manoeuvres_controls = {
    #'Immelmann': ['elevator', 'aileron'],
    #'Split-S': ['elevator', 'aileron'],
    #'HalfCubanEight': ['elevator', 'aileron'],
    'Climb': ['elevator'],
    'Approach': ['elevator', 'throttle'],
    
    'SteepCurve': ['elevator', 'aileron', 'rudder'],
    #'SteepCurve': ['rudder'],

    'Roll': [ 'aileron', 'elevator'],
    'CanopyRoll': [ 'aileron', 'elevator'],

    #'TaxiRun&TakeOff': [],
    #'Landing': [],
    #'CubanEight': [],
    #'HammerHead': [],
    #'Tailslide': []
}
                
def absolute_file_name(absolute):
    return 'absolute' if absolute else 'relative'

evaluation_thresholds = [1, 0.9, 0.75, 0.6]
absolute_output = [True,]# False]

start_time = time.time()

# load of all examples from manoeuvre_name 
for manoeuvre_name, controls in manoeuvres_controls.items():
    # list of pd.DataFrame examples
    examples_eval_list = []
    for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
        df = pd.read_csv(filename)
        examples_eval_list.append((df, manoeuvre_evaluation[manoeuvre_name](df)))

    for eval_threshold in evaluation_thresholds:

        sorted_examples_eval_list = sorted(examples_eval_list, key=lambda x: x[1])
        threshold = round(len(sorted_examples_eval_list) * eval_threshold)

        filtered_examples_list = [x[0] for x in sorted_examples_eval_list[0:threshold]]

        for absolute in absolute_output:
            # separate at this stage to prevent any test data "leaked" to the training
            examples_train, examples_test = train_test_split(filtered_examples_list, test_size=0.2)

            # calculate features such as time_diff or altitude_diff inside each df
            examples_train = manoeuvre_feature_calculation[manoeuvre_name](examples_train)
            examples_test = manoeuvre_feature_calculation[manoeuvre_name](examples_test)
            
            for control_surface in controls:
                # returns list of chosen features for X and outputs y
                X_train, y_train = manoeuvre_data[manoeuvre_name][control_surface](examples_train, absolute)
                X_test, y_test = manoeuvre_data[manoeuvre_name][control_surface](examples_test, absolute)

                # returns np.array of inputs, each a window of X size
                X, y = manoeuvre_dataset_2_input[manoeuvre_name](X_train, y_train, manoeuvre_window_size[manoeuvre_name])

                # apply scaler and save in file
                scaler = MinMaxScaler()
                reshaped_X = X
                original_shape_train = X.shape
                if len(original_shape_train) == 3:
                    reshaped_X = np.reshape(X, (-1, original_shape_train[1] * original_shape_train[2])) # reshaped because scaler only accepts 2D array
                scaled_X = scaler.fit_transform(reshaped_X)
                if len(original_shape_train) == 3:
                    scaled_X = np.reshape(scaled_X, original_shape_train)

                dump(scaler, f'{trained_models_path}/{manoeuvre_name}/{absolute_file_name(absolute)}/threshold-{eval_threshold}/{control_surface}.scaler')

                # model
                model = manoeuvre_model[manoeuvre_name](scaled_X, y)
                callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, mode='min')

                # training
                history = model.fit(scaled_X, y, epochs=100, batch_size=64, validation_split=0.2, callbacks=[callback])

                # test predictions
                X_predict, y_true_val = manoeuvre_dataset_2_input[manoeuvre_name](X_test, y_test, manoeuvre_window_size[manoeuvre_name])
                reshaped_X_predict = X_predict
                original_shape_test = X_predict.shape
                if len(original_shape_test) == 3:
                    reshaped_X_predict = np.reshape(X_predict, (-1, original_shape_test[1] * original_shape_test[2]))
                scaled_X_predict = scaler.transform(reshaped_X_predict)
                if len(original_shape_test) == 3:
                    scaled_X_predict = np.reshape(scaled_X_predict, original_shape_test)
                predictions = model.predict(scaled_X_predict)

                # model training and testing data stored on file
                history_dict = { f'{manoeuvre_name}_{absolute_file_name(absolute)}_threshold-{eval_threshold}_{control_surface}':{
                                    'history': history.history, 
                                    'predictions': predictions.flatten().tolist(), 
                                    'true_value': y_true_val.tolist(),}
                                }
            
                history_from_file = {}
                try:
                    # read contents
                    with open(f'{trained_models_path}/history.json', 'r') as file:
                        history_from_file = json.load(file)
                except:
                    pass
                finally:
                    # re-write with new dict addition
                    with open(f'{trained_models_path}/history.json', "w") as file:
                        history_to_store = {**history_from_file, **history_dict}
                        json.dump(history_to_store, file)

                model.save(f'{trained_models_path}/{manoeuvre_name}/{absolute_file_name(absolute)}/threshold-{eval_threshold}/{control_surface}')

print(f'------- Execution time: {time.time() - start_time} seconds -----------')
