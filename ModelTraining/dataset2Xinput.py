import numpy as np

def default_process():
    pass

def immelmann_features(X, y):
    window = 15
    X_final = np.empty(shape=(0, window, X.shape[1]), dtype=np.float32)
    for i in range(len(X)-window-1):
        X_final = np.concatenate((X_final, np.array([X[i:i+window]])))

    return X_final, y[window+1:]

manoeuvre_dataset_2_Xinput = {
    'Hammerhead': default_process,
    'Immelmann': immelmann_features,
}