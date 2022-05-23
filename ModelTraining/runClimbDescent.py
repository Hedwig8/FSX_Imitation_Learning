import pandas as pd
import glob
import tensorflow as tf
from sklearn.model_selection import train_test_split
import json
import time
from sklearn.preprocessing import MinMaxScaler
from joblib import dump
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, InputLayer
from keras.losses import MeanSquaredError
from keras.optimizer_v2.adam import Adam

def build_model(X_train, y_train):
    # same number as input features
    units = X_train.shape[2]

    model = Sequential()
    model.add(InputLayer(batch_input_shape=(None, X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(units=units, input_shape=(None, X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(rate=0.175)) # as found out in last years work, in hyperparameter tunning
    model.add(Dense(1))
    opt = Adam(learning_rate=0.005)
    model.compile(optimizer=opt, loss=MeanSquaredError())
    return model

def feature_calculation(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        final_altitude = df['altitude'].iloc[-1]
        df['altitude_diff'] = final_altitude - df['altitude']
        df['climb_rate'] = df['altitude'].diff().shift(-1)
        new_list.append(df[:-1])
    return new_list

def data_considered(ex_list):
    features = ['angle_of_attack', 'pitch', 'velocity_world_y', 'velocity_body_z', 'velocity_rot_body_x', 'altitude_diff']
    new_listX = []
    new_listy = []
    for df in ex_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'])
    return new_listX, new_listy

def dataset_list_2_input(X_list, y_list, window=15):
    X_final = np.empty(shape=(0, window, X_list[0].shape[1]), dtype=np.float32)
    y_final = np.empty(shape=(0))
    for X_i, X in enumerate(X_list):
        for i in range(len(X)-window-1):
            # select values from i to i+window to make one 3D input frame
            X_final = np.concatenate((X_final, np.array([X[i:i+window]])))
        # select all values from window+1, making the outputs
        y_final = np.concatenate((y_final, y_list[X_i][window+1:]))
    return X_final, y_final

dataset_path = "../ProcessedDataset"
id = "*"
manoeuvre_quality = "Good"

trained_models_path = "../TrainedModels"
trained_model_name = "AltitudeChanger"

control_surface = 'elevator'
manoeuvres = ['Climb', 'Approach']

filename_examples = glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/Climb/*_1.csv', recursive=True)
filename_examples.extend(glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/Approach/*_1.csv', recursive=True))

# list of pd.DataFrame examples
examples_list = []
for filename in filename_examples:
    examples_list.append(pd.read_csv(filename))
# separate at this stage to prevent any test data "leaked" to the training
examples_train, examples_test = train_test_split(examples_list, test_size=0.2)

# calculate features such as time_diff or altitude_diff inside each df
examples_train = feature_calculation(examples_train)
examples_test = feature_calculation(examples_test)

# returns list of chosen features for X and outputs y
X_train, y_train = data_considered(examples_train)
X_test, y_test = data_considered(examples_test)

# returns np.array of inputs, each a window of X size
X, y = dataset_list_2_input(X_train, y_train)

# apply scaler and save in file
scaler = MinMaxScaler()
original_shape_train = X.shape
reshaped_X = np.reshape(X, (-1, original_shape_train[1] * original_shape_train[2]))
scaled_X = scaler.fit_transform(reshaped_X) # reshaped because scaler only accepts 2D array
X = np.reshape(scaled_X, original_shape_train)

dump(scaler, f'{trained_models_path}/{trained_model_name}/{control_surface}.scaler')

# model
model = build_model(X, y)
callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, mode='min')

# training
history = model.fit(X, y, epochs=100, batch_size=64, validation_split=0.2, callbacks=[callback])

# test predictions
X_predict, y_true_val = dataset_list_2_input(X_test, y_test)
original_shape_test = X_predict.shape
reshaped_X_predict = np.reshape(X_predict, (-1, original_shape_test[1] * original_shape_test[2]))
scaled_X_predict = scaler.transform(reshaped_X_predict)
X_predict = np.reshape(scaled_X_predict, original_shape_test)
predictions = model.predict(X_predict)

# model training and testing data stored on file
history_dict = { f'{trained_model_name}_{control_surface}':{
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
model.save(f'{trained_models_path}/{trained_model_name}/{control_surface}')
