
def default_features():
    pass

def approach_features(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        min_altitude = min(df['altitude'])
        df['altitude_diff'] = min_altitude - df['altitude']
        new_list.append(df[:-1])
    return new_list

def climb_features(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        max_altitude = max(df['altitude'])
        df['altitude_diff'] = max_altitude - df['altitude']
        new_list.append(df[:-1])
    return new_list

def half_cuban_eight_features(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        max_altitude = max(df['altitude'])
        df['max_altitude_diff'] = max_altitude - df['altitude']
        final_altitude = df['altitude'].iloc[-1]
        df['final_altitude_diff'] = final_altitude - df['altitude']
        new_list.append(df[:-1])
    return new_list

def immelmann_features(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        final_altitude = df['altitude'].loc[-1]
        df['altitude_diff'] = final_altitude - df['altitude']
        new_list.append(df[:-1])
    return new_list

def split_s_features(ex_list):
    new_list = []
    for df in ex_list:
        df['time_diff'] = df['time'].diff().shift(-1)
        final_altitude = df['altitude'].iloc[-1]
        df['altitude_diff'] = df['altitude'] - final_altitude
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
            diff = last_heading - df['heading'][i]
            accumulated_heading_diff += diff + 360 if diff < -180 else diff - 360 if diff > 180 else diff
            heading_diff.append(accumulated_heading_diff)
            last_heading = df['heading'][i]
        heading_diff.reverse()
        df['heading_diff'] = heading_diff
        new_list.append(df[:-1])
    return new_list

manoeuvre_feature_calculation = {
    'Approach': approach_features,
    'Climb': climb_features,
    'HalfCubanEight': half_cuban_eight_features,
    'Immelmann': immelmann_features,
    'Split-S': split_s_features,
    'SteepCurve': curve_features,
}