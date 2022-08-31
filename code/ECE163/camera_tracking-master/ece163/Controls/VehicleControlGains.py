"""
Duseok Choi
"""
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

def computeGains(tuningParameters=Controls.controlTuning(), linearizedModel=Linearized.transferFunctions()):
    controlGains = Controls.controlGains()

    Wn_roll = tuningParameters.Wn_roll
    Zeta_roll = tuningParameters.Zeta_roll
    Wn_course = tuningParameters.Wn_course
    Zeta_course = tuningParameters.Zeta_course
    Wn_sideslip = tuningParameters.Wn_sideslip
    Zeta_sideslip = tuningParameters.Zeta_sideslip
    Wn_pitch = tuningParameters.Wn_pitch
    Zeta_pitch = tuningParameters.Zeta_pitch
    Wn_altitude = tuningParameters.Wn_altitude
    Zeta_altitude = tuningParameters.Zeta_altitude
    Wn_SpeedfromElevator = tuningParameters.Wn_SpeedfromElevator
    Zeta_SpeedfromElevator = tuningParameters.Zeta_SpeedfromElevator
    Wn_SpeedfromThrottle = tuningParameters.Wn_SpeedfromThrottle
    Zeta_SpeedfromThrottle = tuningParameters.Zeta_SpeedfromThrottle
  
    a_phi1 = linearizedModel.a_phi1
    a_phi2 = linearizedModel.a_phi2
    a_beta1 = linearizedModel.a_beta1
    a_beta2 = linearizedModel.a_beta2
    a_theta1 = linearizedModel.a_theta1
    a_theta2 = linearizedModel.a_theta2
    a_theta3 = linearizedModel.a_theta3
    a_V1 = linearizedModel.a_V1
    a_V2 = linearizedModel.a_V2
    Va_trim = linearizedModel.Va_trim

    #Roll Attitude------------------------------------------------------------------------------------------
    #eq6.5
    controlGains.kp_roll = (Wn_roll ** 2) / a_phi2 
    #Meg section
    controlGains.ki_roll = 0.001 
    #eq6.6
    controlGains.kd_roll = ((2 * Zeta_roll * Wn_roll) - a_phi1) / a_phi2 
    #--------------------------------------------------------------------------------------------------------

    # Course Hold--------------------------------------------------------------------------------------------
    #eq6.12
    controlGains.kp_course = (2 * Zeta_course * Wn_course) * (Va_trim / VPC.g0)
    #eq6.13
    controlGains.ki_course = (Wn_course ** 2) * (Va_trim / VPC.g0) 
    #--------------------------------------------------------------------------------------------------------

    #Sideslip Hold-------------------------------------------------------------------------------------------    
    #eq6.14
    controlGains.ki_sideslip = (Wn_sideslip ** 2) / a_beta2
    #eq6.15
    controlGains.kp_sideslip = ((2 * Zeta_sideslip * Wn_sideslip) - a_beta1) / a_beta2 
    #--------------------------------------------------------------------------------------------------------

    #Pitch Attitude Hold------------------------------------------------------------------------------------
    #eq6.19
    controlGains.kp_pitch = ((Wn_pitch ** 2) - a_theta2) / a_theta3 
    #eq6.20
    controlGains.kd_pitch = ((2 * Zeta_pitch * Wn_pitch) - a_theta1) / a_theta3 
    #eq6.23
    kp_pitch = controlGains.kp_pitch
    Kpitch_DC = (kp_pitch * a_theta3) / (Wn_pitch ** 2) #wn_pitch = a_theta2 + (kp_pitch*a_theta3), already set in control.py
    #---------------------------------------------------------------------------------------------------------

    #Altitude Hold Using Commanded Pitch----------------------------------------------------------------------
    #eq6.24
    controlGains.ki_altitude = (Wn_altitude ** 2) / (Kpitch_DC * Va_trim)
    #eq6.25
    controlGains.kp_altitude = (2 * Zeta_altitude * Wn_altitude) / (Kpitch_DC * Va_trim) 
    #---------------------------------------------------------------------------------------------------------

    # Airspeed Hold Using Commanded Pitch---------------------------------------------------------------------
    #eq6.27
    controlGains.ki_SpeedfromElevator = -((Wn_SpeedfromElevator ** 2) / (Kpitch_DC * VPC.g0)) 
    #eq6.28
    controlGains.kp_SpeedfromElevator = (a_V1 - (2 * Zeta_SpeedfromElevator * Wn_SpeedfromElevator)) / (Kpitch_DC * VPC.g0)
    #---------------------------------------------------------------------------------------------------------

    #Airspeed Hold Using Throttle-----------------------------------------------------------------------------
    #eq6.29
    controlGains.ki_SpeedfromThrottle = (Wn_SpeedfromThrottle ** 2) / a_V2 
    #eq6.30
    controlGains.kp_SpeedfromThrottle = ((2 * Zeta_SpeedfromThrottle * Wn_SpeedfromThrottle) - a_V1) / a_V2
    #---------------------------------------------------------------------------------------------------------

    return controlGains

