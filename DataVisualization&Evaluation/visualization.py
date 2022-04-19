import glob
import math
import pandas as pd
import numpy as np
import plotly.express as px

from visUtils import velocity_to_position, rotate_initial_heading
from evaluation import manoeuvre_evaluation

dataset_path = "../dataset"
id = "*"
manoeuvre_quality = "Good"
manoeuvre_name = "SteepCurve"

examples_evals_list = []
evals_list = []
components_list = []
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = velocity_to_position(pd.read_csv(filename))
    df = rotate_initial_heading(df)
    eval, components = manoeuvre_evaluation[manoeuvre_name](df)
    examples_evals_list.append((df, eval))
    evals_list.append(eval)
    components_list.append(components)

components_box = px.box(components_list)
components_box.show()

min_eval = np.min(evals_list)
max_eval = np.max(evals_list)


trajetories_lines = px.line_3d()
for example, eval in examples_evals_list:
    intensity_green_blue = 255 - (((eval - min_eval)/(max_eval-min_eval)) * 255)
    trajetories_lines.add_scatter3d(x=example['x'], y=example['y'], z=example['z'], marker=dict(
        size=1,
        sizemode='diameter',
        color=f'rgb(255, {intensity_green_blue}, {intensity_green_blue})'
        )
    )
trajetories_lines.show()
