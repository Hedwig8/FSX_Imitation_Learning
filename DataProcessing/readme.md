(HF)

# DataProcessing

### fileCounter.py

This script was used to count all examples already collected from the volunteers. This prints in a tabular format the number of Good or Bad examples for each manoeuvre.

### fixTimeIntervals.py

The AircraftDataCollector is programmed to record the dataframes' time. The initial implementation did this by storing the time, in ms, referent to the starting of the example collection. Sometimes the queue of examples would expand (due to network problems or any delay in data processing) and several dataframes would end up with very close timestamps.

Then, I changed it to store the Sim time in which it was read (I believe it is the Unixtime or something based on that). Anyway, this script interpolates the timestamps of all dataframes to have a consistent time associated with each state reading. Each step is calculated as (last_timestamp - first_timestamp) / example_size, and each dataframe(i) is given the value of round(i * step).

### prepareFinalDataset

This basically organized the dataset in the publication format.

### requirements.txt

Hopefully an updated list of the dependencies used in this folder.

### utils

Utility functions used in the other files.