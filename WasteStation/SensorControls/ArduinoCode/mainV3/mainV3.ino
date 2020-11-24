
// Include Libraries
#include "Arduino.h"
#include "NewPing.h"
#include "Servo.h"
#include <Stepper.h>
#include <stdlib.h>

// Pin Definitions
#define HCSR04_PIN_TRIG	3
#define HCSR04_PIN_ECHO	2
#define SERVO360MICRO_1_PIN_SIG  5


// Global variables and defines
// define vars for testing menu
const int timeout = 6000;       //define timeout of 6 sec
char menuOption = 0;
long time0;
// number of steps per stepper motor rotation:
const int stepsPerRevolution = 512; //2048 = full rotation

// object initialization
NewPing hcsr04(HCSR04_PIN_TRIG,HCSR04_PIN_ECHO);
Servo servo360Micro_1;
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11); //stepper motor driver pin arrangement on Arduino

void setup() 
{
    // Setup Serial communication (for RPi communication)
    Serial.begin(9600);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB
    //Serial.println("start");
    
    servo360Micro_1.attach(SERVO360MICRO_1_PIN_SIG); // attach servo 1 to pin to control it.
    servo360Micro_1.write(1500);  // value of 1500 = stoped
    delay(100);
    
    // Set stepper motor speed to 36 rpm:
    myStepper.setSpeed(36);
    
    menuOption = menu();
}

// Main logic of circuit
void loop() 
{
  //operation with real values from ultrasonicsensor in bin 1
  if(menuOption == '1') {
    // Read distance measurment from UltraSonic sensor
    int hcsr04Dist = hcsr04.ping_cm();
    Serial.println(hcsr04Dist);
    delay(3000);

    //only perform actuations if selected bin is not full (3 is an arbitrary max fullness value)
    if (hcsr04Dist > 3) {
      actuatorsRun(hcsr04Dist, false);
    }
    Serial.println("stop");
    delay(3200);
  }
  //operation with simulated values for bins 2, 3, 4
  else {
    int hcsr04DistSim = 0;
    //setting values for the selected simulate bin
    switch(menuOption) {
      case '2':
        hcsr04DistSim = 50; //not full
        break;
      case '3':
        hcsr04DistSim = 0; //full
        break;
      case '4':
        hcsr04DistSim = 75; //not full
        break;
    }
    
    Serial.println(hcsr04DistSim);
    delay(3000);

    //only perform actuations if selected bin is not full (3 is an arbitrary max fullness value)
    if (hcsr04DistSim > 3) {
      actuatorsRun(hcsr04DistSim, true);
    }
    Serial.println("stop");
    delay(3200);
  }
  
  menuOption = menu();      
}


// Menu function for selecting the components to be tested
// Follow serial monitor for instrcutions
char menu()
{
  while (!Serial.available());

  // Read data from serial monitor if received
  while (Serial.available()) {
    char c = Serial.read();
    if (isAlphaNumeric(c)) {
      time0 = millis();
      return c;
    }
  }
}

/**
 * Trigger actuators in waste station
 * Rotates internal divider, opens lid, then close lid
 *    
 * param initFullness:  the initial fullness measurement on the bin (from ultrasonic sensor or simulated value)   
 * param simBin:        true if using a simulated bin (i.e. no use of ultrasonic sensor)
 *
 */
void actuatorsRun(int initFullness, bool simBin)
{
  // 1. Rotate internal divider accordingly
  // Trigger stepper motor to rotate for a quarter of full rotation:
  myStepper.step(stepsPerRevolution);
  delay(500);
  
  // 2. Open station's lid
  servo360Micro_1.writeMicroseconds(1180); // set servo speed (counter clockwise)
  delay(397); // time delay of 397ms with speed of 1180 is a half (360) turn of the servo
  servo360Micro_1.writeMicroseconds(1500); // stopped
  delay(100);
  
  // 3.Close station's lid (after UltraSonic sensor trigger or timeout)
  bool deposited = false;
  int hcsr04Dist2;

  if (simBin) hcsr04Dist2 = initFullness - (rand() % 5) + 1;
  do { //lid closes either on timeout or fullness increases
    if (!simBin){
      hcsr04Dist2 = hcsr04.ping_cm();
    }
    delay(50);
    if (initFullness > hcsr04Dist2) deposited = true;
  } while (!deposited && time0 + timeout > millis());
      
  Serial.println(hcsr04Dist2);
  delay(2500);
  //closing lid
  servo360Micro_1.writeMicroseconds(1790); // counter clockwise to close lid
  delay(390); // time delay of 390ms with speed of 1180 is a half (360) turn of the servo
  servo360Micro_1.writeMicroseconds(1500); // stopped
  delay(100);
}
