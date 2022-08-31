/* 
 * File:   DCM2Angles.h
 * Author: kyleg
 *
 * Created on May 22, 2022, 2:09 PM
 */

#ifndef DCM2ANGLES_H
#define	DCM2ANGLES_H

// Convert DCM to pitch euler angle in degrees
float DCM2Pitch(float R[3][3]);

// Convert DCM to roll euler angle in degrees
float DCM2Roll(float R[3][3]);

// Convert DCM to yaw euler angle in degrees
float DCM2Yaw(float R[3][3]);

#endif
