from manoeuvres.halfCubanEight import half_eval
from manoeuvres.immelmann import immelmann_eval
from manoeuvres.curve import curve_eval
from manoeuvres.splits import split_s_eval
from manoeuvres.approach import approach_eval
from manoeuvres.climb import climb_eval
from manoeuvres.roll import roll_eval
from manoeuvres.canopyRoll import canopy_roll_eval

manoeuvre_evaluation = {
    'Approach': approach_eval,
    'Climb': climb_eval,
    'HalfCubanEight': half_eval,
    'Immelmann': immelmann_eval,
    'Split-S': split_s_eval,
    'SteepCurve': curve_eval,
    
    'Roll': roll_eval,
    'CanopyRoll': canopy_roll_eval,
}