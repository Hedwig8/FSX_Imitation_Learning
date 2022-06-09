from math import pi as PI, isnan
import numpy as np

def immelmann_eval(df):
    INITIAL_FINAL_HEADING_EXP_WEIGHT = 10
    INITIAL_FINAL_HEADING_WEIGHT = 100

    HEADING_DIFF_EXP_WEIGHT = 2.5
    HEADING_DIFF_WEIGHT = 1

    SEMI_LOOP_EXP_WEIGHT = 2.3
    SEMI_LOOP_WEIGHT = 1

    SEMI_ROLL_EXP_WEIGHT = 2
    SEMI_ROLL_WEIGHT = 1

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
    # compare all x-axis rotation velocity
    # when pitch is lower than -0.1 (pointing upwards)
    threshold_pitch = -0.1
    rot_vel_x = np.abs(df[df['pitch'] < threshold_pitch]['velocity_rot_body_x'].to_numpy())

    eval_semi_loop = np.std(rot_vel_x) * rot_vel_x.size ** SEMI_LOOP_EXP_WEIGHT * SEMI_LOOP_WEIGHT

    # semi-roll consistency
    # compare all z-axis rotation velocity
    # when roll is between 2 values and higher than threshold_pitch
    threshold_roll = 0.2
    threshold_pitch_roll = -0.3
    temp_pitch = df[df['pitch'] > threshold_pitch_roll] # 
    temp_pitch_bank = temp_pitch[abs(temp_pitch['bank']) > threshold_roll]
    rot_vel_z = temp_pitch_bank['velocity_rot_body_z'].to_numpy()
    eval_semi_roll = np.std(rot_vel_z) * rot_vel_z.size
    eval_semi_roll = eval_semi_roll if not isnan(eval_semi_roll) else 500

    eval_semi_roll = eval_semi_roll ** SEMI_ROLL_EXP_WEIGHT * SEMI_ROLL_WEIGHT
    
    eval = eval_heading_diff+eval_heading_initial_final+eval_semi_loop+eval_semi_roll
    return eval, {
                    'heading_initial_final': eval_heading_initial_final, 
                    'heading_diff': eval_heading_diff, 
                    'semi_loop': eval_semi_loop, 
                    'semi_roll': eval_semi_roll
                }
