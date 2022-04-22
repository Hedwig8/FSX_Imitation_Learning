from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, InputLayer, Normalization
from keras.losses import MeanSquaredError

def default_model(X_train, y_train):
    normalizer = Normalization()
    normalizer.adapt(X_train)

    model = Sequential()
    model.add(InputLayer(batch_input_shape=(None, X_train.shape[1], X_train.shape[2])))
    model.add(normalizer)
    model.add(LSTM(units=X_train.shape[1], input_shape=(None, X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(rate=0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss=MeanSquaredError())
    return model

manoeuvre_model = {
    'Approach': default_model,
    'Climb': default_model,
    'HalfCubanEight': default_model,
    'Immelmann': default_model,
    'Split-S': default_model,
    'SteepCurve': default_model
}

