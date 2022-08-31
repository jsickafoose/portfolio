/*
 * Author: jsick
 *
 * Created on January 9, 2021, 1:24 PM
 */

#include "BOARD.h"

#include <xc.h>

#define NOPS_FOR_10HZ 100000

int main(void) {
    BOARD_Init();
    
    TRISDbits.TRISD0 = 0; // Sets pin 3 and 5 on the board to "0" for output
    TRISDbits.TRISD1 = 0; // Pin 3 is for the Green LED, pin 5 for Red
    
    TRISDbits.TRISD2 = 1; // Sets pin 6 to be "1" for button input
    
    uint8_t secondRun = 0x00;
    while(1){
        
        if (PORTDbits.RD2 == 1){ // First of all, checks if button is pressed
            LATDbits.LATD0 ^= 0x01; // If button pressed, toggles Red LED
            if (secondRun > 0){ // Toggles Green LED every other run through
                secondRun = 0;
                LATDbits.LATD1 ^= 0x01;
            }
            else{
                secondRun++;
            }
        }
        else {
            LATDbits.LATD1 ^= 0x01; // If button pressed, same code but flipped for simplicity
            if (secondRun > 0){
                secondRun = 0;
                LATDbits.LATD0 ^= 0x01;
            }
            else{
                secondRun++;
            }
        }
        
        // NOPS loop for delay
        int i;
        for (i = 0; i < NOPS_FOR_10HZ; i++){
            asm("nop");
        }
    }
}


//TRIS //set a pin to be either input or output
//
//       //'1' being input '0' being output
//
//PORT //read a pin
//
//LAT //set a pin that is designated as an output
//
// ODC // Sets a pin to Open Drain