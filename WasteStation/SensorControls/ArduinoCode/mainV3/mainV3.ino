
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
char binNum = 0;
long time0;
// number of steps per stepper motor rotation:
const int stepsPerRevolution = 512; //2048 = full rotation

// object initialization
NewPing hcsr04(HCSR04_PIN_TRIG,HCSR04_PIN_ECHO);
Servo servo360Micro_1;
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11); //stepper motor driver pin arrangement on Arduino


/**
 * Intiallize the sensors and actuators
 */
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
    
    binNum = waitForRequest();
}


/** 
 * Main logic of circuit
 **/
void loop() 
{
  int hcsr04Dist = 0;
  if(binNum == '1') { //operation with real values from ultrasonicsensor in bin 1
    // Read distance measurment from UltraSonic sensor
    hcsr04Dist = hcsr04.ping_cm();
  } else {  //operation with simulated values for bins 2, 3, 4
    switch(binNum) {
      case '2':
        hcsr04Dist = 50; //not full
        break;
      case '3':
        hcsr04Dist = 0; //full
        break;
      case '4':
        hcsr04Dist = 75; //not full
        break;
    }
  }
  Serial.println(hcsr04Dist);
  delay(3000);

  //only perform actuations if selected bin is not full (3 is an arbitrary max fullness value)
  if (hcsr04Dist > 3) {
    //only bin 1 in my testing is a 'real' bin
    actuatorsRun(binNum, hcsr04Dist, binNum != '1');
  }
  Serial.println("stop");
  delay(3200);

  
  binNum = waitForRequest();      
}


/** 
 * Function for waiting for data from serial connection
 *
 **/
char waitForRequest()
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
 * paran bin:           the bin that the user has selected
 *                        '1' = Garbage Bin
                          '2' = Cans/Bottles Bin  
                          '3' = Papers Bin
                          '4' = Compost Bin
 * param initFullness:  the initial fullness measurement on the bin (from ultrasonic sensor or simulated value)   
 * param simBin:        true if using a simulated bin (i.e. no use of ultrasonic sensor)
 *
 */
void actuatorsRun(char bin, int initFullness, bool simBin)
{
  // 1. Rotate internal divider accordingly
  switch(bin) {
    case '1':
      // no rotation
      // funnel is already aligned (default position
      break;
    case '2':
      // Trigger stepper motor to rotate for a quarter of full rotation:
      myStepper.step(stepsPerRevolution);
      delay(500);
      break;
    case '3':
      // Trigger stepper motor to rotate for a half of full rotation:
      myStepper.step(2*stepsPerRevolution);
      delay(500);
      break;
    case '4':
      // Trigger stepper motor to rotate for a three quarters of full rotation:
      myStepper.step(3*stepsPerRevolution);
      delay(500);
      break;
  }
  
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

  // 4. Reset internal divider back to default position
  switch(bin) {
    case '1':
      // no rotation
      // funnel is already aligned (default position)
      break;
    case '2':
      // Trigger stepper motor to rotate for a quarter of full rotation in reverse:
      myStepper.step(-stepsPerRevolution);
      delay(500);
      break;
    case '3':
      // Trigger stepper motor to rotate for a half of full rotation in reverse:
      myStepper.step(-2*stepsPerRevolution);
      delay(500);
      break;
    case '4':
      // Trigger stepper motor to rotate for a quarter of full rotation reverse:
      myStepper.step(stepsPerRevolution);
      delay(500);
      break;
  }
}
