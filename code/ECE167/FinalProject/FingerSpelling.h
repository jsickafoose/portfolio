/*
 * File:   FingerSpelling.h
 * Author: jsickafo
 *
 * Software module to convert flex sensor values from sign language symbols to alphanumerics.
 *
 * Created on June 6, 2022, 2:30 PM
 */

/*
 chipKIT Pin Usage
 * IMU I2C Pins:
 *  pin A0 = Finger0(Ring) Flex sensor
 *  pin A1 = Finger1(Middle) Flex sensor
 *  pin A2 = Finger2(Pinky) Flex sensor
 *  pin A3 = Finger3(Thumb) Flex sensor
 *  pin A5 = Finger4() Flex sensor
 */

#ifndef FingerSpelling_H
#define FingerSpelling_H

/*******************************************************************************
 * Private #DEFINES and ENUMS, do not change                                                             *
 ******************************************************************************/

// The states the fingers could be in
typedef enum {
    STRAIGHT = 0,
    HALF = 1, 
    CURLED = 2
} FingerStates;

typedef enum {
    THUMB = 0,
    INDEX = 1, 
    MIDDLE = 2,
    RING = 3,
    PINKY = 4
} FingerIndex;

// Thresholds for the different potentiometers
// Finger 0
#define finger_0_straight_min   45
#define finger_0_curled_max     28

// Finger 1
#define finger_1_straight_min   1000
#define finger_1_curled_max     840

// Finger 2
#define finger_2_straight_min   1005
#define finger_2_curled_max     980

// Finger 3
#define finger_3_straight_min   850
#define finger_3_curled_max     555

// Finger 4
#define finger_4_straight_min   1020
#define finger_4_curled_max     1005

/*******************************************************************************
 * PUBLIC FUNCTION PROTOTYPES                                                  *
 ******************************************************************************/
FingerStates setFingerState(int flexAngle, FingerIndex FingerNumber);

char getLetter(FingerStates finger0, FingerStates finger1, FingerStates finger2, FingerStates finger3, FingerStates finger4);


#endif