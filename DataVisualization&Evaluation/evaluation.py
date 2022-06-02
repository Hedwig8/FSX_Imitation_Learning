from manoeuvres.immelmann import immelmann_eval
from manoeuvres.curve import curve_eval
from manoeuvres.splits import split_s_eval

manoeuvre_evaluation = {
    'Immelmann': immelmann_eval,
    'Split-S': split_s_eval,
    'SteepCurve': curve_eval,
}