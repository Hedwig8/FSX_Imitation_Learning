import numpy as np

def hammerhead_process():
    pass

def immelmann_process(df):
    df['dt'] = df['time'].diff().shift(-1)
    max_altitude = np.max(df['altitude'])
    df['da'] = max_altitude - df['altitude']
    df = df[:-1]
    df = df.drop_duplicates(subset=['time'])
    return df

manoeuvre_processing = {
    'Hammerhead': hammerhead_process,
    'Immelmann': immelmann_process,
}