/*
 * Author: jsick
 *
 * Created on January 9, 2021, 1:24 PM
 */

#include "BOARD.h"
#include "CircularBuffer.h"
#include <xc.h>

int main(void) {
    BOARD_Init();
    Buffer_Init();
    int i;
    
    while(1){
        
        char hello[] = "Hello, World!";
        char hello2[14];
        
        for (i = 0; i < 13; i++){
            AddData(hello[i]);
        }
       
        int size = itemNumber();
        
        for (i = 0; i < 13; i++){
            hello2[i] = GetData();
        }
        printf("%s", hello2);
        // NOPS loop for delay
        int i;
        for (i = 0; i < 10000; i++){
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