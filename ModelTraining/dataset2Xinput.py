import numpy as np

def default_features(X_list, y_list):
    window = 15
    X_final = np.empty(shape=(0, window, X_list[0].shape[1]), dtype=np.float32)
    y_final = np.empty(shape=(0))
    for X_i, X in enumerate(X_list):
        for i in range(len(X)-window-1):
            # select values from i to i+window to make one 3D input frame
            X_final = np.concatenate((X_final, np.array([X[i:i+window]])))
        # select all values from window+1, making the outputs
        y_final = np.concatenate((y_final, y_list[X_i][window+1:]))
    return X_final, y_final

manoeuvre_dataset_2_Xinput = {
    'Immelmann': default_features,
    'SteepCurve': default_features,
}