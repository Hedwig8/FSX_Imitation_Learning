import glob
import pandas as pd
import plotly.express as px

from visUtils import velocity_to_position, rotate_initial_heading
from evaluation import manoeuvre_evaluation

dataset_path = '../ProcessedDataset'
id = '*'
manoeuvre_quality = 'Good'
manoeuvre_name = 'Immelmann'

examples_evals_list = []
evals_list = []
components_list = []
components_evals_list = []
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = velocity_to_position(pd.read_csv(filename))
    df = rotate_initial_heading(df)
    eval, components = manoeuvre_evaluation[manoeuvre_name](df)
    examples_evals_list.append((df, eval))
    evals_list.append(eval)
    components_list.append(components)
    components_evals_list.append((eval, components))

components_box = px.box(components_list)
components_box.update_layout(xaxis=dict(tickfont=dict(size=30)),
                                yaxis=dict(tickfont=dict(size=15)),
                                boxgap=0,
                                margin=dict(
                                    b=100
                                ),)
components_box.show()

evals_box =  px.box(dict(total_evaluation = evals_list))
evals_box.update_layout(xaxis=dict(tickfont=dict(size=30)),
                                yaxis=dict(tickfont=dict(size=15)),
                                margin=dict(
                                    r=1450,
                                    b=100
                                ))
evals_box.show()

trajetories_xy = px.line()
trajetories_yz = px.line()
trajetories_xz = px.line()
for example, _ in examples_evals_list:
    trajetories_xy.add_scatter(x=example['x'], y=example['y'])
    trajetories_yz.add_scatter(x=example['y'], y=example['z'])
    trajetories_xz.add_scatter(x=example['x'], y=example['z'])
trajetories_xy.show()
trajetories_yz.show()
trajetories_xz.show()

# 60% best evals
eval_threshold = .6
threshold = round(len(examples_evals_list) * eval_threshold)

sorted_examples_evals_list = sorted(examples_evals_list, key=lambda x: x[1])
sorted_components_evals_list = sorted(components_evals_list, key=lambda x: x[0])

filtered_examples_evals_list = sorted_examples_evals_list[:threshold]
filtered_components_evals_list = sorted_components_evals_list[:threshold]

filtered_components_list = [x[1] for x in filtered_components_evals_list]
filtered_evals_list = [x[0] for x in filtered_components_evals_list]

filtered_components_box = px.box(filtered_components_list)
filtered_components_box.show()

filtered_evals_box =  px.box(filtered_evals_list)
filtered_evals_box.show()

filtered_trajetories_xy = px.line()
filtered_trajetories_yz = px.line()
filtered_trajetories_xz = px.line()
for example, _ in filtered_examples_evals_list:
    filtered_trajetories_xy.add_scatter(x=example['x'], y=example['y'])
    filtered_trajetories_yz.add_scatter(x=example['y'], y=example['z'])
    filtered_trajetories_xz.add_scatter(x=example['x'], y=example['z'])
filtered_trajetories_xy.show()
filtered_trajetories_yz.show()
filtered_trajetories_xz.show()