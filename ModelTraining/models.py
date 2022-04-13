from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, InputLayer
from keras.losses import MeanSquaredError

def default_model(shapeX1, shapeX2, shapey):
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(None, shapeX1, shapeX2)))
    model.add(LSTM(units=shapeX1, input_shape=(None, shapeX1, shapeX2)))
    model.add(Dropout(rate=0.3))
    model.add(Dense(shapey))
    model.compile(optimizer='adam', loss=MeanSquaredError())
    return model

manoeuvre_model = {
    'Immelmann': default_model,
    'SteepCurve': default_model
}

