Arduino relate things are found in this directory

"ArduinoCode" contains Arduino code for recieving and triggering data from the sensors and actuators.
"arduinoToRpi4V2.png" is the Arduino setup required to run these tests

The folder "mainV3" contains code for running the waste station in operation (i.e. components run in sequence)
The Python script "runStation.py" is used to call the Arduino to perform operations

Features:
	- Reading data from ultrasonic sensor, then sending data to ThingSpeak.
		- Data is read and sent before user drops item in station's bin.
		- Data is read and sent after user drops item in station's bin.
	- Stepper motor rotates the internal funnel to line up to selected bin.
	- Servo motor rotates to open and close the station's lid.

How to run:
	The "ArduinoCode" folder contains the Arduino related files.
	1. In the "mainV3" folder (inside ("ArduinoCode"), open "Main.ino" with Arduino IDE
	2. Load the file to the Arduino. The Arduino should be setup similarly to "arduinoToRpi4V2.png"
	3. With Python3, import "runStation.py" that's found back in the "ArduinoCode" directory
		3.1.	"blankTestScript.py" contains an example of this usage
		3.2. 	In "runStation.py" on line 128, '/dev/ttyACM0' might needs to be changed.
				This is the port that the Arduino board is connected to.
				For example, if the board is connected to ACM1, then it should be '/dev/ttyACM1'
	4. Now you're ready to call the functions found in "runStation.py"
		4.1.	To quickly test the system, you can run the function 'testStation'
		4.2.	'activateStation' is the function you need to call for triggering the Arduino

Additional Notes:
	- Using "runStation.py" without having an device that's connected via a Serial connection will present an error
	- Not setting the correct port in "runStation.py" will present an error (see instruction 3.2. above)
	- "mainV3" code has lots of "delay" to accomedate with Serial communication delays
		- Needs improvement
		
Sources:
	- Ultrasonic sensor uses code from NewPing Library:
		AUTHOR/LICENSE: Tim Eckel - teckel@leethost.com
		Copyright 2016 License: GNU GPL v3 http://www.gnu.org/licenses/gpl.html
	