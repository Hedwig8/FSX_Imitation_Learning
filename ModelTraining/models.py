from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, InputLayer
from keras.losses import MeanSquaredError
from keras.optimizer_v2.adam import Adam

def default_LSTM_model(X_train, y_train):
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

def basic_NN_model(X_train, y_train):
    model = Sequential()
    model.add(InputLayer(input_shape=(X_train.shape[1])))
    model.add(Dense(X_train.shape[1]))
    model.add(Dense(1))
    opt = Adam(learning_rate=0.002)
    model.compile(optimizer=opt, loss=MeanSquaredError())
    return model

manoeuvre_model = {
    'Approach': default_LSTM_model,
    'Climb': basic_NN_model,
    'HalfCubanEight': default_LSTM_model,
    'Immelmann': default_LSTM_model,
    'Split-S': default_LSTM_model,
    'SteepCurve': default_LSTM_model,

    'Roll': default_LSTM_model,
    'CanopyRoll': default_LSTM_model,
}

