# FSX Imitation Learning

This project aims to create a program capable of autonomously flying aircraft on the FSX.
At the moment only the data collection module is available.



## Preparation

For this program to work the **Simconnect SDK must be installed**. 

For FSX:SE follow the steps below:
1. Go to "FSX location"\SDK\Core Utilities Kit\SimConnect SDK\LegacyInterfaces
2. For each folder in this directory run SimConnect.msi to install
3. To check if Simconnect was successfully installed, there should be several entries of "Microsoft Flight Simulator Simconnect Client" in the program list on Control Panel

To install the SDK in other versions of FSX please follow [this guide](https://www.fsdeveloper.com/wiki/index.php?title=SDK_Installation_(FSX)).



## How to run the program

1. Unzip *FSXDataResquest.zip* 
2. Execute *FSXDataRequest.exe* (a window should pop up)
3. The connection status should be "Trying to connect ..."
<img src="https://i.imgur.com/sgwSDf8.png" width="300">



## How to collect flight data

1. Run FSX.
2. The *FSXDataRequest* automatically detects if FSX is running. The connection status should now be "Connected".

<img src="https://i.imgur.com/3dPRiMU.png" width="300">

3. Start a free flight with an aircraft, location and weather of your choosing.
4. Click the button "Start Collect" in order to start collecting flight data.

<img src="https://i.imgur.com/LgoFdVJ.png" width="300">

5. Perform an aerobatic maneuver.
6. Click the button "Stop Collect".
7. If you are happy with your performance click on "Save".

<img src="https://i.imgur.com/cOL6u3F.png" width="300">

9. All the log files are stored in the *logs* folder located inside *FSXDataRequest*. 

# How to send us the log files.

Visit https://web.fe.up.pt/~up201605344/

Drag and drop all the files on the *logs* folder into the website.

## Notes
* Before ending the flight or restarting make sure the program is not collecting data in order to avoid conflicts between flights.

## Variables collected

The following presents an exhaustive list of all the variables that *FSXDataRequest* collects:

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
