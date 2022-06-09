from manoeuvres.halfCubanEight import half_eval
from manoeuvres.immelmann import immelmann_eval
from manoeuvres.curve import curve_eval
from manoeuvres.splits import split_s_eval

manoeuvre_evaluation = {
    'HalfCubanEight': half_eval,
    'Immelmann': immelmann_eval,
    'Split-S': split_s_eval,
    'SteepCurve': curve_eval,
}