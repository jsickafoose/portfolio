// DCM2Angles.c
// Lab 4
#include "MatrixMath.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "BOARD.h"

#define pi 3.142857

//Returns Euler angles from DCM
float DCM2Pitch(float R[3][3]){
    float Pitch;
    // Check if R[0][2] position is out of bounds +1,-1
    if(R[0][2] < -1){
        Pitch = -asin(-1);
    }
    else if(R[0][2] > 1){
        Pitch = -asin(1);
    }
    else{
        Pitch = -asin(R[0][2]);
    }
    return Pitch * (180/pi);  // Convert from radians to degrees
}

float DCM2Roll(float R[3][3]){
    float Roll = atan2(R[1][2],R[2][2]);
    return Roll * (180/pi);  // Convert from radians to degrees
}

float DCM2Yaw(float a[3][3]){
    float Yaw = atan2(a[0][1],a[0][0]);
    return Yaw * (180/pi);  // Convert from radians to degrees
}


//#define TESTING_DCM 1
#ifdef TESTING_DCM
int main(void){
    BOARD_Init();
    while(1);
}
#endif