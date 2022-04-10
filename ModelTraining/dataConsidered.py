

def default_data():
    pass

def immelmann_dataX(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'velocity_world_y', 'velocity_body_z', 'altitude_diff', 'time_diff', 'elevator']
    new_list = []
    for df in examples_list:
        new_list.append(df[features])
    return new_list

def immelmann_datay(examples_list):
    new_list = []
    for df in examples_list:
        new_list.append(df['elevator'])
    return new_list

manoeuvre_dataX = {
    'Hammerhead': default_data,
    'Immelmann': immelmann_dataX,
}

manoeuvre_datay = {
    'Immelmann': immelmann_datay,
}