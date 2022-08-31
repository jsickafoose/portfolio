// OpenLoop.c
// Lab 4
#include <stdio.h>
#include <stdlib.h>
#include <xc.h>
#include <sys/attribs.h>

#include "BNO055.h"
#include "BOARD.h"
#include "I2C.h"
#include "serial.h"
#include "timers.h"
#include "ForwardEuler.h"
#include "DCM2Angles.h"
#include "Oled.h"
#include "serial.h"

// Assumes gyros is 1x3 [p,q,r]
#define TIMESTEP 0.02

//Inputs: Previous attitute DCM (R)
//         Body Fixed Rotation rates gyros ([p;q;r]) in rad/s
//         Time between samples (dT) in seconds

// Outputs: New DCM (Rnew)
void IntegrateOpenLoop(float Rnew[3][3],float R[3][3],float gyros[3],float dT, uint8_t UseMatrixExponential){
    float p = gyros[1];
    float q = gyros[2];
    float r = gyros[3];
    if (UseMatrixExponential){
        MatrixExponential(Rnew,R, dT, p, q, r);
    }
    else{
        ForwardEuler(Rnew, R, dT, p, q, r);
    }
}

//#define TESTING_OPENLOOP 1
#ifdef TESTING_OPENLOOP
int main(void){
    BOARD_Init();
    BNO055_Init();
    TIMERS_Init();
    OledInit();
    
    float Rnew[3][3];
    // Initialize DCM to identity matrix
    float R[3][3] = {{1, 0, 0},
                     {0, 1, 0},
                     {0, 0, 1}};
    
    float gyros[3];
    float yaw,pitch,roll;
    int prevTime = 0;
    
    // Read gyro data from IMU and store into gyros[0][2] vector
    char message[100];
    while(1){
        // Integrate and print new euler angles every 20 ms
        if (TIMERS_GetMilliSeconds() - prevTime >= 20) { // Timer loop to trigger every time step (20 ms)
            prevTime = TIMERS_GetMilliSeconds();

            gyros[0] = BNO055_ReadGyroX();
            gyros[1] = BNO055_ReadGyroY();
            gyros[2] = BNO055_ReadGyroZ();

            IntegrateOpenLoop(Rnew, R, gyros, TIMESTEP, 1);
            // use DCM2Angle library to extract euler angles from new DCM and print to Oled
            yaw = DCM2Yaw(Rnew);
            pitch = DCM2Pitch(Rnew);
            roll = DCM2Roll(Rnew);

            printf("%f,%f,%f\n", yaw, pitch, roll);

            OledClear(0);
            sprintf(message, "yaw:%f\npitch:%f\n,roll:%f", yaw, pitch, roll);
            OledDrawString(message);
            OledUpdate();
        }
    }
}
#endif