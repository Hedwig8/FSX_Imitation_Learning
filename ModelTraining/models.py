from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, InputLayer


def default_model():
    pass

def immelmann_model(shapeX1, shapeX2, shapey):
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(None, shapeX1, shapeX2)))
    model.add(LSTM(units=shapeX1, input_shape=(None, shapeX1, shapeX2)))
    model.add(Dropout(rate=0.3))
    model.add(Dense(shapey))
    model.compile(optimizer='adam', loss='mean_square_error')
    return model

manoeuvre_model = {
    'Hammerhead': default_model,
    'Immelmann': immelmann_model,
}

