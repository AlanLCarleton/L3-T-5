Arduino relate things are found in this directory

"Main" contains some test experiments with sensors and actuators that will be used.
"arduinoToRpi4V2.png" is the Arduino setup required to run these tests
*Everything is still under testing*

How to run:
	The "Main" folder contains the Arduino related files.
	1. In the "Main" folder, open "Main.ino" with Arduino IDE
	2. Load the file to the Arduino. The Arduino should be setup similarly to "arduinoToRpi4V2.png"
	3. With Python3, run "testArduinoCode.py" that's found back in the "ArduinoCode" directory
	4. You should now see a menu a the Python console. Follow the prompts to test which component.


Sources:
	- Ultrasonic sensor uses code from NewPing Library:
		AUTHOR/LICENSE: Tim Eckel - teckel@leethost.com
		Copyright 2016 License: GNU GPL v3 http://www.gnu.org/licenses/gpl.html
	