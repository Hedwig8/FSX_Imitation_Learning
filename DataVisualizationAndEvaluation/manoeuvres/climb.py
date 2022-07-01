import numpy as np
from sklearn.preprocessing import normalize


def climb_eval(df):

    CONSTANT_CLIMB_RATE_EXP_WEIGHT = 2
    CONSTANT_CLIMB_RATE_WEIGHT = 1

    NOT_CLIMB_EXP_WEIGHT = 1
    NOT_CLIMB_WEIGHT = 2000
    
    # constant climb rate
    climb_rate_np = df['altitude'].diff().shift(-1)[:-1].to_numpy()
    normalized_climb_rate = normalize([climb_rate_np])[0]
    eval_constant_climb_rate = np.std(normalized_climb_rate) * climb_rate_np.size #TODO rethink this

    eval_constant_climb_rate = eval_constant_climb_rate ** CONSTANT_CLIMB_RATE_EXP_WEIGHT * CONSTANT_CLIMB_RATE_WEIGHT


    # if go up
    initial_altitude = df['altitude'][0]
    final_altitude = df['altitude'].iloc[-1]
    diff = final_altitude - initial_altitude
    eval_not_climb = 1 if diff < 0 else 0

    eval_not_climb = eval_not_climb ** NOT_CLIMB_EXP_WEIGHT * NOT_CLIMB_WEIGHT

    eval = eval_constant_climb_rate + eval_not_climb

    return eval, {
                    'constant_climb_rate': eval_constant_climb_rate,
                    'not_climb':eval_not_climb,
                }