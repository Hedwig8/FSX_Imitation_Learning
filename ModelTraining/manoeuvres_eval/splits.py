from math import pi as PI, atan2, cos, sin, sqrt
import numpy as np
from skg import nsphere_fit
from visUtils import velocity_to_position, rotate_initial_heading

def std_point_to_curve(point, r, center):
    x, y = point
    xc, yc = center
    angle = atan2(y-yc, x-xc)
    x1 = r * cos(angle) + xc
    y1 = r * sin(angle) + yc
    distance = sqrt((x1-x) ** 2 + (y1-y) ** 2)
    return distance

def split_s_eval(df):
    if not {'x', 'y', 'z'}.issubset(df.columns):
        df = velocity_to_position(df)
        df = rotate_initial_heading(df)
    
    INITIAL_FINAL_HEADING_EXP_WEIGHT = 1
    INITIAL_FINAL_HEADING_WEIGHT = .6

    HEADING_DIFF_EXP_WEIGHT = 1
    HEADING_DIFF_WEIGHT = 1

    SEMI_LOOP_EXP_WEIGHT = 1
    SEMI_LOOP_WEIGHT = 1

    SEMI_ROLL_COMPLETION_EXP_WEIGHT = 1
    SEMI_ROLL_COMPLETION_WEIGHT = 1

    SEMI_ROLL_ALTITUDE_EXP_WEIGHT = 1
    SEMI_ROLL_ALTITUDE_WEIGHT = .5

     # vertical plane consistency
    # initial and final heading are references 
    heading_np = df['heading'].to_numpy()

    initial_heading = heading_np[0]
    final_heading = heading_np[-1]

    diff = (final_heading - initial_heading + PI) % (PI * 2) - PI # smaller angle
    eval_heading_initial_final = (180 - abs(diff * 180 / PI)) ** INITIAL_FINAL_HEADING_EXP_WEIGHT * INITIAL_FINAL_HEADING_WEIGHT
    
    eval_heading_diff = 0
    for heading in heading_np[5:-5]:
        initial_diff = (heading - initial_heading + PI) % (2 * PI) - PI
        
        final_diff = (heading - final_heading + PI) % (2 * PI) - PI
        
        eval_heading_diff += min(abs(initial_diff), abs(final_diff))
    eval_heading_diff = (180 * eval_heading_diff / PI / (heading_np.size-2)) ** HEADING_DIFF_EXP_WEIGHT * HEADING_DIFF_WEIGHT

    # semi-loop consistency
    # select all point whose pitch is higher than 0 (pointing downwards)
    # then fit to circunference and calculate deviations from the curve
    threshold_pitch = 0
    yz_points = np.abs(df[df['pitch'] > threshold_pitch][['y', 'z']].to_numpy())
    radius, center = nsphere_fit(yz_points)
    error = 0
    for point in yz_points:
        error += std_point_to_curve(point, radius, center)
    eval_semi_loop = (error/yz_points.size * .3048) ** SEMI_LOOP_EXP_WEIGHT * SEMI_LOOP_WEIGHT

    # semi-roll completion
    # sum all bank values of the airplane
    # when pitch is higher than 0 (pointing downwards)
    banks_in_loop = df[df['pitch'] > threshold_pitch]['bank'].to_numpy()
    eval_semi_roll_completion = 0
    for bank in banks_in_loop:
        diff_from_0 = (bank - 0 + PI) % (2 * PI) - PI
        diff_from_PI = (bank - PI + PI) % (2 * PI) - PI

        eval_semi_roll_completion += min(abs(diff_from_0), abs(diff_from_PI))

    eval_semi_roll_completion = (eval_semi_roll_completion * 180 / PI / banks_in_loop.size) ** SEMI_ROLL_COMPLETION_EXP_WEIGHT * SEMI_ROLL_COMPLETION_WEIGHT

    # semi-roll altitude consistency
    # compare all z-axis rotation velocity
    # when roll is between 2 values and higher than threshold_pitch
    threshold_roll = 0.2
    threshold_pitch_roll = 0.1
    temp_pitch = df[df['pitch'] < threshold_pitch_roll] # 
    temp_pitch_bank = temp_pitch[abs(temp_pitch['bank']) > threshold_roll]
    altitude_diff_np = np.abs(np.diff(temp_pitch_bank['altitude']))
    altitude_diff_np = altitude_diff_np[altitude_diff_np < 50]
    eval_semi_roll_altitude = np.sum(altitude_diff_np)

    eval_semi_roll_altitude = (eval_semi_roll_altitude * .3048) ** SEMI_ROLL_ALTITUDE_EXP_WEIGHT * SEMI_ROLL_ALTITUDE_WEIGHT
    
    eval = eval_heading_diff+eval_heading_initial_final+eval_semi_loop+eval_semi_roll_completion+eval_semi_roll_altitude
    return eval, {
                    'heading_initial_final': eval_heading_initial_final, 
                    'heading_diff': eval_heading_diff, 
                    'semi_loop': eval_semi_loop,
                    'semi_roll_completion': eval_semi_roll_completion,
                    'semi_roll_altitude': eval_semi_roll_altitude
                }