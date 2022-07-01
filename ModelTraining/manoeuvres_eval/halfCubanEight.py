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


def half_eval(df):
    if not {'x', 'y', 'z'}.issubset(df.columns):
        df = velocity_to_position(df)
        df = rotate_initial_heading(df)
    
    INITIAL_FINAL_HEADING_EXP_WEIGHT = 1
    INITIAL_FINAL_HEADING_WEIGHT = 1

    HEADING_DIFF_EXP_WEIGHT = 1
    HEADING_DIFF_WEIGHT = 1

    SEMI_LOOP_EXP_WEIGHT = 1
    SEMI_LOOP_WEIGHT = 1

    SEMI_ROLL_EXP_WEIGHT = 1
    SEMI_ROLL_WEIGHT = 1

    SEMI_ROLL_STRAIGHT_EXP_WEIGHT = 2
    SEMI_ROLL_STRAIGHT_WEIGHT = .05

    # vertical plane consistency
    # initial and final heading are references 
    heading_np = df['heading'].to_numpy()

    initial_heading = heading_np[0]
    final_heading = heading_np[-1]

    diff = (final_heading - initial_heading + PI) % (PI * 2) - PI # smaller angle
    eval_heading_initial_final = (180 - abs(diff * 180 / PI)) ** INITIAL_FINAL_HEADING_EXP_WEIGHT * INITIAL_FINAL_HEADING_WEIGHT
    
    eval_heading_diff = 0
    for heading in heading_np[1:-1]:
        initial_diff = (heading - initial_heading + PI) % (2 * PI) - PI
        
        final_diff = (heading - final_heading + PI) % (2 * PI) - PI
        
        eval_heading_diff += min(abs(initial_diff), abs(final_diff))
    eval_heading_diff = (180 * eval_heading_diff / PI / (heading_np.size-2)) ** HEADING_DIFF_EXP_WEIGHT * HEADING_DIFF_WEIGHT

    # semi-loop consistency
    # select all point whose pitch is lower than -0.1 (pointing upwards)
    # then fit to circunference and calculate deviations from the curve
    threshold_pitch = -0.1
    yz_points = df[df['pitch'] < threshold_pitch][['y', 'z']].to_numpy()
    radius, center = nsphere_fit(yz_points)
    error = 0
    for point in yz_points:
        error += std_point_to_curve(point, radius, center)
    eval_semi_loop = (error / yz_points.size * 0.3048) ** SEMI_LOOP_EXP_WEIGHT * SEMI_LOOP_WEIGHT

    # semi-roll overshoot
    # analyse the evolution of bank values, looking for sign changes
    # when roll is between 2 values and higher than threshold_pitch
    threshold_roll = 0.2
    threshold_pitch_roll = -0.3
    temp_pitch = df[df['pitch'] > threshold_pitch_roll] # 
    temp_pitch_bank = temp_pitch[abs(temp_pitch['bank']) > threshold_roll]
    bank_np = temp_pitch_bank['bank'].to_numpy()
    overshoot = 0
    for i in range(bank_np.size - 1):
        mul = bank_np[i] * bank_np[i+1] # if mul<0, went from + -> - or viceversa
        if mul < 0 and mul > -0.6: # difference from angles smaller than ~PI/4
            overshoot = np.sum(np.abs(np.diff(bank_np[i:])))
            break

    eval_semi_roll = (overshoot * 180 / PI / 2) ** SEMI_ROLL_EXP_WEIGHT * SEMI_ROLL_WEIGHT

    # semi-roll straight line
    # compare pitch changes when performing roll
    temp_pitch_straight = df[df['pitch'] > threshold_pitch_roll]
    temp_pitch_bank_straight = temp_pitch_straight[abs(temp_pitch_straight['bank']) > threshold_roll]
    pitch_straight = temp_pitch_bank_straight['pitch'].to_numpy()
    eval_semi_roll_straightness = np.std(pitch_straight) # TODO rethink this

    eval_semi_roll_straightness = (eval_semi_roll_straightness * 180 / PI) ** SEMI_ROLL_STRAIGHT_EXP_WEIGHT * SEMI_ROLL_STRAIGHT_WEIGHT

    eval = eval_heading_diff+eval_heading_initial_final+eval_semi_loop+eval_semi_roll+eval_semi_roll_straightness
    return eval, {
                    'heading_initial_final': eval_heading_initial_final, 
                    'heading_diff': eval_heading_diff, 
                    'semi_loop': eval_semi_loop, 
                    'semi_roll_overshoot': eval_semi_roll,
                    'semi_roll_straightness': eval_semi_roll_straightness
                }
