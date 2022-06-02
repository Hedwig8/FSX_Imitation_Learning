import glob
import pandas as pd
from math import isnan
import plotly.express as px

from visUtils import velocity_to_position, rotate_initial_heading
from evaluation import manoeuvre_evaluation

dataset_path = "../ProcessedDataset"
id = "*"
manoeuvre_quality = "Good"
manoeuvre_name = "Immelmann"

examples_evals_list = []
evals_list = []
components_list = []
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = velocity_to_position(pd.read_csv(filename))
    df = rotate_initial_heading(df)
    eval, components = manoeuvre_evaluation[manoeuvre_name](df)
    if eval < 60: continue
    examples_evals_list.append((df, eval))
    evals_list.append(eval)
    components_list.append(components)

components_box = px.box(components_list)
components_box.show()

min_eval = min(evals_list)
max_eval = max(evals_list)


trajetories_lines = px.line_3d()
for example, eval in examples_evals_list:
    intensity_green_blue = 255 - (((eval - min_eval)/(max_eval-min_eval)) * 255)
    intensity_green_blue = intensity_green_blue if not isnan(intensity_green_blue) else 0
    trajetories_lines.add_scatter3d(x=example['x'], y=example['y'], z=example['z'], marker=dict(
        size=1,
        sizemode='diameter',
        color=f'rgb(255, {intensity_green_blue}, {intensity_green_blue})'
        )
    )
trajetories_lines.show()
