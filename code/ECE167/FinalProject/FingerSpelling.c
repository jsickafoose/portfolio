/*
 * File:   FingerSpelling.c
 * Author: jsickafo
 *
 * Created on June 6, 2022, 2:30 PM
 */


#include <xc.h>
#include <BOARD.h>
#include "FingerSpelling.h"
#include <sys/attribs.h>

// Enums available to use from the header file
//typedef enum {
//    STRAIGHT = 0,
//    HALF = 1, 
//    CURLED = 2
//} FingerStates;
//
//typedef enum {
//    THUMB = 0,
//    INDEX = 1, 
//    MIDDLE = 2,
//    RING = 3,
//    PINKY = 4
//} FingerIndex;

// These two #defines are available for each of the 5 fingers
//#define finger_0_straight_min   1
//#define finger_0_curled_max     1
FingerStates setFingerState(int flexAngle, FingerIndex FingerNumber){
    int state;
    //// Checks for what state each finger is in
    // Finger 0
    if (FingerNumber == THUMB){
        if (flexAngle > finger_0_straight_min){
            state = STRAIGHT;
        }
        else if (flexAngle < finger_0_curled_max){
            state = CURLED;
        }
        else{
            state = HALF;
        }
    }
    // Finger 1
    else if (FingerNumber == INDEX){
        if (flexAngle > finger_1_straight_min){
            state = STRAIGHT;
        }
        else if (flexAngle < finger_1_curled_max){
            state = CURLED;
        }
        else{
            state = HALF;
        }
    }
    // Finger 2
    else if (FingerNumber == MIDDLE){
        if (flexAngle > finger_2_straight_min){
            state = STRAIGHT;
        }
        else if (flexAngle < finger_2_curled_max){
            state = CURLED;
        }
        else{
            state = HALF;
        }
    }
    // Finger 3
    else if (FingerNumber == RING){
        if (flexAngle > finger_3_straight_min){
            state = STRAIGHT;
        }
        else if (flexAngle < finger_3_curled_max){
            state = CURLED;
        }
        else{
            state = HALF;
        }
    }
    // Finger 4
    else{
        if (flexAngle > finger_4_straight_min){
            state = STRAIGHT;
        }
        else if (flexAngle < finger_4_curled_max){
            state = CURLED;
        }
        else{
            state = HALF;
        }
    }
    
    return state;
}


char getLetter(FingerStates THUMB, FingerStates INDEX, FingerStates MIDDLE, FingerStates RING, FingerStates PINKY){
    char output = 'Z';
    
    // NUMBERS
    // 1: Flex thumb, pinky, ring, and middle
    if (THUMB == CURLED && INDEX == STRAIGHT && MIDDLE == CURLED && RING == CURLED && PINKY == CURLED){
        output = '1';
    }
    // 2: Flex Middle, ring, and thumb
    else if (THUMB == CURLED && INDEX == STRAIGHT && MIDDLE == STRAIGHT && RING == CURLED && PINKY == CURLED){
        output = '2';
    }
    // 3: Flex Ring and pinky
    else if (THUMB == STRAIGHT && INDEX == STRAIGHT && STRAIGHT == CURLED && RING == CURLED && PINKY == CURLED){
        output = '3';
    }
    // 4: Flex thumb against light threshold
    else if (THUMB == CURLED && INDEX == STRAIGHT && MIDDLE == STRAIGHT && RING == STRAIGHT && PINKY == STRAIGHT){
        output = '4';
    }
    // 5: Nothing flexed
    else if (THUMB == STRAIGHT && INDEX == STRAIGHT && MIDDLE == STRAIGHT && RING == STRAIGHT && PINKY == STRAIGHT){
        output = '5';
    }
    // 6: Flex pinky and thumb
    else if (THUMB == CURLED && INDEX == STRAIGHT && MIDDLE == STRAIGHT && RING == STRAIGHT && PINKY == CURLED){
        output = '6';
    }
    // 7: Flex ring and thumb
    else if (THUMB == CURLED && INDEX == STRAIGHT && MIDDLE == STRAIGHT && RING == CURLED && PINKY == STRAIGHT){
        output = '7';
    }
    // 8: Flex middle and thumb
    else if (THUMB == CURLED && INDEX == STRAIGHT && MIDDLE == CURLED && RING == STRAIGHT && PINKY == STRAIGHT){
        output = '8';
    }
    // 9: Flex index and thumb
    else if (THUMB == CURLED && INDEX == CURLED && MIDDLE == STRAIGHT && RING == STRAIGHT && PINKY == STRAIGHT){
        output = '9';
    }
    // LETTERS
    // A: Flex index and thumb
    else if (THUMB == STRAIGHT && INDEX == CURLED && MIDDLE == CURLED && RING == CURLED && PINKY == CURLED){
        output = 'A';
    }
    // C: Flex index and thumb
    else if (THUMB == HALF && INDEX == HALF && MIDDLE == HALF && RING == HALF && PINKY == HALF){
        output = 'C';
    }
    // I: Flex index and thumb
    else if (THUMB == CURLED && INDEX == CURLED && MIDDLE == CURLED && RING == CURLED && PINKY == STRAIGHT){
        output = 'I';
    }
    // X: Flex index and thumb
    else if (THUMB == CURLED && INDEX == HALF && MIDDLE == CURLED && RING == CURLED && PINKY == CURLED){
        output = 'X';
    }
    // Y: Flex index and thumb
    else if (THUMB == STRAIGHT && INDEX == CURLED && MIDDLE == CURLED && RING == CURLED && PINKY == STRAIGHT){
        output = 'Y';
    }
    
    return output;
}
