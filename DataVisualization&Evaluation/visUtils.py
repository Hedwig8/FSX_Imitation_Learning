
from math import cos, sin, sqrt, atan2
from scipy.spatial.transform import Rotation as R

def velocity_to_position(df):
    x=0
    y=0
    z=0
    x_list=[]
    y_list=[]
    z_list=[]

    rx = 0
    ry = 0
    rz = 0
    rx_list = 0
    ry_list = 0
    rz_list = 0

    velocity = 'velocity_world_'
    last_time = -50
    initial_altitude = df['altitude'][0]

    for _, row in df.iterrows():
        time =  (row['time'] -last_time)/1000
        last_time = row['time']
        # rx += row['velocity_rot_body_x']*time
        # ry += row['velocity_rot_body_y']*time
        # rz += row['velocity_rot_body_z']*time

        vx = row[velocity+'x']*time
        vy = row[velocity+'y']*time
        #vy = row['altitude'] - initial_altitude
        vz = row[velocity+'z']*time

        # r = R.from_rotvec([rx, ry, rz])
        # v = r.apply([vx, vy, vz])

        x += vx
        y += vy
        z += vz
        x_list.append(z)
        y_list.append(x)
        z_list.append(y)

    df['x'] = x_list
    df['y'] = y_list
    df['z'] = z_list
    
    return df

def rotate_initial_heading(df):
    x_rotated = []
    y_rotated = []
    angle = atan2(df['y'][0], df['x'][0])
    for _, row in df.iterrows():
        radius = sqrt(row['x'] ** 2 + row['y'] ** 2)
        heading = atan2(row['y'], row['x'])
        x_rotated.append(radius * sin(heading - angle))
        y_rotated.append(radius * cos(heading - angle))
    df['x'] = x_rotated
    df['y'] = y_rotated
   
    return df