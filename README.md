# SYSC3010_L2-M-6_Project

This document provides an outline for the GitHub, and for how to set up the Household Environment Monitoring Automation System (H.E.M.A.S.).

GitHub: 
	The GitHub has two (2) active branches: main, and final.  The main branch consists of all the testing and prototyping code, while the final branch contains only the code used in the final system implementation. Some tests are outdated and should no longer be used; specifically the tests for RPI4 channels.

	The branches have several folders that specify which Raspberry Pi they are intended for use on, according to the architecture UML diagram used in all project reports.  

RPI1: 
	For usage of this code on the Raspberry Pi, download all files from the final branch.  All code must be in the same folder directory on the Raspberry Pi.  Before running the code, ensure that all hardware is connected to the appropriate GPIO ports on the Raspberry Pi, and that all necessary libraries have been installed.  For a list of necessary libraries please see the Imports section of RPI1_Final.py.  

To run the code, you only need to run RPI1_Final.py.  All necessary external code will be imported.  It will initially run a few test cases to ensure the hardware is connected properly and all necessary libraries are installed.  These tests can be found in RPI1_LED_test.py, RPI1_PiCam_test.py, and RPI1_Motor_test.py, but there is no need to run them individually, as RPI1_Final.py will import them and run them as necessary.  For information on what these tests are expected to do, please see the documentation in the relevant file.  

RPI2:
	All the code required to operate RPI2 can be found within the RPI2 folder of the Final branch on the team GitHub. There is one file there that needs to be run which is RPI2_Final.py. To enable this component, it is as simple as opening this file and running it. The data collection will automatically start to operate at its set frequency of once every second, writing the data to ThingSpeak Channel B.

RPI3:
	The code necessary for RPI3 to run is in the GitHub repository in the Final branch. The file that needs to be run is Anemometer&WindVane.py, however it requires two test classes, which are Anemometer_test.py, Wind_Vane_test.py to run successfully. The first two files are test classes needed to run the main file. Both test classes ensure the imports and data collection can be done by the system. Anemometer&WindVane.py will run the test cases on its own. 

RPI4:
	All the code for the RPI4 is in the RPI4 folder in the Final branch on GitHub. The required files are: RPI4_Final.py, emailAlert.py, RPI4_GUI3.py, RPI4_main.py, RPI4_Temp.py and mage.png. The database file should be ignored as it will be created upon running the code. To run the code, open RPI4_main.py and run it. The list of required libraries should be clear from the import statements at the top of the file, however, to get pandas use pip and type: “pip install altair vega_datasets” (The reason for this is because installing just pandas alone has some issues).

H.E.M.A.S.
	For the overall system to work to its full capacity all systems should be running properly at the same time.   The system should not break down if a Pi is not running, but the database will not contain the data for that specific Pi, given that it would not be sending data to the thingspeak channel.
