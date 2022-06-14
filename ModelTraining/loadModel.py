from keras.models import load_model
from joblib import load

models_path = '../TrainedModels'

def load_models(manoeuvres_controls, absolute='absolute', threshold=1):
    new_dict = {}

    for name, controls in manoeuvres_controls.items():
        new_dict[name] = {}
        for control_surface in controls:
            new_dict[name][control_surface] = load_model(f'{models_path}/{name}/{absolute}/threshold-{threshold}/{control_surface}')
    return new_dict

def load_scalers(manoeuvres_controls, absolute='absolute', threshold=1):
    new_dict = {}

    for name, controls in manoeuvres_controls.items():
        new_dict[name] = {}
        for control_surface in controls:
            new_dict[name][control_surface] = load(f'{models_path}/{name}/{absolute}/threshold-{threshold}/{control_surface}.scaler')
    return new_dict