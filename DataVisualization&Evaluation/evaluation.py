from manoeuvres.immelmann import immelmann_eval
from manoeuvres.curve import curve_eval

manoeuvre_evaluation = {
    'Immelmann': immelmann_eval,
    'SteepCurve': curve_eval,
}