Arduino relate things are found in this directory

"ArduinoCode" contains some test experiments with sensors and actuators that will be used.
"arduinoToRpi4V2.png" is the Arduino setup required to run these tests

***NEW***
The folder "mainV2" contains test code for testing the waste station in operation (i.e. components run in sequence)
Running these tests is the same process as mentioned below.

Features:
	- Test reading data from ultrasonic sensor, then sending data to ThingSpeak. This test runs for around 18s and writes to ThingSpeak every 5s.
	- Test reading data from ThingSpeak channel. This test runs for around 18s and reads from ThingSpeak every 5s.
	- Test the stepper motor. Rotates the stepper motor clockwise and anti-clockwise.
	- Test the servo. Rotates the servo arm.

How to run:
	The "ArduinoCode" folder contains the Arduino related files.
	1. In the "main" folder (inside ("ArduinoCode"), open "Main.ino" with Arduino IDE
	2. Load the file to the Arduino. The Arduino should be setup similarly to "arduinoToRpi4V2.png"
	3. With Python3, run "testArduinoCode.py" that's found back in the "ArduinoCode" directory
	4. You should now see a menu a the Python console. Follow the prompts to test which component.


Sources:
	- Ultrasonic sensor uses code from NewPing Library:
		AUTHOR/LICENSE: Tim Eckel - teckel@leethost.com
		Copyright 2016 License: GNU GPL v3 http://www.gnu.org/licenses/gpl.html
	