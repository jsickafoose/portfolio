/*
 * File:   FinalProject_Main.c
 * Authors: jsick, kcatlas
 *
 * Created on May 29, 2022, 11:15
 */


#include "BOARD.h"
#include "AD.h"
#include "Oled.h"
#include "timers.h"
#include "FingerSpelling.h"
#include "serial.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

//#define RAW_Value_Testing 1
#define Main_Letter_Translation 1

#define flexADPin0 AD_A0             // Defines the AD pin for the Flex sensor as A1
#define flexADPin1 AD_A1             // Defines the AD pin for the Flex sensor as A1
#define flexADPin2 AD_A2             // Defines the AD pin for the Flex sensor as A1
#define flexADPin3 AD_A3             // Defines the AD pin for the Flex sensor as A1
#define flexADPin4 AD_A4             // Defines the AD pin for the Flex sensor as A1

#define delayinMicroseconds 2000    // Defines the delay in the scanning and tone changes as about 50microseconds
#define samples 100                 // Samples for rolling average

/*
 chipKIT Pin Usage
 * Flex Sensor Pins Used Per Finger:
 *  pin A0 = Finger0(THUMB) Flex sensor
 *  pin A1 = Finger1(INDEX) Flex sensor
 *  pin A2 = Finger2(MIDDLE) Flex sensor
 *  pin A3 = Finger3(RING) Flex sensor
 *  pin A4 = Finger4(PINKY) Flex sensor
 */

#ifdef Main_Letter_Translation

int main(void) {
    BOARD_Init();
    AD_Init();
    OledInit();
    TIMERS_Init();
    
    // Adds each pin for each finger flex sensor
    AD_AddPins((flexADPin0 | flexADPin1 | flexADPin2 | flexADPin3 | flexADPin4));
    
    int i;  // reused in every for loop
    int counter = 0;    // Counter variable for storing samples to average
    int prevTime_Sampling = 0, prevTime_Display = 0;    // Keeps timer for the updating data and displaying data loops
    int flexAngle[5];                   // Storing flexAngle values in an array of 5, one for each finger
    int flexValues[5][samples];
    uint8_t fingerStates[5];
    char translation = 'Z';
    char message[100];
    
    while(1){
        if (TIMERS_GetMilliSeconds() - prevTime_Sampling >= 5){     // Updating the data every 5ms or 200Hz
            prevTime_Sampling = TIMERS_GetMilliSeconds();
            
            // Resets my avg values array index
            if (counter >= samples){
                counter = 0;
            }
            
            // Updating the current sample in the array of samples for each sensor
            flexValues[0][counter] = AD_ReadADPin(flexADPin0);
            flexValues[1][counter] = AD_ReadADPin(flexADPin1);
            flexValues[2][counter] = AD_ReadADPin(flexADPin2);
            flexValues[3][counter] = AD_ReadADPin(flexADPin3);
            flexValues[4][counter] = AD_ReadADPin(flexADPin4);
            
            counter++;
        }
        
        if (TIMERS_GetMilliSeconds() - prevTime_Display >= 100){     // Only updates the screen every 100ms or 10Hz
            prevTime_Display = TIMERS_GetMilliSeconds();
            
            // The rolling average is only calculated every time it will be printed
            // Sums every value in all arrays
            for (i = 0; i < samples; i++){
                flexAngle[0] += flexValues[0][i];
                flexAngle[1] += flexValues[1][i];
                flexAngle[2] += flexValues[2][i];
                flexAngle[3] += flexValues[3][i];
                flexAngle[4] += flexValues[4][i];
            }
            
            // Divides by the number of samples to extract the mean
            flexAngle[0] = flexAngle[0]/samples;
            flexAngle[1] = flexAngle[1]/samples;
            flexAngle[2] = flexAngle[2]/samples;
            flexAngle[3] = flexAngle[3]/samples;
            flexAngle[4] = flexAngle[4]/samples;
            
            // Sets the states for each finger
            fingerStates[0] = setFingerState(flexAngle[0], THUMB);
            fingerStates[1] = setFingerState(flexAngle[1], INDEX);
            fingerStates[2] = setFingerState(flexAngle[2], MIDDLE);
            fingerStates[3] = setFingerState(flexAngle[3], RING);
            fingerStates[4] = setFingerState(flexAngle[4], PINKY);
            
            // Gets the current char to display
            translation = getLetter(fingerStates[0], fingerStates[1], fingerStates[2], fingerStates[3], fingerStates[4]);
            
            // Prints to OLED
            OledClear(0);
            sprintf(message, "Current Hand Pose is Spelling: %c", translation);
            OledDrawString(message);
            OledUpdate();
        }
    }
    
    OledOff();
    AD_End();
}

