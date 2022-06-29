from math import pi as PI, isnan, atan2, cos, sin, sqrt
import numpy as np
from skg import nsphere_fit
from visUtils import velocity_to_position

def std_point_to_curve(point, r, center):
    x, y = point
    xc, yc = center
    angle = atan2(y-yc, x-xc)
    x1 = r * cos(angle) + xc
    y1 = r * sin(angle) + yc
    distance = sqrt((x1-x) ** 2 + (y1-y) ** 2)
    return distance


def half_eval(df):
    df = velocity_to_position(df)

    INITIAL_FINAL_HEADING_EXP_WEIGHT = 6
    INITIAL_FINAL_HEADING_WEIGHT = 2000

    HEADING_DIFF_EXP_WEIGHT = 2
    HEADING_DIFF_WEIGHT = 2.5

    SEMI_LOOP_EXP_WEIGHT = 1.3
    SEMI_LOOP_WEIGHT = .3

    SEMI_ROLL_EXP_WEIGHT = 1
    SEMI_ROLL_WEIGHT = 120000

    SEMI_ROLL_STRAIGHT_EXP_WEIGHT = 3
    SEMI_ROLL_STRAIGHT_WEIGHT = .5

    # vertical plane consistency
    # initial and final heading are references 
    heading_np = df['heading'].to_numpy()

    initial_heading = heading_np[0]
    final_heading = heading_np[-1]

    diff = (final_heading - initial_heading + PI) % (PI * 2) - PI # smaller angle
    eval_heading_initial_final = (PI - abs(diff) + 1) ** INITIAL_FINAL_HEADING_EXP_WEIGHT * INITIAL_FINAL_HEADING_WEIGHT
    #print(initial_heading, final_heading, eval_heading_initial_final)
    
    eval_heading_diff = 0
    for heading in heading_np[5:-5]:
        initial_diff = (heading - initial_heading + PI) % (2 * PI) - PI
        
        final_diff = (heading - final_heading + PI) % (2 * PI) - PI
        
        eval_heading_diff += min(abs(initial_diff), abs(final_diff))
    eval_heading_diff = eval_heading_diff ** HEADING_DIFF_EXP_WEIGHT * HEADING_DIFF_WEIGHT

    # semi-loop consistency
    # select all point whose pitch is lower than -0.1 (pointing upwards)
    # then fit to circunference and calculate deviations from the curve
    threshold_pitch = -0.1
    yz_points = df[df['pitch'] < threshold_pitch][['y', 'z']].to_numpy()
    radius, center = nsphere_fit(yz_points)
    error = 0
    for point in yz_points:
        error += std_point_to_curve(point, radius, center)
    eval_semi_loop = error ** SEMI_LOOP_EXP_WEIGHT * SEMI_LOOP_WEIGHT

    # semi-roll consistency
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

    eval_semi_roll = overshoot ** SEMI_ROLL_EXP_WEIGHT * SEMI_ROLL_WEIGHT

    # semi-roll straight line
    # compare pitch changes when performing roll
    temp_pitch_straight = df[df['pitch'] > threshold_pitch_roll]
    temp_pitch_bank_straight = temp_pitch_straight[abs(temp_pitch_straight['bank']) > threshold_roll]
    pitch_straight = temp_pitch_bank_straight['pitch'].to_numpy()
    eval_semi_roll_straightness = np.std(pitch_straight) * pitch_straight.size
    eval_semi_roll_straightness = eval_semi_roll_straightness if not isnan(eval_semi_roll_straightness) else 500

    eval_semi_roll_straightness = eval_semi_roll_straightness ** SEMI_ROLL_STRAIGHT_EXP_WEIGHT * SEMI_ROLL_STRAIGHT_WEIGHT

    
    eval = eval_heading_diff+eval_heading_initial_final+eval_semi_loop+eval_semi_roll+eval_semi_roll_straightness
    return eval, {
                    'heading_initial_final': eval_heading_initial_final, 
                    'heading_diff': eval_heading_diff, 
                    'semi_loop': eval_semi_loop, 
                    'semi_roll_overshoot': eval_semi_roll,
                    'semi_roll_straightness': eval_semi_roll_straightness
                }
