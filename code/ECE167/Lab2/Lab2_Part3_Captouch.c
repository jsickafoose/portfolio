/*
 * File:   Lab2_Part3_Captouch.c
 * Author: jsick
 *
 * Created on April 28, 2021, 5:48 PM
 */

/*
 Pin Usage
 * Captouch:
 *  pin35 = input for input capture to detect captouch
 */

#define LEDS_Init() do { \
    TRISE = 0x00; \
    LATE = 0x00; \
} while (0)

//Sets LATE to input x
#define LEDS_SET(x) (LATE = x)

//Returns LATE value
#define LEDS_GET() LATE

#include "BOARD.h"
#include "Oled.h"
#include "timers.h"
#include "CAPTOUCH.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

int main(void) {
    BOARD_Init();
    OledInit();
    CAPTOUCH_Init();
    LEDS_Init();
    TIMERS_Init();
    
    int prevTime = 0;
    char message[100];
    
    while(1){
        if (TIMERS_GetMilliSeconds() - prevTime >= 50){
            prevTime = TIMERS_GetMilliSeconds();            // Reset Timer
            
            // Simply changes the message and turns on the LED if the CAPTOUCHED_IsTouched() == TRUE
            if (CAPTOUCH_IsTouched()){
                sprintf(message, "Hi\nCap Pressed!");
                LEDS_SET(0xFF);
            }
            else {
                sprintf(message, "Hi");
                LEDS_SET(0x00);
            }
            OledClear(0);
            OledDrawString(message);
            OledUpdate();
        }
    }
    OledOff();
}