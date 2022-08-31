/*
 * File:   1_Lab0Main.c
 * Author: jsick
 *
 * Created on April 2, 2021, 4:32 PM
 */
#include "BOARD.h"
#include "serial.h"         // Used for outputting Hello World
#include "AD.h"             // Used for the Potentiometer value
#include "ToneGeneration.h" // Used to output PWM controlled tone
#include "Oled.h"           // Used to display helpful values on the OLED

#include <stdio.h>
#include <string.h>
#include <xc.h>

#define averageSamples 100  // Samples taken for the rolling average

int main(void) {
    // Initializing all libraries
    BOARD_Init();
    SERIAL_Init();
    ToneGeneration_Init();
    AD_Init();
    OledInit();
    
    AD_AddPins(AD_A0);                  // Sets ADC to read POT pin
    ToneGeneration_ToneOff();           // Initializes tone output to be off
    ToneGeneration_SetFrequency(1024);  // Initializes the frequency to be outside the range of what's played
    
    int i, k = 0;       // Used in calculating the average
    int potVal;
    unsigned int potAvg[averageSamples];
    char message[100];  // Stores the Hello World message
    
    
    // Part 1, printing Hello World to the serial port
    sprintf(message, "Hello World!");
    for (i = 0; i < strlen(message); i++){
        PutChar(message[i]);
    }
    
    while(1){
        // Part 2, was used to hardcode the tone
//        for (i = 0; i < 5000; i++){
//            asm("nop");
//        }
        OledClear(0);
        
        // Grabs potentiometer value, and displays it on OLED
        potVal = AD_ReadADPin(AD_A0);
        sprintf(message, "Hello World!\nPotentiometer Value: %u\n", potVal);
        OledDrawString(message);
        
        // Calculates a moving average of potentiometer values to smooth frequency
        potAvg[k] = potVal;
        for (i = 0; i < averageSamples; i++){
            potVal += potAvg[k];
        }
        potVal /= averageSamples;
        potVal /= 4;
//        potVal -= 511;
        // Resets k when it hits the upper limit
        k++;
        if (k >= averageSamples){
            k = 0;
        }
        OledUpdate();
        
        // Part 6
        // Sets tone based on averaged potValue + TONE of appropriate button
        // If two buttons pressed at once, no tone outputted
        if (BTN1 && !BTN2 && !BTN3 && !BTN4){
            ToneGeneration_ToneOn();
            ToneGeneration_SetFrequency(potVal+TONE_196);
        }
        else if (!BTN1 && BTN2 && !BTN3 && !BTN4){
            ToneGeneration_ToneOn();
            ToneGeneration_SetFrequency(potVal+TONE_293);
        }
        else if (!BTN1 && !BTN2 && BTN3 && !BTN4){
            ToneGeneration_ToneOn();
            ToneGeneration_SetFrequency(potVal+TONE_440);
        }
        else if (!BTN1 && !BTN2 && !BTN3 && BTN4){
            ToneGeneration_ToneOn();
            ToneGeneration_SetFrequency(potVal+TONE_659);
        }
        else {
            ToneGeneration_ToneOff();
            ToneGeneration_SetFrequency(1024);
        }
    }
    
    AD_End();
}