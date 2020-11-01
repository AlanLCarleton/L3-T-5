
// Include Libraries
#include "Arduino.h"
#include "NewPing.h"
// Include the Arduino Servo.h library:
#include "Servo.h"

// Pin Definitions
#define HCSR04_PIN_TRIG	3
#define HCSR04_PIN_ECHO	2
#define SERVO360MICRO_1_PIN_SIG  9
#define SERVO360MICRO_2_PIN_SIG  10


// Global variables and defines

// define vars for testing menu
const int timeout = 15000;       //define timeout of 15 sec
char menuOption = 0;
long time0;

// object initialization
NewPing hcsr04(HCSR04_PIN_TRIG,HCSR04_PIN_ECHO);
Servo servo360Micro_1;
Servo servo360Micro_2;

void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB
    Serial.println("start");
    
    servo360Micro_1.attach(SERVO360MICRO_1_PIN_SIG); // attach servo 1 to pin to control it.
    servo360Micro_1.write(90);  // stoped
    delay(100);
    servo360Micro_2.attach(SERVO360MICRO_2_PIN_SIG); // attach servo 2 to pin to control it.
    servo360Micro_2.write(90);  // stoped
    delay(100);
    
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
        //Activate servo if sensed distance is 6cm or less
        if (hcsr04Dist <= 6) {
          servo360Micro_1.writeMicroseconds(1820); // clockwise
          delay(195); // time delay of 195ms with speed of 1180 is a quarter (360) turn of the servo
          servo360Micro_1.writeMicroseconds(1500); // stopped
        }
      }
      menuOption = menu();
    }
    else if(menuOption == '2') {
      servo360Micro_1.writeMicroseconds(1180); // set servo speed (counter clockwise)
      delay(195); // time delay of 195ms with speed of 1180 is a quarter (360) turn of the servo
      servo360Micro_1.writeMicroseconds(1500); // stopped
      delay(1000);
      
      servo360Micro_1.writeMicroseconds(1180);
      delay(195);
      servo360Micro_1.writeMicroseconds(1500);
      delay(1000);
      
      servo360Micro_1.writeMicroseconds(1180);
      delay(195);
      servo360Micro_1.writeMicroseconds(1500);
      delay(1000);
      
      servo360Micro_1.writeMicroseconds(1180);
      delay(195);
      servo360Micro_1.writeMicroseconds(1500);
      delay(1000);

      menuOption = menu();
    }
    else if(menuOption == '3') {
      servo360Micro_2.writeMicroseconds(1180); // set servo speed (counter clockwise)
      delay(397); // time delay of 397ms with speed of 1180 is a half (360) turn of the servo
      servo360Micro_2.writeMicroseconds(1500); // stopped
      delay(1500);

      servo360Micro_2.writeMicroseconds(1790); // counter clockwise
      delay(390); // time delay of 390ms with speed of 1180 is a half (360) turn of the servo
      servo360Micro_2.writeMicroseconds(1500); // stopped
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
    Serial.println(F("(2) FS90R Servo Motor #1"));
    Serial.println(F("(3) FS90R Servo Motor #2"));
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
    			  Serial.println(F("Now Testing FS90R Servo Motor #1"));
          else if(c == '3') 
            Serial.println(F("Now Testing FS90R Servo Motor #2"));
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
