/*
 * File:   Lab2_Part1_Encoder.c
 * Author: jsick
 *
 * Created on April 27, 2022, 3:48 PM
 */

/*
 Pin Usage
 * RGB Pins:
 *  pin9  = R_PWM
 *  pin6  = G_PWM
 *  pin5  = B_PWM
 * QEI:
 *  pin36 = A
 *  pin37 = B
 */

// #Defines for RGB Pins
#define R_Pin PWM_PORTY04   // R = Pin 9
#define G_Pin PWM_PORTY10   // G = Pin 6
#define B_Pin PWM_PORTY12   // B = Pin 5

//// # Includes
#include "BOARD.h"
#include "Oled.h"
#include "QEI.h"
#include "pwm.h"
#include "timers.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

// I chose to make this as a function, implemented under main
void QEItoColor(int angle);
static int r, g, b;

int main(void) {
    BOARD_Init();
    OledInit();
    QEI_Init();
    PWM_Init();
    TIMERS_Init();
    
    int prevTime = 0;
    int angle = 0;
    char message[100];
    PWM_AddPins(R_Pin | G_Pin | B_Pin);
    
    while(1){
        if (TIMERS_GetMilliSeconds() - prevTime >= 50){     // I only update every 50ms
            prevTime = TIMERS_GetMilliSeconds();            // Reset Timer
            
            if (angle > 360){ // Keeps the angle below 360
                angle%=360;
            }
            angle = QEI_GetPosition();
            QEItoColor(angle); // Runs my function for calculating RGB values out of a 0-360 number
            
            PWM_SetDutyCycle(R_Pin, (1000-r)); //// I noticed a PWM duty cycle of 100% turned the pin off soo
            PWM_SetDutyCycle(G_Pin, (1000-g)); //   I just took the difference.
            PWM_SetDutyCycle(B_Pin, (1000-b));
            
            OledClear(0);
            sprintf(message, "Encoder Value: %d\nR: %d\nG: %d\nB: %d", angle, r, g, b);
            OledDrawString(message);
            OledUpdate();
        }
    }
    
    OledOff();
}



void QEItoColor(int angle){
    // Sets H to be within the correct shifted range for the equation I found
    static int H;
    if (angle<0){
        H = abs(angle) + 90;
    }
    else {
        H = abs(450 - angle);
    }
    if (H >= 360){
        H %= 360;
    }
    // Implements the formula I found on rapidtables.com for HSV to RGB conversion
    static int X = 0;
    X = 100 - abs(((H*10)/6)%200 - 100);
    if (H >= 0 && H < 60){
        r = 100; // The difference is, on the formula max RGB is 255 but for me it's 1000 PWM
        g = X;
        b = 0;
    }
    else if (H >= 60 && H < 120){
        r = X;
        g = 100;
        b = 0;
    }
    else if (H >= 120 && H < 180){
        r = 0;
        g = 100;
        b = X;
    }
    else if (H >= 180 && H < 240){
        r = 0;
        g = X;
        b = 100;
    }
    else if (H >= 240 && H < 300){
        r = X;
        g = 0;
        b = 100;
    }
    else if (H >= 300 && H < 360){
        r = 100;
        g = 0;
        b = X;
    }
    
    r *= 10;
    g *= 10;
    b *= 10;
}