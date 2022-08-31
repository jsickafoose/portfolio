#############################################
#   Created by Jacob Sickafoose - jsickafo  #
#############################################

import math
import pickle
from ece163.Modeling import VehicleAerodynamicsModel
from ece163.Constants import VehiclePhysicalConstants as VPC
from ece163.Containers import States
from ece163.Containers import Inputs
from ece163.Containers import Controls
from ece163.Containers import Linearized
from ece163.Utilities import MatrixMath
from ece163.Utilities import Rotations



'''
Function to compute the control gains using the tuning parameters outlined in
Beard Chapter 6. Both the lateral and longitudinal gains are calculated. No
check is made for frequency separation. Transfer function input comes fromm the
VehiclePerturbationModels which rely on the VehicleTrim.py (provided) to compute
the trim values.

Parameters: tuningParameters – class controlTuning from Containers.Controls
            linearizedModel – class transferFunction from Containers.Linearized

Returns:    controlGains - class controlGains from Containers.Controls
'''
def computeGains(tuningParameters=Controls.controlTuning(), linearizedModel=Linearized.transferFunctions()):
    out = Controls.controlGains()

    out.kp_roll = (tuningParameters.Wn_roll**2) / linearizedModel.a_phi2 # Equation 6.5
    out.kd_roll = (2*tuningParameters.Zeta_roll*tuningParameters.Wn_roll - linearizedModel.a_phi1) / linearizedModel.a_phi2 # Equation 6.6
    out.ki_roll = 0.001 # Piazza
    
    out.kp_sideslip = (2*tuningParameters.Zeta_sideslip*tuningParameters.Wn_sideslip - linearizedModel.a_beta1) / linearizedModel.a_beta2 # Equation 6.15
    out.ki_sideslip = (tuningParameters.Wn_sideslip**2) / linearizedModel.a_beta2 # Equation 6.14

    out.kp_course = 2*tuningParameters.Zeta_course*tuningParameters.Wn_course * (linearizedModel.Va_trim/VPC.g0) # Equation 6.12
    out.ki_course = tuningParameters.Wn_course**2 * (linearizedModel.Va_trim / VPC.g0) # Equation 6.13

    out.kp_pitch = (tuningParameters.Wn_pitch**2 - linearizedModel.a_theta2) / linearizedModel.a_theta3 # Equation 6.19
    out.kd_pitch = (2*tuningParameters.Zeta_pitch*tuningParameters.Wn_pitch - linearizedModel.a_theta1) / linearizedModel.a_theta3 # Equation 6.20

    K_pitchDC = (out.kp_pitch*linearizedModel.a_theta3) / (tuningParameters.Wn_pitch**2) # Equation 6.23
    out.kp_altitude = (2*tuningParameters.Zeta_altitude*tuningParameters.Wn_altitude) / (K_pitchDC*linearizedModel.Va_trim) # Equation 6.25
    out.ki_altitude = (tuningParameters.Wn_altitude**2) / (K_pitchDC*linearizedModel.Va_trim) # Equation 6.24

    out.kp_SpeedfromThrottle = (2*tuningParameters.Zeta_SpeedfromThrottle*tuningParameters.Wn_SpeedfromThrottle - linearizedModel.a_V1) / (linearizedModel.a_V2) # Equation 6.30
    out.ki_SpeedfromThrottle = (tuningParameters.Wn_SpeedfromThrottle**2) / (linearizedModel.a_V2) # Equation 6.29

    out.kp_SpeedfromElevator = (linearizedModel.a_V1 - 2*tuningParameters.Zeta_SpeedfromElevator*tuningParameters.Wn_SpeedfromElevator) / (K_pitchDC*VPC.g0) # Equation 6.28
    out.ki_SpeedfromElevator = -(tuningParameters.Wn_SpeedfromElevator**2) / (K_pitchDC*VPC.g0) # Equation 6.27

    return out


'''
Function to compute the tuning parameters given the gains in the successive
loop closure, needs a try block to deal with taking square root of negative
number. Function should never fail, if an exception occurs, return an empty
(inited) turningParameters class. Transfer function input comes from the
VehiclePerturbationModels which rely on the VehicleTrim.py (provided) to
compute the trim values.

Parameters: controlGains – class controlGains from Containers.Controls
            linearizedModel – class transferFunction from Containers.Linearized
 
Returns:    tuningParameters - class controlTuning from Containers.Controls
'''
def computeTuningParameters(controlGains=Controls.controlGains(), linearizedModel=Linearized.transferFunctions()):
    out = Controls.controlTuning()

    out.Wn_roll = math.sqrt(controlGains.kp_roll*linearizedModel.a_phi2) # Equation 6.5
    out.Zeta_roll = (linearizedModel.a_phi1 + controlGains.kd_roll*linearizedModel.a_phi2) / (2*out.Wn_roll) # Equation 6.6

    out.Wn_course = math.sqrt(controlGains.ki_course / (linearizedModel.Va_trim/VPC.g0)) # Equation 6.13
    out.Zeta_course = (controlGains.kp_course / (linearizedModel.Va_trim/VPC.g0)) / (2*out.Wn_course) # Equation 6.12

    out.Wn_sideslip = math.sqrt(linearizedModel.a_beta2*controlGains.ki_sideslip) # Equation 6.14
    out.Zeta_sideslip = (linearizedModel.a_beta1 + linearizedModel.a_beta2*controlGains.kp_sideslip) / (2*out.Wn_sideslip) # Equation 6.15

    out.Wn_pitch = math.sqrt(linearizedModel.a_theta2 + controlGains.kp_pitch*linearizedModel.a_theta3) # Equation 6.19
    out.Zeta_pitch = (linearizedModel.a_theta1 + controlGains.kd_pitch*linearizedModel.a_theta3) / (2*out.Wn_pitch) # Equation 6.20

    K_pitchDC = (controlGains.kp_pitch*linearizedModel.a_theta3) / (out.Wn_pitch**2) # Equation 6.23
    out.Wn_altitude = math.sqrt(K_pitchDC*linearizedModel.Va_trim*controlGains.ki_altitude) # Equation 6.24
    out.Zeta_altitude = (controlGains.kp_altitude*K_pitchDC*linearizedModel.Va_trim) / (2*out.Wn_altitude) # Equation 6.25

    out.Wn_SpeedfromThrottle = math.sqrt(controlGains.ki_SpeedfromThrottle*linearizedModel.a_V2) # Equation 6.29
    out.Zeta_SpeedfromThrottle = (controlGains.kp_SpeedfromThrottle*linearizedModel.a_V2 + linearizedModel.a_V1) / (2*out.Wn_SpeedfromThrottle) # Equation 6.30

    out.Wn_SpeedfromElevator = math.sqrt(controlGains.ki_SpeedfromElevator*-K_pitchDC*VPC.g0) # Equation 6.27
    out.Zeta_SpeedfromElevator = (controlGains.kp_SpeedfromElevator*K_pitchDC*VPC.g0 - linearizedModel.a_V1) / -(2*out.Wn_SpeedfromElevator) # Equation 6.28

    return out