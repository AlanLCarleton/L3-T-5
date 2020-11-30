from sense_hat import SenseHat

sense = SenseHat()

directions = ["up", "down", "left", "right", "middle"]

def moveTest(direction):
    if direction not in directions:
        print("Not a valid direction")
        return
    moved = False
    while not moved:
        events = []
        while not events:
            events = sense.stick.get_events()
        for event in events:
            if event.action != "pressed":
                events.remove(event)
        for event in events:      
            if event.direction == direction:
                print("Joystick moved correctly.", direction, "direction detected.\n")
                moved = True
            else:
                print("Joystick moved incorrectly.", event.direction, "direction detected.")
    
print("Test 1: Please move joystick to the left")
moveTest("left")
print("Test 2: Please move joystick to the right")
moveTest("right")
print("Test 3: Please move joystick up")
moveTest("up")
print("Test 4: Please move joystick down")
moveTest("down")
print("Test 5: Please press joystick in the middle")
moveTest("middle")
print("All tests passed successfully!")