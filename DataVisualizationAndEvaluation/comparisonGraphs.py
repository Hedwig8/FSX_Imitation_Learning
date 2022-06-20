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
manoeuvre_name = 'Split-S'

results_path = '../Results'

evals = {
    'Total Eval': []
}
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = pd.read_csv(filename)
    eval, _ = manoeuvre_evaluation[manoeuvre_name](df)
    evals['Total Eval'].append(eval)

threshold = [1, .9, .75, .6]
for t in threshold:
    t_evals = []
    for filename in glob.glob(f'{results_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
        df = pd.read_csv(filename)
        eval, _ = manoeuvre_evaluation[manoeuvre_name](df)
        t_evals.append(eval)
    evals[f'{t*100}%'] = t_evals

figure = go.Figure()
for key in evals.keys():
    figure.add_trace( go.Box(x= evals[key], name=key))
figure.show()
