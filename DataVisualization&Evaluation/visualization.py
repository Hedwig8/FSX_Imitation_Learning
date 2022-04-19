import glob
import math
import pandas as pd
import plotly.express as px

from visUtils import velocity_to_position, rotate_initial_heading
from evaluation import manoeuvre_evaluation

dataset_path = "../dataset"
id = "*"
manoeuvre_quality = "Good"
manoeuvre_name = "Immelmann"

fig = px.line_3d()
examples_list = []
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = velocity_to_position(pd.read_csv(filename))
    df = rotate_initial_heading(df)
    examples_list.append(df)
    _,_,_,_, eval = manoeuvre_evaluation[manoeuvre_name](df)
    #green_blue = 255 - (((eval - 4360)/(400000-4360)) * 255)
    green_blue = 255 - (((eval - 760)/(2110-760)) * 255)

    green_blue = 0 if math.isnan(green_blue) else green_blue
    fig.add_scatter3d(x=df['x'], y=df['y'], z=df['z'], marker=dict(
        size=2,
        sizemode='diameter',
        color=f'rgb(255, {green_blue}, {green_blue})'
        )
    )

fig.show()
