from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, InputLayer
from keras.losses import MeanSquaredError
from keras.optimizer_v2.adam import Adam

def default_model(X_train, y_train):
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

manoeuvre_model = {
    'Approach': default_model,
    'Climb': default_model,
    'HalfCubanEight': default_model,
    'Immelmann': default_model,
    'Split-S': default_model,
    'SteepCurve': default_model
}

