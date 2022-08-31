/*
 * File:   HelloWorld_Main.c
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
//    if (buttons.event == TRUE) {
//        LEDS_SET(buttons.value);
//        buttons.event = FALSE;
//    }
    
    uint8_t leds = 0x00;
    while(1){
        buttons.value = ButtonsCheckEvents();
        if ((buttons.value & BUTTON_EVENT_1DOWN) == BUTTON_EVENT_1DOWN){  // If button is pressed
            leds |= 0x03; // Sets the LED output value to have the correct bits set high by OR bitmasking
            LEDS_SET(leds);// set led output value
        }
        if ((buttons.value & BUTTON_EVENT_1UP) == BUTTON_EVENT_1UP){
            leds |= 0x03; // Sets the LED output value to have the correct bits set low
            leds ^= 0x03; // The only way I could figure out how to do this without NOR is by setting it to guaranteed be on with OR mask, then toggle it off with XOR mask
            LEDS_SET(leds);
        }
        if ((buttons.value & BUTTON_EVENT_2DOWN) == BUTTON_EVENT_2DOWN){
            leds |= 0x0C;
            LEDS_SET(leds);
        }
        if ((buttons.value & BUTTON_EVENT_2UP) == BUTTON_EVENT_2UP){
            leds |= 0x0C;
            leds ^= 0x0C;
            LEDS_SET(leds);
        }
        if ((buttons.value & BUTTON_EVENT_3DOWN) == BUTTON_EVENT_3DOWN){
            leds |= 0x30;
            LEDS_SET(leds);
        }
        if ((buttons.value & BUTTON_EVENT_3UP) == BUTTON_EVENT_3UP){
            leds |= 0x30;
            leds ^= 0x30;
            LEDS_SET(leds);
        }
        if ((buttons.value & BUTTON_EVENT_4DOWN) == BUTTON_EVENT_4DOWN){
            leds |= 0xC0;
            LEDS_SET(leds);
        }
        if ((buttons.value & BUTTON_EVENT_4UP) == BUTTON_EVENT_4UP){
            leds |= 0xC0;
            leds ^= 0xC0;
            LEDS_SET(leds);
        }
          
//            LEDS_SET(leds); // Sets led and buttons.event back to false
        
        // NOPS loop for delay
        int i;
        for (i = 0; i < NOPS_FOR_5MS; i++){
            asm("nop");
        }
    }
}

//void __ISR(_TIMER_2_VECTOR, ipl4auto) TimerInterrupt100Hz(void)
//{
//    // Clear the interrupt flag.
//    IFS0CLR = 1 << 8;
//
//    buttons.event = TRUE; // Sets the event to true and sets value to the new value
//    buttons.value = ButtonsCheckEvents();
//}