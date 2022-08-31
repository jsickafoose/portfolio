/*
 * File:   Lab1Main_1.c
 * Author: jsick
 *
 * Created on April 9, 2022, 14:15
 */


#include "BOARD.h"
#include "AD.h"
#include "ToneGeneration.h"
#include "Oled.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

#define flexADPin AD_A1             // Defines the AD pin for the Flex sensor as A1
                                    // Pin 3 is used for the tone generator as OC1
#define delayinMicroseconds 2000    // Defines the delay in the scanning and tone changes as about 50microseconds
#define minFlexValue 630            // The lowest flex value I got was 630

int main(void) {
    BOARD_Init();
    ToneGeneration_Init();
    AD_Init();
    OledInit();
    
    AD_AddPins(flexADPin);
    ToneGeneration_ToneOn();
    ToneGeneration_SetFrequency(1024);
    
    int i;
    int flexValue = 1023, flexAngle, toneValue = 1000, targetValue, lastTone = 0;
    int flexScalar = 100000/(1023-minFlexValue); // Changes the flex scalar based on the minimum value for the sensor
    char message[100];
    
    while(1){
        // Adds a delay, mainly so the speaker is not changing tone values too quickly
        for (i = 0; i < delayinMicroseconds; i++){
            asm("nop");
        }
        
        // Reads flex sensor raw value
        targetValue = AD_ReadADPin(flexADPin);
        if (targetValue > flexValue){
            flexValue++;    // Only allows the stored flexValue to increment by 1 each run for smoothing
        }
        else if (targetValue < flexValue){
            flexValue--;
        }
        
        // Converts flex value minimum flex value to the max 700-1023 to a tone value of 0-1000
        toneValue = flexValue - minFlexValue;
        toneValue *= flexScalar;
        toneValue /= 100;
        
        // Only sets new frequency if the delta is greater than 10
        if ((lastTone - toneValue) > 10 || (lastTone - toneValue) < -10){
            lastTone = toneValue;
            ToneGeneration_SetFrequency(toneValue);
        }
        
        // Calculates the flex angle using LSR calculated in the Sheets graph
        flexAngle = (flexValue/-3)+318;
        
        // Commands for printing flex value, angle, and output tone to OLED
        OledClear(0);
        sprintf(message, "Flex Value:%d\nAngle: %d\nTone Value: %d", flexValue, flexAngle, toneValue);
        OledDrawString(message);
        OledUpdate();
    }
    
    OledOff();
    ToneGeneration_ToneOff();
    AD_End();
}