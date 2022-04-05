import numpy as np

def default_features():
    pass

def immelmann_features(df):
    df['time_diff'] = df['time'].diff().shift(-1)
    max_altitude = np.max(df['altitude'])
    df['altitude_diff'] = max_altitude - df['altitude']
    df = df[:-1]
    return df

manoeuvre_feature_calculation = {
    'Hammerhead': default_features,
    'Immelmann': immelmann_features,
}