from manoeuvres_eval.halfCubanEight import half_eval
from manoeuvres_eval.immelmann import immelmann_eval
from manoeuvres_eval.curve import curve_eval
from manoeuvres_eval.splits import split_s_eval
from manoeuvres_eval.climb import climb_eval
from manoeuvres_eval.approach import approach_eval

from manoeuvres_eval.roll import roll_eval
from manoeuvres_eval.canopyRoll import canopy_roll_eval

manoeuvre_evaluation = {
    'Approach': approach_eval,
    'Climb': climb_eval,
    'HalfCubanEight': half_eval,
    'Immelmann': immelmann_eval,
    'Split-S': split_s_eval,
    'SteepCurve': curve_eval,

    'Roll': roll_eval,
    'CanopyRoll': canopy_roll_eval
}