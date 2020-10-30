
// Include Libraries
#include "Arduino.h"
#include "NewPing.h"
// Include the Arduino Stepper.h library:
#include <Stepper.h>

// Pin Definitions
#define HCSR04_PIN_TRIG	3
#define HCSR04_PIN_ECHO	2


// Global variables and defines

// define vars for testing menu
const int timeout = 50000;       //define timeout of 50 sec
char menuOption = 0;
long time0;
// number of steps per rotation:
const int stepsPerRevolution = 512;
long distance;

// object initialization
NewPing hcsr04(HCSR04_PIN_TRIG,HCSR04_PIN_ECHO);
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);


void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB
    Serial.println("start");

    // Set stepper motor speed to 12 rpm:
    myStepper.setSpeed(12);

    menuOption = menu();
    
}

// Main logic of circuit
void loop() 
{
    if(menuOption == '1') {
      // Ultrasonic Sensor - HC-SR04 - Test Code
      // Read distance measurment from UltraSonic sensor
      int hcsr04Dist;
      while (time0 + timeout > millis()) {
        hcsr04Dist = hcsr04.ping_cm();
        delay(50);
        //distance = hcsr04Dist;
        Serial.print(F("Distance: ")); Serial.print(hcsr04Dist); Serial.println(F("cm"));
        //Activate stepper motor if sensed distance is 6cm or less
        if (hcsr04Dist <= 6) {
          Serial.println("clockwise");
          myStepper.step(stepsPerRevolution);
        }
      }
      menuOption = menu();
    }
    else if(menuOption == '2') {
      // Step one revolution in one direction:
      Serial.println("clockwise");
      myStepper.step(stepsPerRevolution);
      delay(500);
      
      // Step one revolution in the other direction:
      Serial.println("counterclockwise");
      myStepper.step(-stepsPerRevolution);
      delay(500);

      menuOption = menu();
    }

    menuOption = menu();
        
}

// Menu function for selecting the components to be tested
// Follow serial monitor for instrcutions
char menu()
{

    Serial.println(F("\nWhich component would you like to test?"));
    Serial.println(F("(1) Ultrasonic Sensor - HC-SR04"));
    Serial.println(F("(2) Stepper Motor"));
    Serial.println(F("(menu) send anything else or press on board reset button\n"));
    while (!Serial.available());

    // Read data from serial monitor if received
    while (Serial.available()) 
    {
        char c = Serial.read();
        if (isAlphaNumeric(c)) 
        {
          if(c == '1') 
    			  Serial.println(F("Now Testing Ultrasonic Sensor - HC-SR04"));
    		  else if(c == '2') 
    			  Serial.println(F("Now Testing Stepper Motor"));
          else
          {
            Serial.println(F("illegal input!"));
            return 0;
          }
          time0 = millis();
          return c;
        }
    }
}
