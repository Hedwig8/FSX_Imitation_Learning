import numpy as np

# input: list of df
# output: data organized accordingly to window of specified size
def default_features(X_list, y_list, window):
    X_final = np.empty(shape=(0, window, X_list[0].shape[1]), dtype=np.float32)
    y_final = np.empty(shape=(0))
    for X_i, X in enumerate(X_list):
        for i in range(len(X)-window-1):
            # select values from i to i+window to make one 3D input frame
            X_final = np.concatenate((X_final, np.array([X[i:i+window]])))
        # select all values from window+1, making the outputs
        y_final = np.concatenate((y_final, y_list[X_i][window+1:]))
    return X_final, y_final

# window unused, just to be according to structure
def no_window(X_list, y_list, window):
    X_final = np.empty(shape=(0, X_list[0].shape[1]))
    y_final = np.empty(shape=(0))
    for X, y in zip(X_list, y_list):
        X_final = np.concatenate((X_final, np.array(X)))
        y_final = np.concatenate((y_final, np.array(y)))
    return X_final, y_final

manoeuvre_dataset_2_input = {
    'Approach': default_features,
    'Climb': no_window,
    'HalfCubanEight': default_features,
    'Immelmann': default_features,
    'Split-S': default_features,
    'SteepCurve': default_features,
    'AltitudeChanger': default_features,

    'Roll': default_features,
    'CanopyRoll': default_features,
}

manoeuvre_window_size = {
    'Approach': 15,
    'Climb': 1,
    'HalfCubanEight': 15,
    'Immelmann': 15,
    'Split-S': 15,
    'SteepCurve': 15,
    'AltitudeChanger': 15,

    'Roll': 15,
    'CanopyRoll': 15,
}