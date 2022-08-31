/*
 * Author: jsickafo
 *
 * Created on January 9, 2021, 1:24 PM
 */

#include "BOARD.h"
#include "Protocol.h"
#include "MessageIDs.h"
#include "FreeRunningTimer.h"
#include "RotaryEncoder.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

int main(void) {
    BOARD_Init();
    Protocol_Init();
    RotaryEncoder_Init(ENCODER_IC_MODE);
    FreeRunningTimer_Init();
    
    // Send an ID_DEBUG message
    char testMessage[MAXPAYLOADLENGTH]; // Prints out time and date
    sprintf(testMessage, "MotorRateTest Compiled at %s %s", __DATE__, __TIME__);
    Protocol_SendDebugMessage(testMessage);

    int previousTime1 = 0, previousTime2 = 0, rate;
    
    while(1){
        if (FreeRunningTimer_GetMilliSeconds() - previousTime1 >= 2){
            previousTime1 = FreeRunningTimer_GetMilliSeconds();
            
            rate = rateCheck(FreeRunningTimer_GetMilliSeconds());
        }
        
        if (FreeRunningTimer_GetMilliSeconds() - previousTime2 >= 10){
            previousTime2 = FreeRunningTimer_GetMilliSeconds();
            
            rate = Protocol_IntEndednessConversion((unsigned int)rate);
            Protocol_SendMessage(4, ID_REPORT_RATE, &rate);
        }
    }
}