
def elevator_control(examples_list):
    features = ['angle_of_attack', 'pitch', 'velocity_world_y', 'velocity_body_z', 'velocity_rot_body_x', 'altitude_diff', 'elevator']
    new_listX = []
    new_listy = []
    for df in examples_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'])
    return new_listX, new_listy

climb_controls = {
    'elevator': elevator_control,
}