
def elevator_control(examples_list, absolute=True):
    features = ['angle_of_attack', 'pitch', 'velocity_body_z', 'velocity_rot_body_x', 'altitude_diff', ]
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'] if absolute else df['elevator'].diff())
    return new_listX, new_listy

def throttle_control(examples_list, absolute=True):
    features = ['angle_of_attack', 'pitch', 'velocity_body_z', 'velocity_rot_body_x', 'altitude_diff', ]
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['General_Eng_Throttle_Lever_Position_1'] if absolute 
                            else df['General_Eng_Throttle_Lever_Position_1'].diff())
    return new_listX, new_listy

approach_controls = {
    'elevator': elevator_control,
    'throttle': throttle_control,
}