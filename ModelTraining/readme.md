(HF)

# ModelTraining

### manoeuvres_data

These files are responsible for the selection of the features for the manoeuvres.

### manoeuvres_eval

These files are responsible for the metrics evaluation of the given examples. Duplicated from `DataVisualizationAndEvaluation/manoeuvres`.

### dataConsidered

The entry point for `manoeuvres_data`.

### dataset2input

Conversion from array of Pandas DataFrame to numpy array that is inputed to the model.

### evaluation

The entry point for `manoeuvres_eval`.

### featureCalculation

Responsible for the feature engineering of the manoeuvres, only one file because not much feature engineering was used.

### loadModel

As the name implies, loads the trained models to be used in `runPredict`.

### models

Configuration of the models experimented.

### predictProcessing

Feature engineering for the input data on the predict phase. It is in a different file because the format is different from the training data.

### requirements.txt

Hopefully an updated list of the dependencies used in this folder.

### run

Where the magic happens. In the first lines there are a lot of constant values to define what is supposed to be run and with which data. This script was developed with the goal of training all models in one process, without the need to be actively waiting for the end to start the next one. Took approximately 2h to run for all models with all Good data in a Ryzen 7 3800X/16GB/3060 Ti. However, as far as I tested, it is CPU-bounded by the dataset2input processing because of Python slowness.

### runClimbDescent

Experiment in which one model was trained with climb and descent data. Did not work.

### runPredict

This script creates a server to enable the communication from the FSXController app, in which recently collected data is received, analysed in order to create the prediction for the better action according to the aircraft state, and then sent the commands back.

### visUtils

Duplicated from `DataVisualizationAndEvaluation/visUtils`. Metrics calculation depend on this in manoeuvres_eval.