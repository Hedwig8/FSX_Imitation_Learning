
def elevator_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'heading', 'velocity_world_y', 'velocity_body_z', 'velocity_body_x', 'velocity_rot_body_z', 'velocity_rot_body_x', 'time_diff', 'elevator', 'aileron', 'rudder']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'])
    return new_listX, new_listy

def aileron_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'heading', 'velocity_world_y', 'velocity_body_z', 'velocity_body_x', 'velocity_rot_body_z', 'velocity_rot_body_x', 'time_diff', 'elevator', 'aileron', 'rudder']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['aileron'])
    return new_listX, new_listy

def rudder_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'heading', 'velocity_world_y', 'velocity_body_z', 'velocity_body_x', 'velocity_rot_body_z', 'velocity_rot_body_x', 'time_diff', 'elevator', 'aileron', 'rudder']
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