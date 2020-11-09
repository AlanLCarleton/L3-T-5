#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()

    while True:
        print("\nWhich component would you like to test?\n")
        print("(1) Ultrasonic Sensor - HC-SR04\n")
        print("(2) Stepper Motor\n")
        print("(3) FS90R Servo Motor\n")
        print("(menu) send anything else or press on board reset button\n")
        option = str(input())
        ser.write(option.encode('utf-8'))
        #line = ser.readline().decode('utf-8').rstrip()
        #print(line)