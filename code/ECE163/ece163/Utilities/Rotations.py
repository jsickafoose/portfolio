'''
Author: Jacob Sickafoose (jsickafo@ucsc.edu)
This file contains tools to perform rotations by producing rotation matrices.
'''

import math
from . import MatrixMath as mm


def euler2DCM(yaw, pitch, roll):
    """
		Function to apply the Direction Cosine Matrix to the supplied Euler angles and return the output matrix

		:param yaw: rotation about inertial down [rad]
		:param pitch: rotation about intermediate y-axis [rad]
		:param roll: rotation about body x-axis [rad]
		:return: Resulting matrix from Euler
	"""

    r_yaw = [[math.cos(yaw), math.sin(yaw), 0],
             [-math.sin(yaw), math.cos(yaw), 0],
             [0, 0, 1]]

    r_pitch = [[math.cos(pitch), 0, -math.sin(pitch)],
               [0, 1, 0],
               [math.sin(pitch), 0, math.cos(pitch)]]

    r_roll = [[1, 0, 0],
              [0, math.cos(roll), math.sin(roll)],
              [0, -math.sin(roll), math.cos(roll)]]

    return mm.multiply(mm.multiply(r_roll, r_pitch), r_yaw);  # Multiplies the three matrices together and returns


def dcm2Euler(dcm):
    """
		Function to get Euler angles from given DCM matrix

		:param dcm: DCM matrix
		:return: List of yaw, pitch, and roll
		# I found the equations for this in slide 24 of the Lecture01 slides
	"""
    yaw = math.atan2(dcm[0][1], dcm[0][0])
    if dcm[0][2] < -1:
        pitch = -math.asin(-1)
    elif dcm[0][2] > 1:
        pitch = -math.asin(1)
    else:
        pitch = -math.asin(dcm[0][2])
    roll = math.atan2(dcm[1][2], dcm[2][2])

    return [yaw, pitch, roll]  # Returns all variables as a list


def ned2enu(points):
    """
		Function to convert list of points in NED to points list in ENU

		:param points: List of points in North-East-Down format
		:return: Points in inertial EAST-NORTH-UP frame (for plotting)
	"""
	# This conversion matrix was solved for in the homework
    r_ned2enu = [[0, 1, 0],
                 [1, 0, 0],
                 [0, 0, -1]]
    return mm.multiply(points, r_ned2enu)

    # print("Here point 1 = ", points)
    # ENU = [points[1], points[0], -points[2]]	# I'm not really sure why this didn't work.
    # return EAST-NORTH-UP    					# The points variable is just too mysterious I guess.