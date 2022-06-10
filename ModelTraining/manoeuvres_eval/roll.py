import numpy as np
from math import pi as PI
from sklearn.preprocessing import normalize

def roll_eval(df):

    INITIAL_FINAL_HEADING_EXP_WEIGHT = 1
    INITIAL_FINAL_HEADING_WEIGHT = 100000

    INITIAL_FINAL_ALTITUDE_EXP_WEIGHT = 1
    INITIAL_FINAL_ALTITUDE_WEIGHT = 200

    ROLL_CONSISTENCY_EXP_WEIGHT = 4
    ROLL_CONSISTENCY_WEIGHT = 10
    
    # vertical plane consistency
    initial_heading = df['heading'][0]
    final_heading = df['heading'].iloc[-1]
    heading_diff = (final_heading - initial_heading + PI) % (2 * PI) - PI
    eval_initial_final_heading = abs(heading_diff) ** INITIAL_FINAL_HEADING_EXP_WEIGHT * INITIAL_FINAL_HEADING_WEIGHT


    # altitude consistency 
    initial_altitude = df['altitude'][0]
    final_altitude = df['altitude'].iloc[-1]
    altitude_diff = final_altitude - initial_altitude
    eval_initial_final_altitude = abs(altitude_diff) ** INITIAL_FINAL_ALTITUDE_EXP_WEIGHT * INITIAL_FINAL_ALTITUDE_WEIGHT

    # roll rotation consistency
    threshold_bank = 0.2
    temp_bank = df[abs(df['bank']) > threshold_bank]
    rot_vel_z = temp_bank['velocity_rot_body_z'].to_numpy()
    normalized_rot_vez_z = normalize([rot_vel_z])[0]
    eval_roll_consistency = np.std(normalized_rot_vez_z) * rot_vel_z.size
    eval_roll_consistency = eval_roll_consistency ** ROLL_CONSISTENCY_EXP_WEIGHT * ROLL_CONSISTENCY_WEIGHT

    
    eval = eval_initial_final_altitude + eval_initial_final_heading + eval_roll_consistency
    return eval, {
                    'initial_final_heading_diff': eval_initial_final_heading,
                    'initial_final_altitude_diff': eval_initial_final_altitude,
                    'roll_consistency': eval_roll_consistency
                }