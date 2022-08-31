/*
 * File:   Lab2_Part2_Ping.c
 * Author: jsick
 *
 * Created on April 27, 2022, 4:50 PM
 */

/*
 Pin Usage
 * PING:
 *  pin4  = output for trigger
 *  pin34 = input for the echo
 * TONE:
 *  pin3  = tone generation
 */

#include "BOARD.h"
#include "Oled.h"
#include "PING.h"
#include "timers.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

int main(void) {
    BOARD_Init();
    OledInit();
    PING_Init();
    ToneGeneration_Init();
    
    int prevTime = 0, prevTime_2 = 0;
    int elapsedTime = 0, last_time = 0;
    int distance = 0;
    int lastTone = 0, tone = 0;
    char message[100];
    
    ToneGeneration_ToneOn();
    while(1){
        if (TIMERS_GetMilliSeconds() - prevTime >= 50){
            prevTime = TIMERS_GetMilliSeconds();            // Reset Timer
            
            // This value only needs to be updated when we update the screen
            distance = PING_GetDistance();
            
            // Displays distance, elapsedTime value, and the tone PMW output on the screen.
            OledClear(0);
            sprintf(message, "Distance: %d\nElapsed Time: %d\nTone: %d", distance, elapsedTime, tone);
            OledDrawString(message);
            OledUpdate();
        }
        
        // Updates the tone value at a quicker rate
        if (TIMERS_GetMilliSeconds() - prevTime_2 >= 3){
            prevTime_2 = TIMERS_GetMilliSeconds();            // Reset Timer
            
            // I start by updating the elapsedTime value
            elapsedTime = PING_GetTimeofFlight();
            // Only allows the stored flexValue to increment by 1 each run for smoothing
            if (elapsedTime > last_time){
                last_time++;
            }
            else if (elapsedTime < last_time){
                last_time--;
            }
            
            //Converts the last time value goal of 100-1100 to be the PWM max range
            if (last_time > 1100){
                tone = 1000;
            }
            else if (last_time < 100){
                tone = 0;
            }
            else {
                tone = last_time-100;
            }
            
            // This makes it so the tone doesn't change unless it tries to change by more than 5 so it doesn't jitter so much
            if (((lastTone - tone) > 5 || (lastTone - tone) < -5)){
                lastTone = tone;
                ToneGeneration_SetFrequency(tone);
            }
        }
    }
    
    ToneGeneration_ToneOff();
    OledOff();
}