import math
from . import MatrixMath
#-------------------------------------------------------------------------------------------------------------------------
# DCM to Euler angle
def dcm2Euler(DCM):
    yaw = math.atan2(DCM[0][1], DCM[0][0])
    if (DCM[0][2] < -1): 
        pitch = -math.asin(-1)
    elif (DCM[0][2] > 1): 
        pitch = -math.asin(1)
    else:
        pitch = -math.asin(DCM[0][2])
    roll = math.atan2(DCM[1][2], DCM[2][2])

    EulerAngle = [yaw, pitch, roll]

    return EulerAngle
#-------------------------------------------------------------------------------------------------------------------------
def euler2DCM(yaw, pitch, roll):
    RotationRoll = [[1, 0, 0], [0, math.cos(roll), math.sin(roll)], [0, -math.sin(roll), math.cos(roll)]]
    RotationPitch = [[math.cos(pitch), 0, -math.sin(pitch)], [0, 1, 0], [math.sin(pitch), 0, math.cos(pitch)]]
    RotationYaw = [[math.cos(yaw), math.sin(yaw), 0], [-math.sin(yaw), math.cos(yaw), 0], [0, 0, 1]]

    DCM3x3 = MatrixMath.multiply(RotationRoll, MatrixMath.multiply(RotationPitch, RotationYaw)) 

    return DCM3x3
#-------------------------------------------------------------------------------------------------------------------------
def ned2enu(points):

    #NED to ENU
    Imatrix = [[0, 1, 0], [1, 0, 0], [0, 0, -1]]
    Ned2Transpose = MatrixMath.transpose(points) 
    enu = MatrixMath.multiply(Imatrix, Ned2Transpose)
    
    enuTranspose = MatrixMath.transpose(enu) 

    return enuTranspose
#-------------------------------------------------------------------------------------------------------------------------    