(HF)

# DataVisualizationAndEvaluation

### manoeuvres

This folder contains auxiliary functions for the metric calculation for the examples. Each is responsible for the manoeuvre associated, and the functions return an overall evaluation and a dictionary with the individual metrics calculated.

### comparisonGraphs

Opens a webpage with a set of box diagrams representing evaluation distributions for the considered manoeuvres.

### evaluation

Entry point for the `manoeuvres` folder's files and functions.

### examples2DVisualization

Opens several web-based tabs with 2D visualizations of the examples trajectories in all combinations of 2-axes graphs (between x, y and z). Also opens box diagram graphs with evaluation distributions.

### examples3DVisualization

web-based 3D visualization of all examples of a certain manoeuvre. Colors vary from white to red, white being the best and red the worstly evaluated example.

### requirements.txt

Hopefully an updated list of the dependencies used in this folder.

### visUtils

Some functions to process data before it is visualized, such as position.