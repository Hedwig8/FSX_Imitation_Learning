from keras.models import load_model

models_path = '../TrainedModels'

def load_models(manoeuvres_controls):
    new_dict = {}

    for name, controls in manoeuvres_controls.items():
        new_dict[name] = {}
        for control_surface in controls:
            new_dict[name][control_surface] = load_model(f'{models_path}/{name}/{control_surface}')
    return new_dict