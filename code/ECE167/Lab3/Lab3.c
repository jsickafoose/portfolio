/*
 * File:   Lab3_Part1.c
 * Author: jsick
 *
 * Created on May 12, 2022, 12:55PM
 */

/*
 chipKIT Pin Usage
 * IMU I2C Pins:
 *  pin45  = SDA1
 *  pin46  = SCL1
 */

//// # Includes
#include "BOARD.h"
#include "Oled.h"
#include "timers.h"
#include "BNO055.h"
#include "serial.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

/* Select which main to run*/
//#define Sample_Data_Collection
#define Display_Values_On_OLED


//# Defined variables
// Calculated Offsets and scaling factors
#define AccelX_Scale 10051
#define AccelY_Scale 10058
#define AccelZ_Scale 10016

#define AccelX_Offset 160869
#define AccelY_Offset 297377
#define AccelZ_Offset 135053

#define MagX_Offset 13955
#define MagY_Offset 18555
#define MagZ_Offset 36564

#define GyroX_Offset 71240
#define GyroY_Offset 71064
#define GyroZ_Offset 80019

#define samples 100 // Samples for rolling average

#ifdef Sample_Data_Collection
int main(void) {
    BOARD_Init();
    BNO055_Init();
    TIMERS_Init();
    
    // Initializing variables
    int prevTime = 0;
    char message[100];
    int i, counter = 0;
    
    int AccelX = 0, AccelY = 0, AccelZ = 0; // Inits Acceleromter Variables
    int GyroX = 0, GyroY = 0, GyroZ = 0;    // Inits Gyroscope Variables
    int MagX = 0, MagY = 0, MagZ = 0;       // Inits Magnetometer Variables
    int temperature = 0;                    // Inits temperature variable
    
    
    
    while(counter<1000){ // Designed to take exactly 1000 samples
        if (TIMERS_GetMilliSeconds() - prevTime >= 20){     // I only update every 20ms for the requested 50Hz data collection
            prevTime = TIMERS_GetMilliSeconds();            // Reset Timer
            
            // Refreshes all variables
            AccelX = BNO055_ReadAccelX();
            AccelY = BNO055_ReadAccelY();
            AccelZ = BNO055_ReadAccelZ();

            GyroX = BNO055_ReadGyroX();
            GyroY = BNO055_ReadGyroX();
            GyroZ = BNO055_ReadGyroX();

            MagX = BNO055_ReadMagX();
            MagY = BNO055_ReadMagY();
            MagZ = BNO055_ReadMagZ();

            temperature = BNO055_ReadTemp();
            
            // Print raw data to terminal to aide in Matlab exporting
            sprintf(message, "%d, %d, %d\n", MagX, MagY, MagZ);
            for (i = 0; i < strlen(message); i++){
                    PutChar(message[i]);
            }
            
            counter++; // Increments the counter
        }
    }
}
#endif


#ifdef Display_Values_On_OLED
int main(void) {
    BOARD_Init();
    OledInit();
    BNO055_Init();
    TIMERS_Init();
    
    // Initializing variables
    int prevTime = 0, prevTime2 = 0; // Two time values for both the different sampling rates
    char message[100];      // Stores OLED and Serial message
    int X_Avg[2][samples];  // I decided to store each of the 3 sensor datas in a 2D array for each axis
    int Y_Avg[2][samples];
    int Z_Avg[2][samples];
    int counter = 0, i, counter2 = 0;
    
    int AccelX = 0, AccelY = 0, AccelZ = 0; // Inits Acceleromter Variables
    int GyroX = 0, GyroY = 0, GyroZ = 0;    // Inits Gyroscope Variables
    int MagX = 0, MagY = 0, MagZ = 0;       // Inits Magnetometer Variables
    int temperature = 0;                    // Inits temperature variable
    
    // These variables are used in the gyro integration
    int currTime = 0, lastTime = 0;
    int GyroSumX = 0, GyroSumY = 0, GyroSumZ = 0;
    
    while(1){
        if (TIMERS_GetMilliSeconds() - prevTime2 >= 5){     // Updating the data every 5ms or 200Hz because it's better for gyro integration
            prevTime2 = TIMERS_GetMilliSeconds(); 
            
            // Resets my avg values array index
            if (counter >= samples){
                counter = 0;
            }

            // Refreshes all variables with calibration taken into account
            X_Avg[0][counter] = ((BNO055_ReadAccelX())*AccelX_Scale + AccelX_Offset)/10000;
            Y_Avg[0][counter] = ((BNO055_ReadAccelY())*AccelY_Scale + AccelY_Offset)/10000;
            Z_Avg[0][counter] = ((BNO055_ReadAccelZ())*AccelZ_Scale + AccelZ_Offset)/10000;
            
            // The Gyro tracks much better when the average isn't taken
            GyroX = ((BNO055_ReadGyroX()*10000)-GyroX_Offset)/1310000;
            GyroY = ((BNO055_ReadGyroY()*10000)-GyroY_Offset)/1310000;
            GyroZ = ((BNO055_ReadGyroZ()*10000)-GyroZ_Offset)/1310000;

            X_Avg[1][counter] = ((BNO055_ReadMagX()*10000)-MagX_Offset)/10000;
            Y_Avg[1][counter] = ((BNO055_ReadMagY()*10000)-MagY_Offset)/10000;
            Z_Avg[1][counter] = ((BNO055_ReadMagZ()*10000)-MagZ_Offset)/10000;
            
            // Temperature was plenty stable and did not need the costly rolling average
            temperature = BNO055_ReadTemp();
            
            // Takes the integration of the Gyro to give the current angles
            currTime = TIMERS_GetMilliSeconds();
            GyroSumX += GyroX*(currTime-lastTime);
            GyroSumY += GyroY*(currTime-lastTime);
            GyroSumZ += GyroZ*(currTime-lastTime);
            lastTime = TIMERS_GetMilliSeconds();

            GyroX = GyroSumX/1000;
            GyroY = GyroSumY/1000;
            GyroZ = GyroSumZ/1000;
            
            counter++;
        }
            
        if (TIMERS_GetMilliSeconds() - prevTime >= 100){     // I only update the screen every 100ms or 10Hz
            prevTime = TIMERS_GetMilliSeconds();            // Reset Timer
            
            // The rolling average is only calculated every time it will be printed
            // Sums every value in all three arrays
            for (i = 0; i < samples; i++){
                AccelX += X_Avg[0][i];
                AccelY += Y_Avg[0][i];
                AccelZ += Z_Avg[0][i];
                
                MagX += X_Avg[1][i];
                MagY += Y_Avg[1][i];
                MagZ += Z_Avg[1][i];
            }
            // Divides by the number of samples to extract the mean
            AccelX /= samples;
            AccelY /= samples;
            AccelZ /= samples;

            MagX /= samples;
            MagY /= samples;
            MagZ /= samples;
            
            // Prints to OLED
            OledClear(0);
            sprintf(message, "A: %d, %d, %d\nG: %d, %d, %d\nM: %d, %d, %d\nTemp: %d",
                            AccelX, AccelY, AccelZ,
                            GyroX, GyroY, GyroZ,
                            MagX, MagY, MagZ,
                            temperature);
            OledDrawString(message);
            OledUpdate();
            
            // Prints the more easily Matlab readable data to Serial
            sprintf(message, "%d, %d, %d, %d, %d, %d, %d, %d, %d\n", AccelX, AccelY, AccelZ, MagX, MagY, MagZ, GyroX, GyroY, GyroZ);
            for (i = 0; i < strlen(message); i++){
                    PutChar(message[i]);
            }
        }
    }
    
    OledOff();
}
#endif