import numpy as np

def default_features():
    pass

def immelmann_features(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        max_altitude = np.max(df['altitude'])
        df['altitude_diff'] = max_altitude - df['altitude']
        new_list.append(df[:-1])
    return new_list

manoeuvre_feature_calculation = {
    'Hammerhead': default_features,
    'Immelmann': immelmann_features,
}