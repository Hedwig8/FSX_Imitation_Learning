
from math import cos, sin, sqrt, atan2

def velocity_to_position(df):
    x=0
    y=0
    z=0
    x_list=[]
    y_list=[]
    z_list=[]

    velocity = 'velocity_world_'
    last_time = -50

    for _, row in df.iterrows():
        time =  (row['time'] -last_time)/1000
        last_time = row['time']

        x += row[velocity+'x']*time
        y += row[velocity+'y']*time
        z += row[velocity+'z']*time

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
    # initial angle to rotate all points
    initial_heading = atan2(df['y'][0], df['x'][0])
    for _, row in df.iterrows():
        # find radius and angle of this point to rotate it to heading - initial_heading
        radius = sqrt(row['x'] ** 2 + row['y'] ** 2)
        heading = atan2(row['y'], row['x'])
        x_rotated.append(radius * sin(heading - initial_heading))
        y_rotated.append(radius * cos(heading - initial_heading))
    df['x'] = x_rotated
    df['y'] = y_rotated
   
    return df