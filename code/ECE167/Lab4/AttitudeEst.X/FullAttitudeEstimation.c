// Full attitude estimation
// Lab 4
#include <stdio.h>
#include <stdlib.h>
#include <xc.h>
#include <sys/attribs.h>
#include "stdint.h"

#include "BNO055.h"
#include "MatrixMath.h"
#include "BOARD.h"
#include "I2C.h"
#include "serial.h"
#include "timers.h"
#include "ForwardEuler.h"
#include "DCM2Angles.h"
#include "Oled.h"
#include "FullAttitudeEstimation.h"

#define pi 3.142857
#define dpsScaleFactor 131
#define dT 0.02 // 20 ms

// Accel Calibrations from tumble test in Lab 3
#define AccelScaleX 994.45
#define AccelScaleY 1000
#define AccelScaleZ 995.8
#define AccelOffsetX -8.01
#define AccelOffsetY -104.07
#define AccelOffsetZ -10.36

// Mag Calibrations from tumble test in Lab 3
#define MagScaleX 0.14
#define MagScaleY 0.08
#define MagScaleZ 0.11
#define MagOffsetX -169.89
#define MagOffsetY 166.71
#define MagOffsetZ -260.21

int timerFlag = 1;
int prevTime = 0;

int main(void){
    // Initialize libraries
    BOARD_Init();
    BNO055_Init();
    TIMERS_Init();
    OledInit();
    
    // Gains for accelerometer and magnetometer
    int Kp_accel = 1;
    int Ki_accel = 0.01;
    int Kp_mag = 1;
    int Ki_mag = 0.01;

    //Initialize DCM to identity matrix
    float R[3][3] = {{1, 0, 0},
                     {0, 1, 0},
                     {0, 0, 1}};
    // Initialize gyro bias 3x1 and prev bias 
    float gyroBias[3] = {0.15, 0.10, 0.25};
    float prevBias[3];
    
    // Declare 3x1 Feedback matrices from accelerometer and magnetometer
    float wMeasAccel[3];
    float wMeasMag[3];
    // Declare 3x1 matrices to hold sensor data
    float gyros[3]; //[1, 2, 3]
    float accel[3];
    float mag[3];
    float w[3];
    
    // Initialize Misalignment matrix from matlab
    float Rmisaligned[3][3] = 
    {{0.0073, 0.0431, 0.0263},
     {-0.0441, 0.0064, -0.0133},
     {-0.0234, 0.0188, 0.0013}};
    
    //Declare variables to hold euler angles
    float yaw = 0, pitch = 0, roll = 0;
    
    char message[100];
    
    while(1){
        if (TIMERS_GetMilliSeconds() - prevTime >= 20){ // Timer loop to trigger every time step (20 ms)
            prevTime = TIMERS_GetMilliSeconds();
            
            // Every 20 ms, read raw IMU data
            gyros[0] = BNO055_ReadGyroX();
            gyros[1] = BNO055_ReadGyroY();
            gyros[2] = BNO055_ReadGyroZ();

            //Read raw accelerometer data into 3x1 matrix
            accel[0] = BNO055_ReadAccelX();
            accel[1] = BNO055_ReadAccelY();
            accel[2] = BNO055_ReadAccelZ();

            //Read raw magnetometer data into 3x1 matrix
            mag[0] = BNO055_ReadMagX();
            mag[1] = BNO055_ReadMagY();
            mag[2] = BNO055_ReadMagZ();

            // Convert accels and mags to unit norm (1)
            accel[0] = (accel[0]/AccelScaleX) + AccelOffsetX;
            accel[1] = (accel[1]/AccelScaleY) + AccelOffsetY;
            accel[2] = (accel[2]/AccelScaleZ) + AccelOffsetZ;

            mag[0] = (mag[0]/MagScaleX) + MagOffsetX;
            mag[1] = (mag[1]/MagScaleY) + MagOffsetY;
            mag[2] = (mag[2]/MagScaleZ) + MagOffsetZ;
            // align magnetometer to accels using misalignment matrix
            mag[0] = (Rmisaligned[0][0]*mag[0]) + (Rmisaligned[0][1]*mag[1]) + (Rmisaligned[0][2]*mag[2]);
            mag[1] = (Rmisaligned[1][0]*mag[0]) + (Rmisaligned[1][1]*mag[1]) + (Rmisaligned[1][2]*mag[2]);
            mag[2] = (Rmisaligned[2][0]*mag[0]) + (Rmisaligned[2][1]*mag[1]) + (Rmisaligned[2][2]*mag[2]);

            // Convert raw gyro to rad/s by dividing by 131 and multiplying into rads
            gyros[0] = (gyros[0]/dpsScaleFactor) * (pi/180);
            gyros[1] = (gyros[1]/dpsScaleFactor) * (pi/180);
            gyros[2] = (gyros[2]/dpsScaleFactor) * (pi/180);
            //Remove gyro bias, store into new matrix w, rotation rate
            w[0] = gyros[0] - gyroBias[0];
            w[1] = gyros[1] - gyroBias[1];
            w[2] = gyros[2] - gyroBias[2];
            // Feedback: Accelerometer correction in body frame

            // accelBody is 3x1 matrix
            static float accelBody[3];
            accelBody[0] = (R[0][0]*accel[0]) + (R[0][1]*accel[1]) + (R[0][2]*accel[2]);
            accelBody[1] = (R[1][0]*accel[0]) + (R[1][1]*accel[1]) + (R[1][2]*accel[2]);
            accelBody[2] = (R[2][0]*accel[0]) + (R[2][1]*accel[1]) + (R[2][2]*accel[2]);
            
            // use skew symmetric to avoid cross product
            static float accelBodycross[3][3];
            accelBodycross[0][0] = 0;
            accelBodycross[0][1] = -accel[2];
            accelBodycross[0][2] = accel[1];
            accelBodycross[1][0] = accel[2];
            accelBodycross[1][1] = 0;
            accelBodycross[1][2] = -accel[0];
            accelBodycross[2][0] = -accel[1];
            accelBodycross[2][1] = accel[0];
            accelBodycross[2][2] = 0;
            
            // Feedback: Accelerometer correction in body frame
            //// Multiplies [3x3] * [3x1] column vector
            wMeasAccel[0] = (accelBodycross[0][0]*accelBody[0]) + (accelBodycross[0][1]*accelBody[1]) + (accelBodycross[0][2]*accelBody[2]);
            wMeasAccel[1] = (accelBodycross[1][0]*accelBody[0]) + (accelBodycross[1][1]*accelBody[1]) + (accelBodycross[1][2]*accelBody[2]);
            wMeasAccel[2] = (accelBodycross[2][0]*accelBody[0]) + (accelBodycross[2][1]*accelBody[1]) + (accelBodycross[2][2]*accelBody[2]);

            // magBody is 3x1 matrix
            static float magBody[3];
            magBody[0] = (R[0][0]*mag[0]) + (R[0][1]*mag[1]) + (R[0][2]*mag[2]);
            magBody[1] = (R[1][0]*mag[0]) + (R[1][1]*mag[1]) + (R[1][2]*mag[2]);
            magBody[2] = (R[2][0]*mag[0]) + (R[2][1]*mag[1]) + (R[2][2]*mag[2]);
            // use skew symmetric to avoid cross product
            static float magBodycross[3][3];
            magBodycross[0][0] = 0;
            magBodycross[0][1] = -mag[2];
            magBodycross[0][2] = mag[1];
            magBodycross[1][0] = mag[2];
            magBodycross[1][1] = 0;
            magBodycross[1][2] = -mag[0];
            magBodycross[2][0] = -mag[1];
            magBodycross[2][1] = mag[0];
            magBodycross[2][2] = 0;
            
            // Feedback: Magnetometer correction in body frame
            //// Multiplies [3x3] * [3x1] column vector
            wMeasMag[0] = (magBodycross[0][0]*magBody[0]) + (magBodycross[0][1]*magBody[1]) + (magBodycross[0][2]*magBody[2]);
            wMeasMag[1] = (magBodycross[1][0]*magBody[0]) + (magBodycross[1][1]*magBody[1]) + (magBodycross[1][2]*magBody[2]);
            wMeasMag[2] = (magBodycross[2][0]*magBody[0]) + (magBodycross[2][1]*magBody[1]) + (magBodycross[2][2]*magBody[2]);

            
            
            // Update gyro input with feedback
            wMeasAccel[0] = wMeasAccel[0] * Kp_accel;
            wMeasAccel[1] = wMeasAccel[1] * Kp_accel;
            wMeasAccel[2] = wMeasAccel[2] * Kp_accel;

            wMeasMag[0] = wMeasMag[0] * Kp_mag;
            wMeasMag[1] = wMeasMag[1] * Kp_mag;
            wMeasMag[2] = wMeasMag[2] * Kp_mag;
            
            static float w_total[3];
            w_total[0] = (w[0] + wMeasAccel[0] + wMeasMag[0]);
            w_total[1] = (w[1] + wMeasAccel[1] + wMeasMag[1]);
            w_total[2] = (w[2] + wMeasAccel[2] + wMeasMag[2]);

            // Integrate using matrix exponential
            MatrixExponential(R, R, dT, w_total[0], w_total[1], w_total[2]);

            // Update bias rate then update bias
            prevBias[0] = -Ki_accel*wMeasAccel[0] - Ki_mag*wMeasMag[0];
            prevBias[1] = -Ki_accel*wMeasAccel[1] - Ki_mag*wMeasMag[1];
            prevBias[2] = -Ki_accel*wMeasAccel[2] - Ki_mag*wMeasMag[2];

            gyroBias[0] = gyroBias[0] + prevBias[0] * dT;
            gyroBias[1] = gyroBias[1] + prevBias[1] * dT;
            gyroBias[2] = gyroBias[2] + prevBias[2] * dT;

            // use DCM2Angle library to extract euler angles from new DCM and print to Oled
            yaw = DCM2Yaw(R);
            pitch = DCM2Pitch(R);
            roll = DCM2Roll(R);

            // Print attitude estimation via serial and on Oled
            printf("%f,%f,%f\n",yaw,pitch,roll);

            OledClear(0);
            sprintf(message, "yaw:%f\npitch:%f\n,roll:%f",yaw,pitch,roll);
            OledDrawString(message);
            OledUpdate(); 
        }
    }
}