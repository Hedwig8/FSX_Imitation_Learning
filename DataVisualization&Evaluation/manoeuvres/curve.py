import numpy as np

def curve_eval(df):
    eval = 0
    ALTITUDE_DIFF_WEIGHT = 1
    BANK_DIFF_WEIGHT = 1000
    PITCH_DIFF_WEIGHT = 1000

    # altitude consistency
    # std * all values
    altitude_np = df['altitude'].to_numpy()
    eval1 = np.std(altitude_np) * altitude_np.size * ALTITUDE_DIFF_WEIGHT
    
    # bank consistency
    # discover max bank
    # consider every timestamp whose bank is higher than threshold_bank
    threshold_bank = 0.5 # percentage
    bank_np = np.abs(df['bank'].to_numpy())
    max_bank = np.max(bank_np)
    curve_np = bank_np[bank_np > max_bank * threshold_bank]
    eval2 = np.std(curve_np) * curve_np.size * BANK_DIFF_WEIGHT

    # pitch consistency
    # standard deviation from mean
    pitch_np = df['pitch'].to_numpy()
    eval3 = np.std(pitch_np) * pitch_np.size * PITCH_DIFF_WEIGHT

    # std from perfect circle curve
    # calculate perfect curve from initial and final heading and position
    # std ?? curve is "mean"
    # TODO

    eval = eval1+eval2+eval3
    return eval1, eval2, eval3, eval, eval1+eval2+eval3