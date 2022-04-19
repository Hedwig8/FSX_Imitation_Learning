import math
import numpy as np

def immelmann_eval(df):
    INITIAL_FINAL_HEADING_WEIGHT = 200
    HEADING_DIFF_WEIGHT = 2
    SEMI_LOOP_WEIGHT = 2
    SEMI_ROLL_WEIGHT = 1

    # vertical plane consistency
    # initial and final heading are references 
    heading_np = df['heading'].to_numpy()

    initial_heading = heading_np[:5].mean()
    final_heading = heading_np[-5:].mean()

    eval_heading_initial_final = abs(final_heading - initial_heading) * INITIAL_FINAL_HEADING_WEIGHT
    eval_heading_diff = 0
    for heading in heading_np[5:-5]:
        eval_heading_diff += min(abs(heading-initial_heading), abs(heading-final_heading)) * HEADING_DIFF_WEIGHT

    # semi-loop consistency
    # compare all x-axis rotation velocity
    # when pitch is lower than -0.1 (pointing upwards)
    threshold_pitch = -0.1
    rot_vel_x = np.abs(df[df['pitch'] < threshold_pitch]['velocity_rot_body_x'].to_numpy())

    eval_semi_loop = np.std(rot_vel_x) * rot_vel_x.size * SEMI_LOOP_WEIGHT

    # semi-roll consistency
    # compare all z-axis rotation velocity
    # when roll is between 2 values and higher than threshold_pitch
    threshold_roll = 0.2
    threshold_pitch_roll = -0.3
    temp_pitch = df[df['pitch'] > threshold_pitch_roll] # 
    temp_pitch_bank = temp_pitch[abs(temp_pitch['bank']) > threshold_roll]
    rot_vel_z = temp_pitch_bank['velocity_rot_body_z'].to_numpy()
    eval_semi_roll = np.std(rot_vel_z) * rot_vel_z.size * SEMI_ROLL_WEIGHT
    eval_semi_roll = eval_semi_roll if not math.isnan(eval_semi_roll) else 1000
    
    eval = eval_heading_diff+eval_heading_initial_final+eval_semi_loop+eval_semi_roll
    return eval, {
                    'heading_initial_final': eval_heading_initial_final, 
                    'heading_diff': eval_heading_diff, 
                    'semi_loop':eval_semi_loop, 
                    'eval_semi_roll': eval_semi_roll
                }
