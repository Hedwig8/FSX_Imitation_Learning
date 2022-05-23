from manoeuvres_data.approach import approach_controls
from manoeuvres_data.climb import climb_controls
from manoeuvres_data.halfCubanEight import half_cuban_eight_controls
from manoeuvres_data.immelmann import immelmann_controls
from manoeuvres_data.splitS import split_s_controls
from manoeuvres_data.curve import curve_controls
from manoeuvres_data.altitudeChanger import altitude_changer_controls

manoeuvre_data = {
    'Approach': approach_controls,
    'Climb': climb_controls,
    'HalfCubanEight': half_cuban_eight_controls,
    'Immelmann': immelmann_controls,
    'Split-S': split_s_controls,
    'SteepCurve': curve_controls,
    'AltitudeChanger': altitude_changer_controls,
}