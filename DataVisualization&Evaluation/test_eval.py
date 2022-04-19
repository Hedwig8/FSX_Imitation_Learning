import glob 
import pandas as pd
import plotly.express as px
import math

from evaluation import manoeuvre_evaluation

dataset_path = '../dataset'
id='*'
manoeuvre_quality = 'Good'
manoeuvre_name = 'Immelmann'

examples_list = []
x1list = []
x2list = []
x3list = []
x4list = []
x5list = []
for filename in glob.glob(f'{dataset_path}/{id}/{manoeuvre_quality}/{manoeuvre_name}/*_1.csv', recursive=True):
    df = pd.read_csv(filename)
    examples_list.append(df)
    x1, x2, x3, x4, x5 = manoeuvre_evaluation[manoeuvre_name](df)
    x1list.append(x1)
    x2list.append(x2)
    x3list.append(x3)
    x4list.append(x4)
    x5list.append(x5)
    if (math.isnan(x5)): print(filename)

df = pd.DataFrame([x1list, x2list, x3list, x4list, x5list])
fig = px.box(df.T)
fig.show()