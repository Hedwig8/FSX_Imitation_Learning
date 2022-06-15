

def elevator_control(examples_list, absolute=True):
    features = ['angle_of_attack', 'pitch', 'bank', 'velocity_rot_body_z', 'aileron' ]
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'] if absolute else df['elevator'].diff())
    return new_listX, new_listy

def aileron_control(examples_list, absolute=True):
    features = ['angle_of_attack', 'pitch', 'bank', 'velocity_rot_body_z', 'elevator']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['aileron'] if absolute else df['aileron'].diff())
    return new_listX, new_listy

roll_controls = {
    'elevator': elevator_control,
    'aileron': aileron_control,
}