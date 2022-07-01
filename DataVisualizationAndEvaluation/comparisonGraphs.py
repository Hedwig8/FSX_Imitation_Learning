from glob import glob
import pandas as pd
import plotly.graph_objects as go
import glob

from evaluation import manoeuvre_evaluation
from visUtils import velocity_to_position

dataset_path = '../ProcessedDataset'
id = '*'
manoeuvre_quality = 'Good'
manoeuvre_name = 'Immelmann'

results_path = '../Results'
id_results = 'AI'

evals = {
    'Examples': []
}
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = pd.read_csv(filename)
    df = velocity_to_position(df)
    eval, _ = manoeuvre_evaluation[manoeuvre_name](df)
    evals['Examples'].append(eval)

threshold = [1, .9, .75, .6]
for t in threshold:
    t_evals = []
    for filename in glob.glob(f'{results_path}/{id_results}/{t}/{manoeuvre_name}/*_1.csv', recursive=True):
        df = pd.read_csv(filename)
        df = velocity_to_position(df)
        eval, _ = manoeuvre_evaluation[manoeuvre_name](df)
        t_evals.append(eval)
    evals[f'{int(t*100)}%'] = t_evals

figure = go.Figure()
for key in evals.keys():
    figure.add_trace( go.Box(x= evals[key], name=key))
figure.update_layout(title=manoeuvre_name,
                        xaxis=dict(tickfont=dict(size=25)),
                        yaxis=dict(tickfont=dict(size=25)),
                        boxgap=0,
                        margin=dict(
                            b=100
                        ),)
figure.show()
