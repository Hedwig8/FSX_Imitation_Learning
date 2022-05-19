
def elevator_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'velocity_world_y', 'velocity_body_z']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'])
    return new_listX, new_listy

def aileron_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'bank', 'velocity_rot_body_y', 'elevator']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['aileron'])
    return new_listX, new_listy

half_cuban_eight_controls = {
    'elevator': elevator_control,
    'aileron': aileron_control,
}