from sense_hat import SenseHat
import time

sense = SenseHat()

red = [248, 0, 0]
green = [0, 248, 0]
blue = [0, 0, 248]
white = [248, 248, 248]

def set_pixels(colour):
    sense.clear()
    for x in range(8):
        for y in range(8):
            sense.set_pixel(x,y,colour)
            time.sleep(0.03)
            
def get_pixels(colour):
    for x in range(8):
        for y in range(8):
            if not sense.get_pixel(x,y) == colour:
                print("LED", x, y, "is not being read correctly!")
                return False
    sense.clear()
    return True

print("Testing Red LEDs")
set_pixels(red)
assert(get_pixels(red)), "Test Failed!"
print("Test Successful!")
print("Testing Green LEDs")
set_pixels(green)
assert(get_pixels(green)), "Test Failed!"
print("Test Successful!")
print("Testing Blue LEDs")
set_pixels(blue)
assert(get_pixels(blue)), "Test Failed!"
print("Test Successful!")
print("Testing White LEDs")
set_pixels(white)
assert(get_pixels(white)), "Test Failed!"
print("Test Successful!")
print("Testing incorrect LED values")
set_pixels(red)
assert(not get_pixels(white)), "Test Failed!"
print("Tests Successful!")
sense.clear()



            
