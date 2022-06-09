from glob import glob
from turtle import color
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import glob

from evaluation import manoeuvre_evaluation

dataset_path = '../ProcessedDataset'
id = '*'
manoeuvre_quality = 'Good'
manoeuvre_name = 'HalfCubanEight'

results_path = '../Results'

evals = []
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = pd.read_csv(filename)
    eval, _ = manoeuvre_evaluation[manoeuvre_name](df)
    evals.append(eval)

results = []
for filename in glob.glob(f'{results_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = pd.read_csv(filename)
    eval, _ = manoeuvre_evaluation[manoeuvre_name](df)
    results.append({'type': 'circle', 
                    'xref': 'x',
                   'yref': 'y',
                   'x0': eval-1200,
                   'y0': -0.005,
                   'x1': eval+1200,
                   'y1': .005,
                   'fillcolor':'rgb(255, 64, 64)', 
                   'line': {
                       'width': 1.5,
                   }})
    print(eval)

#graph = ff.create_distplot([ evals ], ['Examples Evaluations'], curve_type='kde', bin_size=10000, show_hist=False, show_rug=False )
#graph.update_layout(title_text=manoeuvre_name)

violin = go.Box({'x':evals})
lines = go.Layout(shapes=results, )
figure = go.Figure(data=violin, layout=lines)
figure.show()
