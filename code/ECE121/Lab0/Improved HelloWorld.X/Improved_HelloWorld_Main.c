/*
 * File:   lab0_Main.c
 * Author: jsick
 *
 * Created on January 9, 2021, 1:24 PM
 */

#include "BOARD.h"
#include "BUTTONS.h"
#include "LEDS.h"

#include <xc.h>
//#include <plib.h>

#define NOPS_FOR_5MS 5000

typedef struct ButtonsTimer {
//    uint8_t event;
    uint16_t value;
} ButtonsTimer;

static ButtonsTimer buttons;

int main(void) {
    BOARD_Init();
    Buttons_Init();
    LEDS_Init();
    
//    LEDS_SET(0xFF);
    
    uint8_t leds = 0x00;
    int delay = 0;
    while(1){
        LEDS_SET(leds); // Sets leds
        
        if (delay > 50){ // This only increments the LED's every 50 run throughs of the loop, so every 250ms approximately
            delay = 0;
            leds++;
        }
        else {
            delay++;
        }
        
        buttons.value = ButtonsCheckEvents();
        if ((buttons.value & BUTTON_EVENT_1DOWN) | (buttons.value & BUTTON_EVENT_2DOWN) | (buttons.value & BUTTON_EVENT_3DOWN) | (buttons.value & BUTTON_EVENT_4DOWN)){ // If any Button is pressed, reset
            leds = 0;
        }
        if (leds > 0xFF){ // Reset if counter tops out
            leds = 0;
        }
        
        int i; // This is the delay of 5ms portion
        for (i = 0; i < (NOPS_FOR_5MS); i++){
            asm("nop");
        }
    }
}