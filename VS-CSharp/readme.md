(HF)

# VS-CSharp

###  AircraftDataCollector

This tool has the purpose of connecting to the FSX runtime engine and receive state information about the currently human-controlled airplane. It searches the simulator in the provided IP and subscribes to every simulation-tick's information about the attitude of the vehicle, as well as the inputs of the players, such as throttle or ailerons.

Composed of 3 different form pages, the interaction details can be found in the dissertation document.

### FSXController

Opposing the previous application, this one is used to input the direct controls of the airplane. This tool opens a tcp port to enable the communication to a python program that is running the trained models, originating and sending the predicted inputs for this tool, so it sends those to the FSX program.