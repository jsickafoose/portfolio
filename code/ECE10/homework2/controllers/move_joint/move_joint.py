"""move_joint controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import math
from controller import Supervisor


# create the Robot instance.

supervisor = Supervisor()
# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
# Initialize the arm motors and encoders.
motorNames = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', \
                'wrist_2_joint', 'wrist_3_joint']
motorDevices = []
for motorName in motorNames: 
    motor = supervisor.getDevice(motorName)
    motor.setPosition(0.0)
    motor.setVelocity(10.0)
    position_sensor = motor.getPositionSensor()
    position_sensor.enable(timestep)
    motorDevices.append(motor)

initialPos = [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5];
#initialPos = [0.0, -1.57, 0.0, 0.0, 1.57, 0.0];
    
 # Initial position
for i in range(len(motorDevices)):
    motorDevices[i].setPosition(initialPos[i])

#for i in range(len(motorDevices)):
#    motorDevices[i].setVelocity(0.0)
    
motionAxis = 0
#Enable vel control for the pan:
motorDevices[motionAxis].setVelocity(0.0)
motorDevices[motionAxis].setPosition(float('+inf'))

#Start the pan operation going:
motorDevices[motionAxis].setVelocity(1.0)

#Get the name of the end effector toolslot
endNode = supervisor.getFromDef("end_effector")


while supervisor.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    endPos = endNode.getPosition()
    endOrient = endNode.getOrientation()
    print('Motion angle:' + str(motorDevices[motionAxis].getPositionSensor().getValue() % (2*math.pi)))
    print(endPos)
    print(endOrient)
 

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
for i in range(len(motorDevices)):
    motorDevices[i].setVelocity(0.0)
