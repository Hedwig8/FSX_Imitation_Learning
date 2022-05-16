
def default_features():
    pass

def half_cuban_eight_features(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1) * 1000 # s -> ms
        max_altitude = max(df['altitude'])
        df['max_altitude_diff'] = max_altitude - df['altitude']
        final_altitude = df['altitude'].iloc[-1]
        df['final_altitude_diff'] = final_altitude - df['altitude']
        new_list.append(df[:-1])
    return new_list

def max_altitude_features(df, max_altitude):
    df['time_diff'] = df['time'].diff().shift(-1)
    df['altitude_diff'] = max_altitude - df['altitude']
    return df[:-1]

def min_altitude_features(df, min_altitude):
    df['time_diff'] = df['time'].diff().shift(-1)
    df['altitude_diff'] = df['altitude'] - min_altitude
    return df[:-1]

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

manoeuvre_predict_processing = {
    'Approach': max_altitude_features, # OK - it was min-altitude
    'Climb': max_altitude_features, # OK
    'HalfCubanEight': half_cuban_eight_features,
    'Immelmann': max_altitude_features, # OK
    'Split-S': min_altitude_features, # OK - it was altitude-min
    'SteepCurve': curve_features,
}