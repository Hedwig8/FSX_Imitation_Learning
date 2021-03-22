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
