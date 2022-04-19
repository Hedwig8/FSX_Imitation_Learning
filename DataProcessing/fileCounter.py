import glob

datasetPath = "../AircraftDataCollector/bin/Release/"
id = "*"
manoeuvreQuality = "Good"
manoeuvreName = "*"
manoeuvres = ['SteepCurve', 'HalfCubanEight', 'Immelmann', 'Split-S', 'Climb', 'Approach']
#manoeuvres = ['SteepCurve', 'HalfCubanEight', 'Immelmann', 'Split-S', 'Climb', 'Approach', 'TaxiRun&TakeOff', 'Landing', 'Roll', 'CanopyRoll', 'CubanEight', 'Hammerhead', 'Tailslide']

print(len(glob.glob(f'{datasetPath}/{id}/{manoeuvreQuality}/{manoeuvreName}/*.csv')))

for manoeuvre in manoeuvres:
    good = int(len(glob.glob(f'{datasetPath}/{id}/Good/{manoeuvre}/*.csv'))/2)
    bad = int(len(glob.glob(f'{datasetPath}/{id}/Bad/{manoeuvre}/*.csv'))/2)
    print(f'-> Good: {good}\t| Bad: {bad}\t<- {manoeuvre}')
