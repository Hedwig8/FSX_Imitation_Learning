import numpy as np
from sklearn.preprocessing import normalize

def curve_eval(df):
    ALTITUDE_DIFF_EXP_WEIGHT = 1
    ALTITUDE_DIFF_WEIGHT = 20000

    BANK_DIFF_EXP_WEIGHT = 3
    BANK_DIFF_WEIGHT = 500

    PITCH_DIFF_EXP_WEIGHT = 3
    PITCH_DIFF_WEIGHT = 3

    # altitude consistency -> TODO: change for altitude delta sum
    # std * all values
    altitude_np = df['altitude'].to_numpy()
    normalized_altitude = normalize([altitude_np])[0]
    eval_altitude_diff = np.std(normalized_altitude) * altitude_np.size 
    eval_altitude_diff = eval_altitude_diff ** ALTITUDE_DIFF_EXP_WEIGHT * ALTITUDE_DIFF_WEIGHT
    
    # bank consistency
    # discover max bank
    # consider every timestamp whose bank is higher than threshold_bank
    threshold_bank = 0.5 # percentage
    bank_np = np.abs(df['bank'].to_numpy())
    max_bank = np.max(bank_np)
    curve_np = bank_np[bank_np > max_bank * threshold_bank]
    normalized_curve = normalize([curve_np])[0]
    eval_bank_diff = np.std(normalized_curve) * curve_np.size
    eval_bank_diff = eval_bank_diff ** BANK_DIFF_EXP_WEIGHT * BANK_DIFF_WEIGHT

    # pitch consistency
    # standard deviation from mean
    pitch_np = df['pitch'].to_numpy()
    normalized_pitch = normalize([pitch_np])[0]
    eval_pitch_diff = np.std(normalized_pitch) * pitch_np.size
    eval_pitch_diff = eval_pitch_diff ** PITCH_DIFF_EXP_WEIGHT * PITCH_DIFF_WEIGHT

    # std from perfect circle curve
    # fit xy datapoints to circumference curve
    # distance from datapoint to closest point in circumference
    # replace both above
    # TODO with calculations already done in immelmann, split-s or halfcubaneight

    eval = eval_altitude_diff+eval_bank_diff+eval_pitch_diff
    return eval, {
                    'altitude_diff': eval_altitude_diff, 
                    'bank_diff': eval_bank_diff, 
                    'pitch_diff': eval_pitch_diff,
                }