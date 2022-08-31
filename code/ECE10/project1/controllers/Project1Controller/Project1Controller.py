#####################################
# File:     Project1Controller.py   #
# Author:   Jacob Sickafoose        #
#                                   #
# Created on 4/15/22 @ 17:15        #
#####################################

## Imports the Robot, Motor, and DistanceSensor libraries
from controller import Robot, Motor, DistanceSensor



# create the Robot instance. I also named it MY_ROBOT
MY_ROBOT = Robot()
# get the time step of the current world.
timestep = int(MY_ROBOT.getBasicTimeStep())

## Setting up motors
maxMotorSpeed = 6.28 # Found in the datasheet
normalSpeed = maxMotorSpeed/4   # Running it slower so the distance sensors get a chance to read
                                # completely arbitrary

leftMotor = MY_ROBOT.getDevice('left wheel motor') # Instantiation
rightMotor = MY_ROBOT.getDevice('right wheel motor')

leftMotor.setPosition(float('inf'))     # I'm still not sure what this does if we still have to set velocity
rightMotor.setPosition(float('inf'))    # I'm guessing it sets the limit of rotation to be infinite so we can use velocity to determine everything

leftMotor.setVelocity(0)    # Starts the motors at velocity 0
rightMotor.setVelocity(0)



## Setting up distance sensors
ds7 = MY_ROBOT.getDevice('ps7')
ds0 = MY_ROBOT.getDevice('ps0')
ds5 = MY_ROBOT.getDevice('ps5')

ds7.enable(timestep) # Idk what this does either. I guess it just turns them on
ds0.enable(timestep) # I just don't know why it needs to know the timestep
ds5.enable(timestep)



## Provided code for pausing the robot for "duration" timed in seconds
def sleep(duration):
    #Waits for the duration seconds before returning.
    global MY_ROBOT # I'm still unsure of what this does or if it's necessary
    end_time = MY_ROBOT.getTime() + duration
    while MY_ROBOT.step(timestep) != -1 and MY_ROBOT.getTime() < end_time:
        pass



## Function for moving forward for code simplicity
def forward():
    leftMotor.setVelocity(normalSpeed)    # Motors on
    rightMotor.setVelocity(normalSpeed)

## Function to move backwards, only used in testing
def backward():
    leftMotor.setVelocity(-normalSpeed)    # Motors on, but in reverse
    rightMotor.setVelocity(-normalSpeed)

## Function for turning right, the only direction it needs
def turnRight():
    leftMotor.setVelocity(normalSpeed)    # Motors spin opposite to spin in place
    rightMotor.setVelocity(-normalSpeed)

##Turning right, but just a 180
def turnRight180():
    leftMotor.setVelocity(normalSpeed)    # Motors spin opposite to spin in place
    rightMotor.setVelocity(-normalSpeed)
    sleep(2.82) # Very carefully calculated amount of time to complete a 180 degree turn
    stop()      # Stops motors after 180 has been made

## Function for stopping both motors
def stop():
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)


state = 'Forward1' ## Initializing state
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while MY_ROBOT.step(timestep) != -1:
    ## Forward1 state, forward until wall detected
    if state == 'Forward1':
        print("Forward") # Announces the state
        forward() # Commencing forward motion

        # Stops moving forward if either sensor hits a high value
        while (MY_ROBOT.step(timestep) != -1 and (ds7.getValue()<82 and ds0.getValue()<82)):
            pass
        state = 'Turn180ThenForward' # Changes state

    ## Turn180ThenForward state, turns a 180 then moves forward again until wall detected
    elif state == 'Turn180ThenForward':
        print("Right180")
        turnRight180()
        forward()
        while (MY_ROBOT.step(timestep) != -1 and (ds7.getValue()<82 and ds0.getValue()<82)):
            pass
        state = 'Rotating'

    ## Rotating state, rotates indefinitely until left sensor reads the wall
    elif state == 'Rotating':
        print("Rotating")
        turnRight()
        while (MY_ROBOT.step(timestep) != -1 and ds5.getValue()<82):
            pass
        sleep(0.15) # I added a delay so the epuck turns more to point less into the wall, and more parallel with it
        state = 'Forward2'

    ## Forward2 state, move's forward again but this time stops when no wall detected on the left
    elif state == 'Forward2':
        print("Forward Again")
        forward()
        while (MY_ROBOT.step(timestep) != -1 and ds5.getValue()>76):
            pass
        state = 'WaitingForever'

    ## WaitingForever state, waits forever.
    # I know I could have just set line 121, state='WaitingForever' to just
    # be the while () pass, but I like it as a state
    elif state == 'WaitingForever':
        print("Waiting Forever")
        stop()
        while MY_ROBOT.step(timestep) != -1:
            pass

    ## This is only here if somehow the state variable becomes defined as something it shouldn't
    else:
        print("Error")