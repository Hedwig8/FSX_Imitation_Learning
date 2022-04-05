

def default_data():
    pass

def immelmann_dataX(df):
    features = ['angle_of_attack', 'pitch', 'bank', 'velocity_world_y', 'velocity_body_z', 'altitude_diff', 'time_diff']
    return df[features].values

def immelmann_datay(df):
    return df['elevator'].values

manoeuvre_dataX = {
    'Hammerhead': default_data,
    'Immelmann': immelmann_dataX,
}

manoeuvre_datay = {
    'Immelmann': immelmann_datay,
}