def computeTuningParameters(controlGains=Controls.controlGains(), linearizedModel=Linearized.transferFunctions()):

    controlTuning = Controls.controlTuning()

    kp_roll = controlGains.kp_roll
    kd_roll = controlGains.kd_roll
    kp_course = controlGains.kp_course
    ki_course = controlGains.ki_course
    kp_sideslip = controlGains.kp_sideslip
    ki_sideslip = controlGains.ki_sideslip
    kp_pitch = controlGains.kp_pitch
    kd_pitch = controlGains.kd_pitch
    kp_altitude = controlGains.kp_altitude
    ki_altitude = controlGains.ki_altitude
    kp_SpeedfromElevator = controlGains.kp_SpeedfromElevator
    ki_SpeedfromElevator = controlGains.ki_SpeedfromElevator
    kp_SpeedfromThrottle = controlGains.kp_SpeedfromThrottle
    ki_SpeedfromThrottle = controlGains.ki_SpeedfromThrottle
    
    a_phi1 = linearizedModel.a_phi1
    a_phi2 = linearizedModel.a_phi2
    a_beta1 = linearizedModel.a_beta1
    a_beta2 = linearizedModel.a_beta2
    a_theta1 = linearizedModel.a_theta1
    a_theta2 = linearizedModel.a_theta2
    a_theta3 = linearizedModel.a_theta3
    a_V1 = linearizedModel.a_V1
    a_V2 = linearizedModel.a_V2
    Va_trim = linearizedModel.Va_trim

    #eq6.5
    controlTuning.Wn_roll = math.sqrt(kp_roll * a_phi2) # Page 36 solving for Wn_roll
    #eq6.6
    Wn_roll = controlTuning.Wn_roll
    controlTuning.Zeta_roll = (a_phi1 + (kd_roll * a_phi2)) / (2 * Wn_roll) 

    #eq6.13
    controlTuning.Wn_course = math.sqrt(ki_course / (Va_trim / VPC.g0)) 
    #eq6.12
    Wn_course = controlTuning.Wn_course
    controlTuning.Zeta_course = (kp_course / (Va_trim / VPC.g0)) / (2 * Wn_course) 

    #eq6.14
    controlTuning.Wn_sideslip = math.sqrt(a_beta2 * ki_sideslip)
    #eq6.15
    Wn_sideslip = controlTuning.Wn_sideslip
    controlTuning.Zeta_sideslip = (a_beta1 + (a_beta2 * kp_sideslip)) / (2 * Wn_sideslip) 

    #eq6.19
    controlTuning.Wn_pitch = math.sqrt(a_theta2 + (kp_pitch * a_theta3)) 
    #eq.6.20
    Wn_pitch = controlTuning.Wn_pitch
    controlTuning.Zeta_pitch = (a_theta1 + (kd_pitch * a_theta3)) / (2 * Wn_pitch) 
    #eq6.23
    Kpitch_DC = (kp_pitch * a_theta3) / (Wn_pitch ** 2) #wn_pitch = a_theta2 + (kp_pitch*a_theta3), already set in control.py

    #ea6.24
    controlTuning.Wn_altitude = math.sqrt(Kpitch_DC * Va_trim * ki_altitude)
    #eq6.25
    Wn_altitude = controlTuning.Wn_altitude
    controlTuning.Zeta_altitude = (kp_altitude * Kpitch_DC * Va_trim) / (2 * Wn_altitude)

    #eq6.27
    controlTuning.Wn_SpeedfromElevator = math.sqrt(ki_SpeedfromElevator * -Kpitch_DC * VPC.g0) 
    #eq6.28
    Wn_SpeedfromElevator = controlTuning.Wn_SpeedfromElevator
    controlTuning.Zeta_SpeedfromElevator = ((kp_SpeedfromElevator * Kpitch_DC * VPC.g0) - a_V1) / -(2 * Wn_SpeedfromElevator) 

    #eq6.29
    controlTuning.Wn_SpeedfromThrottle = math.sqrt(ki_SpeedfromThrottle * a_V2) 
    #eq6.30
    Wn_SpeedfromThrottle = controlTuning.Wn_SpeedfromThrottle
    controlTuning.Zeta_SpeedfromThrottle = ((kp_SpeedfromThrottle * a_V2) + a_V1) / (2 * Wn_SpeedfromThrottle)


    return controlTuning
