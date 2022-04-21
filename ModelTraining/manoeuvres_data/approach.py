
def elevator_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'velocity_world_y', 'velocity_body_z', 'velocity_rot_body_x', 'altitude_diff', 'time_diff', 'elevator', 'General_Eng_Throttle_Lever_Position_1']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'])
    return new_listX, new_listy

def throttle_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'velocity_world_y', 'velocity_body_z', 'velocity_rot_body_x', 'altitude_diff', 'time_diff', 'elevator', 'General_Eng_Throttle_Lever_Position_1']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['General_Eng_Throttle_Lever_Position_1'])
    return new_listX, new_listy

approach_controls = {
    'elevator': elevator_control,
    'throttle': throttle_control,
}