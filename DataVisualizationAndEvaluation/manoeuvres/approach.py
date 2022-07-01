import numpy as np
from sklearn.preprocessing import normalize

def approach_eval(df):
    CONSTANT_DESCENT_RATE_EXP_WEIGHT = 1
    CONSTANT_DESCENT_RATE_WEIGHT = 1

    NOT_DESCENT_EXP_WEIGHT = 1
    NOT_DESCENT_WEIGHT = 100
    
    # constant descent rate
    descent_rate_np = df['altitude'].diff().shift(-1)[:-1].to_numpy()
    normalized_descent_rate = normalize([descent_rate_np])[0]
    eval_constant_descent_rate = np.std(normalized_descent_rate) * descent_rate_np.size #TODO rethink this

    eval_constant_descent_rate = eval_constant_descent_rate ** CONSTANT_DESCENT_RATE_EXP_WEIGHT * CONSTANT_DESCENT_RATE_WEIGHT


    # if go up
    initial_altitude = df['altitude'][0]
    final_altitude = df['altitude'].iloc[-1]
    diff = final_altitude - initial_altitude
    eval_not_descent = 1 if diff > 0 else 0

    eval_not_descent = eval_not_descent ** NOT_DESCENT_EXP_WEIGHT * NOT_DESCENT_WEIGHT

    eval = eval_constant_descent_rate + eval_not_descent

    return eval, {
                    'constant_descent_rate': eval_constant_descent_rate,
                    'not_descent':eval_not_descent,
                }