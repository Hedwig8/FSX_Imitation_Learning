
def elevator_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'heading', 'velocity_rot_body_x', 'acc_rot_body_x', 'heading_diff']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'])
    return new_listX, new_listy

def aileron_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'heading', 'velocity_rot_body_z', 'acc_rot_body_z', 'heading_diff']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['aileron'])
    return new_listX, new_listy

def rudder_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'heading', 'velocity_rot_body_y', 'acc_rot_body_y', 'heading_diff']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['rudder'])
    return new_listX, new_listy

curve_controls = {
    'elevator': elevator_control,
    'aileron': aileron_control,
    'rudder': rudder_control
}