#endif

#ifdef RAW_Value_Testing

int main(void) {
    BOARD_Init();
    SERIAL_Init();
    AD_Init();
    OledInit();
    TIMERS_Init();
    
    // Adds each pin for each finger flex sensor
    AD_AddPins((flexADPin0 | flexADPin1 | flexADPin2 | flexADPin3 | flexADPin4));
    
    int i;  // reused in every for loop
    int counter = 0;    // Counter variable for storing samples to average
    int prevTime_Sampling = 0, prevTime_Display = 0;    // Keeps timer for the updating data and displaying data loops
    int flexAngle[5];                   // Storing flexAngle values in an array of 5, one for each finger
    int flexValues[5][samples];
    char message[100];
    
    while(1){
        if (TIMERS_GetMilliSeconds() - prevTime_Sampling >= 5){     // Updating the data every 5ms or 200Hz
            prevTime_Sampling = TIMERS_GetMilliSeconds();
            
            // Resets my avg values array index
            if (counter >= samples){
                counter = 0;
            }
            
            // Updating the current sample in the array of samples for each sensor
            flexValues[0][counter] = AD_ReadADPin(flexADPin0);
            flexValues[1][counter] = AD_ReadADPin(flexADPin1);
            flexValues[2][counter] = AD_ReadADPin(flexADPin2);
            flexValues[3][counter] = AD_ReadADPin(flexADPin3);
            flexValues[4][counter] = AD_ReadADPin(flexADPin4);
            
            counter++;
        }
        
        if (TIMERS_GetMilliSeconds() - prevTime_Display >= 100){     // Only updates the screen every 100ms or 10Hz
            prevTime_Display = TIMERS_GetMilliSeconds();
            
            // The rolling average is only calculated every time it will be printed
            // Sums every value in all arrays
            for (i = 0; i < samples; i++){
                flexAngle[0] += flexValues[0][i];
                flexAngle[1] += flexValues[1][i];
                flexAngle[2] += flexValues[2][i];
                flexAngle[3] += flexValues[3][i];
                flexAngle[4] += flexValues[4][i];
            }
            
            // Divides by the number of samples to extract the mean
            flexAngle[0] = flexAngle[0]/samples;
            flexAngle[1] = flexAngle[1]/samples;
            flexAngle[2] = flexAngle[2]/samples;
            flexAngle[3] = flexAngle[3]/samples;
            flexAngle[4] = flexAngle[4]/samples;
            
            // Prints to OLED
            OledClear(0);
            sprintf(message, "Finger0: %d\nFinger1: %d\nFinger2: %d\nFinger3,4: %d,%d",flexAngle[0],flexAngle[1],flexAngle[2],flexAngle[3],flexAngle[4]);
            OledDrawString(message);
            OledUpdate();
            
            // Prints the more easily Matlab readable data to Serial
            sprintf(message, "%d,%d,%d,%d,%d\n", flexAngle[0],flexAngle[1],flexAngle[2],flexAngle[3],flexAngle[4]);
            for (i = 0; i < strlen(message); i++){
                    PutChar(message[i]);
            }
        }
    }
    
    OledOff();
    AD_End();
}

#endif