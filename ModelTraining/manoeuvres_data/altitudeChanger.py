

def elevator_control(ex_list, absolute=True):
    features = ['angle_of_attack', 'pitch', 'velocity_world_y', 'velocity_body_z', 'velocity_rot_body_x', 'altitude_diff']
    new_listX = []
    new_listy = []
    for df in ex_list:
        new_listX.append(df[features])
        new_listy.append(df['elevator'] if absolute else df['elevator'].diff())
    return new_listX, new_listy

altitude_changer_controls = {
    'elevator': elevator_control,
}