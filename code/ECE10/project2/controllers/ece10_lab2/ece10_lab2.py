"""ece10_lab2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import math
from controller import Robot, Motor, DistanceSensor
import os

# Ground Sensor Measurements under this threshold are black
# measurements above this threshold can be considered white.
# TODO: Fill this in with a reasonable threshold that separates "line detected" from "no line detected"
GROUND_SENSOR_THRESHOLD = 400

# These are your pose values that you will update by solving the odometry equations
pose_x     = -3.03083e-08  # Meters
pose_y     = 0  # Meters
pose_theta = -1.65806  # Radians

# Index into ground_sensors and ground_sensor_readings for each of the 3 onboard sensors.
LEFT_IDX   = 2
CENTER_IDX = 1
RIGHT_IDX  = 0

# create the Robot instance.
robot = Robot()

# ePuck Constants
EPUCK_AXLE_DIAMETER = 0.053     # ePuck's wheels are 53mm apart.
EPUCK_MAX_WHEEL_SPEED = 0.126   # Found by calculating distance over time b/c it seemed like we had to
                                # calculating with the specs given shows it should be 0.1287 but I'm splitting hairs
MAX_SPEED = 6.28                # Radians/Second
EPUCK_WHEEL_RADIUS = 0.0205     # I had to find this, ePuck wheel radius is 20.5mm

# get the time step of the current world.
SIM_TIMESTEP = int(robot.getBasicTimeStep())

# Initialize Motors
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# Initialize and Enable the Ground Sensors
gsr = [0, 0, 0]
ground_sensors = [robot.getDevice('gs0'), robot.getDevice('gs1'), robot.getDevice('gs2')]
for gs in ground_sensors:
    gs.enable(SIM_TIMESTEP)

# Allow sensors to properly initialize
for i in range(10): robot.step(SIM_TIMESTEP)  

vL = 0 # TODO: Initialize variable for left speed, radians/sec
vR = 0 # TODO: Initialize variable for right speed, radians/sec


###### Added Functions for code simplicity
def forward(speed):
    vL = MAX_SPEED/speed
    vR = MAX_SPEED/speed
    return vL, vR
def turnLeft(speed):
    vL = -MAX_SPEED/speed
    vR = MAX_SPEED/speed
    return vL, vR
def turnRight(speed):
    vL = MAX_SPEED/speed
    vR = -MAX_SPEED/speed
    return vL, vR

def leftDetected():
    if gsr[0]<GROUND_SENSOR_THRESHOLD:
        return True
    else:
        return False
def centerDetected():
    if gsr[1]<GROUND_SENSOR_THRESHOLD:
        return True
    else:
        return False
def rightDetected():
    if gsr[2]<GROUND_SENSOR_THRESHOLD:
        return True
    else:
        return False
def lineDetected(): # Really just means all sensors see the start line
    if gsr[0]<GROUND_SENSOR_THRESHOLD and gsr[1]<GROUND_SENSOR_THRESHOLD and gsr[2]<GROUND_SENSOR_THRESHOLD:
        return True
    else:
        return False

## My implementation of updating the odometry
def update_odometry(x, y, theta, dT):
    ### Implementing equation 3.33 in the textbook to apply the transformation matrix
    left_dist = (vL/MAX_SPEED)*EPUCK_MAX_WHEEL_SPEED  # Except with the measured wheelspeed, not theoretical max
    right_dist = (vR/MAX_SPEED)*EPUCK_MAX_WHEEL_SPEED # which would have been found with the arc length like the book does

    T = [[math.cos(theta), -math.sin(theta), 0], # Transform matrix
         [math.sin(theta), math.cos(theta) , 0],
         [0              , 0               , 1]]

    R = [[(left_dist)/2 + (right_dist)/2], # Second matrix in 3.33
         [0],
         [(left_dist)/EPUCK_AXLE_DIAMETER - (right_dist)/EPUCK_AXLE_DIAMETER]]

    # Setting Outputs to the matrix math, Transform matrix multiplied by the robot's coords
    x_dot     = T[0][0]*R[0][0] + T[0][1]*R[1][0] + T[0][2]*R[2][0]
    y_dot     = T[1][0]*R[0][0] + T[1][1]*R[1][0] + T[1][2]*R[2][0]
    theta_dot = T[2][0]*R[0][0] + T[2][1]*R[1][0] + T[2][2]*R[2][0]

    # Performing the integration
    dT /= 1000.0    # Converts the timestep to seconds
    
    x     += x_dot*dT # Adding distance traveled over time step to last x, y, theta value
    y     -= y_dot*dT
    theta -= theta_dot*dT
    
    # Resets theta if it rolls over    
    if theta > math.pi:
        theta = -math.pi
    elif theta < -math.pi:
        theta = math.pi

    return x, y, theta



start = True ## Flag for the very start, looking for the line

## Variables and flags for closing the loop at the start line
lineSamples = 0
firstLineSighting = True
lastLinePose_x = 0
lastLinePose_y = 0
lastLinePose_theta = 0
# Main Control Loop:
while robot.step(SIM_TIMESTEP) != -1:

    # Read ground sensor values
    for i, gs in enumerate(ground_sensors):
        gsr[i] = gs.getValue()

    # print(gsr) # TODO: Uncomment to see the ground sensor values!

    
    # Hints: 
    #
    # 1) Setting vL=MAX_SPEED and vR=-MAX_SPEED lets the robot turn
    #    in place. vL=MAX_SPEED and vR=0.5*MAX_SPEED makes the
    #    robot drive a right curve.
    #
    # 2) If your robot "overshoots", turn slower.
    #
    # 3) Only set the wheel speeds once so that you can use the speed
    #    that you calculated in your odometry calculation.
    #
    # 4) Remove all console output to speed up simulation of the robot
    # TODO: Insert Line Following Code Here
    if start:               # When it first starts, no line = go forward
        vL, vR = forward(3) # The rest of the time, no line = ccw rotation
        if centerDetected():
            start = False
    else:
        if centerDetected():    # If the center is detected, ignore the other 2 sensors and go forward
            vL, vR = forward(3)
            if lineDetected():  # Only checks for startline while going forward
                lineSamples+=1  # And increments samples rather than sets a flag
        elif rightDetected():
            vL, vR = turnRight(3)
        else:                       # Turns left if the other two sensors are not detected, not if the left sensor is detected
            vL, vR = turnLeft(3)    # so it turns left if no line is seen


    # Hints:
    #
    # 1) Divide vL/vR by MAX_SPEED to normalize, then multiply with
    # the robot's maximum speed in meters per second. 
    #
    # 2) SIM_TIMESTEP tells you the elapsed time per step. You need
    # to divide by 1000.0 to convert it to seconds
    #
    # 3) Do simple checks to make sure things are working. In the beginning, 
    #    only one value changes. Once you do a right turn, this value should be constant.
    #
    # 4) Focus on getting things generally right first, then worry
    #    about calculating odometry in the world coordinate system of the
    #    Webots simulator first (x points down, y points right)
    # TODO: Call update_odometry Here
    pose_x, pose_y, pose_theta = update_odometry(pose_x, pose_y, pose_theta, SIM_TIMESTEP) # Just calls the function and sets variables


    # Hints:
    #
    # 1) Set a flag whenever you encounter the line
    #
    # 2) Use the pose when you encounter the line last 
    #    for best results
    # TODO: Insert Loop Closure Code Here
    if lineSamples > 8: # Initially getting on the track triggers 7 of these lineSamples
        if not lineDetected():                      # Changes only go into affect after the start line
            if firstLineSighting:                   # If it's the first time
                lastLinePose_x = pose_x             # just store values
                lastLinePose_y = pose_y
                lastLinePose_theta = pose_theta
                firstLineSighting = False           # And lower the first time flag
            else:
                temp_x = pose_x                     # Store the current pose to set it next loop, I wasn't sure if we do this or just continually reset the variables to the beginning startline pose but this was the impression I got
                temp_y = pose_y
                temp_theta = pose_theta

                pose_x = lastLinePose_x
                pose_y = lastLinePose_y
                pose_theta = lastLinePose_theta

                lastLinePose_x = temp_x
                lastLinePose_y = temp_y
                lastLinePose_theta = temp_theta

            lineSamples = 0     # Reset samples regardless of first line sighting or not, but only after the end of the startline


    print("Current pose: [%5f, %5f, %5f]" % (pose_x, pose_y, pose_theta))
    leftMotor.setVelocity(vL)
    rightMotor.setVelocity(vR)