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

def curve_features(ex_list):
    new_list=[]
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        # heading delta calculation
        # start from the last timeframe to the beginning
        # accounting for all edge cases
        # like turns over 180 degrees, or 360 degrees
        last_heading = df['heading'][len(df.index)-1]
        accumulated_heading_diff = 0
        heading_diff = []
        for i in reversed(df.index):
            accumulated_heading_diff += last_heading - df['heading'][i]
            heading_diff.append(accumulated_heading_diff)
            last_heading = df['heading'][i]
        heading_diff.reverse()
        df['heading_diff'] = heading_diff
        new_list.append(df[:-1])
    return new_list

manoeuvre_feature_calculation = {
    'Immelmann': immelmann_features,
    'SteepCurve': curve_features,
}