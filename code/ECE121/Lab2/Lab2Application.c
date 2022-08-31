/*
 * Author: jsickafo
 *
 * Created on January 9, 2021, 1:24 PM
 */

#include "BOARD.h"
#include "Protocol.h"
#include "MessageIDs.h"
#include "FreeRunningTimer.h"
#include "PingSensor.h"
#include "RCServo.h"
#include "RotaryEncoder.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

static union {
    struct {
        unsigned int outputValue;
        char status;
    };
    char asChar[5];
} AngleData;

int main(void) {
    BOARD_Init();
    Protocol_Init();
    FreeRunningTimer_Init();
    PingSensor_Init();
    RCServo_Init();
    RotaryEncoder_Init(ENCODER_SPI_MODE);
    
    char testMessage[MAXPAYLOADLENGTH]; // Prints out time and date
    sprintf(testMessage, "Lab2Application Compiled at %s %s", __DATE__, __TIME__);
    Protocol_SendDebugMessage(&testMessage);

//    char status;
    unsigned int pingValue = 0xfff, pulseValue = 0, targetMilli = 0;
//    unsigned int pingValue = 0xfff;
//    unsigned int pulseValue = 0;
//    unsigned int targetMilli = 0;
//    unsigned int outputValue;
    unsigned short rotaryAngle = 0, pingDistance = 0, inputSel = 0;
//    unsigned short rotaryAngle = 0;
//    unsigned short pingDistance = 0;
//    unsigned short inputSel = 0;
    AngleData.status = 0x00;
//    status = 0x00;
    uint8_t timerFlag = 1;
    while(1){
        rotaryAngle = RotaryEncoder_ReadRawAngle();
        pingDistance = PingSensor_GetDistance();

        // This IF statement selects input method if there is a message available
        if (Protocol_IsMessageAvailable()) {
            if (Protocol_ReadNextID() == ID_LAB2_INPUT_SELECT) { // If we get servo pulse
                // send pong in response here
                Protocol_GetPayload(&pingValue); // receive it
                if (pingValue > 0){    // ENCODER
                    inputSel = 1;
                }
                else {  // PING SENSOR
                    inputSel = 0;
                }
            }
        }
        
        // This sets pulseValue depending on which driven mode it's on
        if (inputSel){  // If Encoder driven mode
            pulseValue = (((rotaryAngle * 11)/100)+600); // The conversion math I came up with
        }
        else {  // If Ping sensor driven mode
            pulseValue = ((((pingDistance - 250)*18)/10)+600); // The conversion from distance to RC ticks
        }
        
        // These IF statements set the ANGLE_REPORT char if it's in or out of bounds
        if (pulseValue > RC_SERVO_MAX_PULSE){
            AngleData.status = 0x01;
//            status = 0x01;
        }
        else if (pulseValue < RC_SERVO_MIN_PULSE){
            AngleData.status = 0x04;
//            status = 0x04;
        }
        else {
            AngleData.status = 0x02;
//            status = 0x02;
        }
        RCServo_SetPulse(pulseValue);
        
        
        if (timerFlag == 1){
            targetMilli = (FreeRunningTimer_GetMilliSeconds() + 50); // This is required to make the timer stop every 50ms
            timerFlag = 0;
        }
        if (FreeRunningTimer_GetMilliSeconds() >= targetMilli){
            AngleData.outputValue = ((pulseValue)-600)*200;
            AngleData.outputValue = Protocol_IntEndednessConversion(AngleData.outputValue);
//            outputValue = Protocol_IntEndednessConversion(pulseValue);
//            outputValue = (outputValue<<8 | status);
            Protocol_SendMessage(5, ID_LAB2_ANGLE_REPORT, &AngleData);
            timerFlag = 1;
        }
        
    }
}