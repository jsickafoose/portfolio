import math
import random
import numpy as np
from ece163.Modeling import VehicleAerodynamicsModel as VDM
from ece163.Constants import VehiclePhysicalConstants as VPC
from ece163.Constants import VehicleSensorConstants as VSC
from ece163.Modeling import VehicleAerodynamicsModel as VAM
from ece163.Controls import VehicleClosedLoopControl as VCL
from ece163.Controls import VehicleControlGains as VCG
from ece163.Controls import VehiclePerturbationModels as VPM
from ece163.Modeling import WindModel as WM
from ece163.Sensors import SensorsModel as SM
from ece163.Containers import States
from ece163.Containers import Inputs
from ece163.Containers import Sensors
from ece163.Containers import Controls
from ece163.Containers import Linearized
from ece163.Utilities import MatrixMath
from ece163.Utilities import Rotations

'''
Orbit Follow / Algorith 4 / Texbook page 184
OrbitCetner --> TargetState
MAVState --> MAVState
Korbit --> gains Korbit
'''
#     return Hc, Xc
def FollowOrbit(TargetState, rho, lmbda, MAVState, Korbit):
    Hc = -TargetState.pd

    d = math.sqrt(((MAVState.pn - TargetState.pn)**2) + ((MAVState.pe - TargetState.pe)**2))
    yaw = math.atan2(MAVState.pe - TargetState.pe, MAVState.pn - TargetState.pn)

    #not sure about X.chi
    while yaw - MAVState.chi < -math.pi:
        yaw += 2*math.pi
    while yaw - MAVState.chi > math.pi:
        yaw -=  2*math.pi
    
    Xc = yaw + lmbda * (((math.pi)/2) + math.atan(Korbit*(((d-rho)/rho))))


    return Hc, Xc