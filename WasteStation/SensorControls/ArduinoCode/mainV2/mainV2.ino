
// Include Libraries
#include "Arduino.h"
#include "NewPing.h"
#include "Servo.h"
#include <Stepper.h>

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
  //Testing station regular operation
  if(menuOption == '1') {
    // 1. Read distance measurment from UltraSonic sensor
    int hcsr04Dist = hcsr04.ping_cm();
    Serial.println(hcsr04Dist);
    delay(2000);

    //only perform actuations if selected bin is not full (3 is an arbitrary max fullness value)
    if (hcsr04Dist > 3) {
      // 2. Rotate internal divider accordingly
      // Trigger stepper motor to rotate for a quarter of full rotation:
      myStepper.step(stepsPerRevolution);
      delay(500);
  
      // 3. Open station's lid
      servo360Micro_1.writeMicroseconds(1180); // set servo speed (counter clockwise)
      delay(397); // time delay of 397ms with speed of 1180 is a half (360) turn of the servo
      servo360Micro_1.writeMicroseconds(1500); // stopped
      delay(100);
  
      // 4.Close station's lid (after UltraSonic sensor trigger or timeout)
      bool deposited = false;
      int hcsr04Dist2;
      do { //lid closes either on timeout or fullness increases
        hcsr04Dist2 = hcsr04.ping_cm();
        if (hcsr04Dist > hcsr04Dist2) deposited = true;
      } while (!deposited && time0 + timeout > millis());
      
      Serial.println(hcsr04Dist2);
      delay(2000);
      //closing lid
      servo360Micro_1.writeMicroseconds(1790); // counter clockwise to close lid
      delay(390); // time delay of 390ms with speed of 1180 is a half (360) turn of the servo
      servo360Micro_1.writeMicroseconds(1500); // stopped
      delay(100);
    }
    Serial.println("stop");
    delay(3000);
  }
  //Testing station operation with a simulated full bin
  else if(menuOption == '2') {
    // Read distance measurment from UltraSonic sensor (hard coded)
    int hcsr04Dist = 2;
    Serial.println(hcsr04Dist);
    delay(2000);
    if (hcsr04Dist < 3) { //stop if bin is full (3 is an arbitrary max fullness value)
      Serial.println("stop");
      delay(3000);
    }
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
