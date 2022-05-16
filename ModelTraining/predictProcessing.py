
def default_features():
    pass

def half_cuban_eight_features(df, final_altitude, max_altitude):
    df['time_diff'] = df['time'].diff().shift(-1) * 1000 # s -> ms
    df['max_altitude_diff'] = max_altitude - df['altitude']
    df['final_altitude_diff'] = final_altitude - df['altitude']
    return df[:-1]

def max_altitude_features(df, max_altitude):
    df['time_diff'] = df['time'].diff().shift(-1) * 1000 # s -> ms
    df['altitude_diff'] = max_altitude - df['altitude']
    return df[:-1]

def min_altitude_features(df, min_altitude):
    df['time_diff'] = df['time'].diff().shift(-1) * 1000 # s -> ms
    df['altitude_diff'] = df['altitude'] - min_altitude
    return df[:-1]

def curve_features(df, final_heading):
    df['time_diff'] = df['time'].diff().shift(-1) * 1000 # s -> ms
    heading_diff = []
    for heading in df['heading']:
        diff = final_heading - heading
        heading_diff.append(diff + 360 if diff < -180 else diff - 360 if diff > 180 else diff)
    df['heading_diff'] = heading_diff
    return df[:-1]

manoeuvre_predict_processing = {
    'Approach': max_altitude_features, # OK - it was min-altitude
    'Climb': max_altitude_features, # OK
    'HalfCubanEight': half_cuban_eight_features,
    'Immelmann': max_altitude_features, # OK
    'Split-S': min_altitude_features, # OK - it was altitude-min
    'SteepCurve': curve_features,
}