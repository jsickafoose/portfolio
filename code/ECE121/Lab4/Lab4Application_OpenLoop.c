/*
 * Author: jsickafo
 *
 * Created on March 9, 2021
 */

#include "BOARD.h"
#include "Protocol.h"
#include "MessageIDs.h"
#include "FreeRunningTimer.h"
#include "DCMotorDrive.h"
#include "RotaryEncoder.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

int main(void) {
    BOARD_Init();
    Protocol_Init();
    RotaryEncoder_Init(ENCODER_IC_MODE);
    DCMotorDrive_Init();
    FreeRunningTimer_Init();
    
    // Send an ID_DEBUG message
    char testMessage[MAXPAYLOADLENGTH]; // Prints out time and date
    sprintf(testMessage, "Open Loop Test Compiled at %s %s", __DATE__, __TIME__);
    Protocol_SendDebugMessage(testMessage);

    int prevTime1, rate, prevTime2, newSpeed = 0;
    while(1){
        if (Protocol_IsMessageAvailable()){ // Every loop, checks for prot messages
            if (Protocol_ReadNextID() == ID_COMMAND_OPEN_MOTOR_SPEED){  // If we get new motor speed
                Protocol_GetPayload(&newSpeed);
                newSpeed = Protocol_IntEndednessConversion(newSpeed);   // Set it
                DCMotorDrive_SetMotorSpeed(newSpeed);
                
                Protocol_SendMessage(0, ID_COMMAND_OPEN_MOTOR_SPEED_RESP, &newSpeed);
            }
        }
        
        if (FreeRunningTimer_GetMilliSeconds() - prevTime1 >= 2){   // Calculate motor velocity (rate) every 2 ms
            prevTime1 = FreeRunningTimer_GetMilliSeconds(); // reset timer
            
            rate = rateCheck(prevTime1);   // Calculates the rate
        }
        
        if (FreeRunningTimer_GetMilliSeconds() - prevTime2 >= 100){     // Reports rate every 100ms
            prevTime2 = FreeRunningTimer_GetMilliSeconds(); // reset timer
            
            rate = Protocol_IntEndednessConversion((unsigned int)rate); // Reports rate
            Protocol_SendMessage(4, ID_REPORT_RATE, &rate);
        }
    }
}