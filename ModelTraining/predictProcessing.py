from math import pi as PI


def default_features():
    pass

def climb_features(df, climb_rate):
    df['time_diff'] = df['time'].diff() * 1000 # s -> ms
    df['climb_rate'] = climb_rate
    return df[1:]

def half_cuban_eight_features(df, final_altitude, max_altitude):
    df['time_diff'] = df['time'].diff() * 1000 # s -> ms
    df['max_altitude_diff'] = max_altitude - df['altitude']
    df['final_altitude_diff'] = final_altitude - df['altitude']
    return df[1:]

def max_altitude_features(df, max_altitude):
    df['time_diff'] = df['time'].diff() * 1000 # s -> ms
    df['altitude_diff'] = max_altitude - df['altitude']
    return df[1:]

def min_altitude_features(df, min_altitude):
    df['time_diff'] = df['time'].diff() * 1000 # s -> ms
    df['altitude_diff'] = df['altitude'] - min_altitude
    return df[1:]

def curve_features(df, rotation, initial_heading):
    df['time_diff'] = df['time'].diff() * 1000 # s -> ms
    df['acc_rot_body_x'] = df['velocity_rot_body_x'].diff()
    df['acc_rot_body_y'] = df['velocity_rot_body_y'].diff()
    df['acc_rot_body_z'] = df['velocity_rot_body_z'].diff()

    final_heading = (initial_heading + rotation) % (2 * PI)
    heading_diff = []
    for heading in df['heading']:
        diff = final_heading - heading 
        heading_diff.append((diff + PI) % (2*PI) - PI)
    df['heading_diff'] = heading_diff

    return df[1:]

def roll_features(df, _):
    df['time_diff'] = df['time'].diff() * 1000 # s -> ms

    return df[1:]

manoeuvre_predict_processing = {
    'Approach': max_altitude_features, # OK - it was trained with min-altitude
    'Climb': max_altitude_features, # OK
    'HalfCubanEight': half_cuban_eight_features,
    'Immelmann': max_altitude_features, # OK
    'Split-S': min_altitude_features, # OK - it was trained with altitude-min
    'SteepCurve': curve_features,
    'AltitudeChanger': max_altitude_features,

    'Roll': roll_features,
    'CanopyRoll': roll_features,
}