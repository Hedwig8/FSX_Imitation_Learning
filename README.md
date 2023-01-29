# FSX Imitation Learning
This project aims to create a program capable of autonomously flying aircraft on the FSX.
At the moment only the data collection module is available.


## Introduction
This project is part of my master's thesis which aims to create an autopilot capable of learning to perform aerobatic maneuvers in various types of aircraft and conditions.
The following section lists some maneuvers selected to be learned by the autopilot.
We ask that you perform some of these maneuvers in various scenarios and with different aircraft while recording the logs using the AircraftDataCollector program.
Please click on Stop collect after each maneuver in order to have only one maneuver per collect.


## List of aerobatic maneuvers
- Knife edge 180 degree turn
- Half cuban eight: https://www.youtube.com/watch?v=Yj7LxfZi0dA
- Canopy roll: http://www.youtube.com/watch?v=uCquoeGZ910&t=1m9s
- Split: http://www.youtube.com/watch?v=uCquoeGZ910&t=1m52s
- Immelman turn: http://www.youtube.com/watch?v=uCquoeGZ910&t=2m18s





## Preparation

For this program to work the **Simconnect SDK must be installed**. 

For FSX:SE follow the steps below:
1. Go to "FSX location"\SDK\Core Utilities Kit\SimConnect SDK\LegacyInterfaces
2. For each folder in this directory run SimConnect.msi to install
3. To check if Simconnect was successfully installed, there should be several entries of "Microsoft Flight Simulator Simconnect Client" in the program list on Control Panel

To install the SDK in other versions of FSX please follow [this guide](https://www.fsdeveloper.com/wiki/index.php?title=SDK_Installation_(FSX)).



## How to run the program

1. Download *AircraftDataCollector.zip" in the releases
2. Unzip *AircraftDataCollector.zip* 
3. Execute *AircraftDataCollector.exe*
4. A window should pop up with connection status "Trying to connect ..."
<img src="https://i.imgur.com/sgwSDf8.png" width="300">



## How to collect flight data

1. Run FSX.
2. The *AircraftDataCollector* automatically detects if FSX is running. The connection status should now be "Connected".

<img src="https://i.imgur.com/3dPRiMU.png" width="300">

3. Start a free flight with an aircraft, location and weather of your choosing.
4. Click the button "Start Collect" in order to start collecting flight data.

<img src="https://i.imgur.com/LgoFdVJ.png" width="300">

5. Perform an aerobatic maneuver.
6. Click the button "Stop Collect".
7. If you are happy with your performance choose the maneuver performed and click on "Save".

<img src="https://i.imgur.com/cJ9yuhC.png" width="300">

9. All the log files are stored in the *logs* folder located inside *AircraftDataCollector*. 

# How to send us the log files.

Visit https://web.fe.up.pt/~up201605344/

Drag and drop all the files on the *logs* folder into the website.

## Notes
* Before ending the flight or restarting make sure the program is not collecting data in order to avoid conflicts between flights.

## Variables collected

The following presents an exhaustive list of all the variables that *AircraftDataCollector* collects:

* Altitude above ground
* Altitude
* Velocity body x/y/z
* Velocity world x/y/z
* Velocity rotation body x/y/z
* Wind velocity body x/y/z
* Wind velocity world x/y/z
* Acceleration body x/y/z
* Pitch angle 
* Bank angle
* Heading angle
* Rudder position
* Elevator position
* Aileron position
* Flaps position
* Spoilers position
* Engine Rpm
* Engine throttle position
* Aircraft model
* Ambient density
* Ambient temperature	
* Ambient pressure
* Sea level pressure
* Gear position
* Current fuel


## Edited at 05/10/2022 by Henrique Freitas (HF) - author of Learn to Fly II: Acrobatic Manoeuvres

The code present in this repository was all developed and used in the context of Learn to Fly II development. The Python scripts played a major role in the data processing and visualization, including all ML training phases. Inside each code folder is a readme.md explaining the usage of each script. 

Below I wrote a brief description of each folder.


#### CircuitControlResults folder

Contains the `.csv` files of the collected data regarding the last stage of the project, Circuit Control. Each `.csv` has timestamps collected during the execution of the manoeuvres.

Unfortunately I don't recall which are good or bad. Two experiments were made: CircuitControl (first) and CircuitControl2 (second). The classification in Good/Bad and Hammerhead/Tailslide are not to be trusted: the AircraftDataCollector app (more info on VS-CSharp folder) was done for collecting individual manoeuvres and was reused here, so the classification was a simple way to differentiate between runs.


#### DataProcessing

These were the first and last scripts I created, some early in the Data Collection phase and one at the end when preparing for the dataset publication. They either read `.csv` files and output information or process `.csv` and write new ones with fixed data.

More info in the `readme.md` inside this folder.


#### DataVisualizationAndEvaluation

Scripts used for mainly data visualization. All graphs are built using plotly library. 

`evaluation` file and `manoeuvres` folder have the metrics used in each manoeuvres. They are a duplicated of the `evaluation` file and `manoeuvres_eval` folder in `ModelTraining` folder. I could not make Python modules out of them, so that was the only quick solution I got. Now, I advise to use something like symbolic links to use it in both folders.

More info in the `readme.md` inside this folder.

#### Model Training

In a broad sense, all these scripts are part of the training of the models, with the preprocessed data from `DataProcessing/fixTimeIntervals`. The only scripts supposed to be run here are the one starting with `run`: `run*.py`.

More info in the `readme.md` inside this folder.

#### ProcessedDataset

After the initially collected dataset, some data files were not in the same format (especifically the time column) and needed to be processed using scripts from `DataProcessing/`.

#### PublishedDataset

Rearranged processed dataset, for the publication of it.

#### Results

Final results gathered in the tests phase. The graphs shown in the dissertation document were constructed using this data.

#### TrainedModels

Last batch of trained models, these were used to originate the datasets inside `Results/`.

#### UnprocessedResults

These are the data files from the last tests done (and kept, the remaining unprocessed data was being deleted throughout the development of the dissertation). Relative to Transfer Learning test phase.

#### VS-CSharp

The C# code for the 2 windows forms application used for communication with the FSX runtime. 

More info in the `readme.md` inside this folder.
