/*
 * Author: jsickafo
 *
 * Created on March 9, 2021
 */

#define MAXOUTPUT_TO_SPEED <<27

#include "BOARD.h"
#include "Protocol.h"
#include "MessageIDs.h"
#include "FreeRunningTimer.h"
#include "DCMotorDrive.h"
#include "FeedbackControl.h"
#include "RotaryEncoder.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

static union {
    struct {
        int Proportional;
        int Integral;
        int Derivative;
    };
} values;

static union {
    struct {
        int error;
        int currentRate;
        int PWM;
    };
} feedback;

int main(void) {
    BOARD_Init();
    Protocol_Init();
    RotaryEncoder_Init(ENCODER_IC_MODE);
    DCMotorDrive_Init();
    FeedbackControl_Init();
    FreeRunningTimer_Init();
    
    // 1. Send an ID_DEBUG message
    char testMessage[MAXPAYLOADLENGTH]; // Prints out time and date
    sprintf(testMessage, "Closed Loop Control Test Compiled at %s %s", __DATE__, __TIME__);
    Protocol_SendDebugMessage(testMessage);
    
    sprintf(testMessage, "");
    int prevTime1, prevTime2, rate, reference;
    long long int newSpeed = 0;
    while(1){
        if (Protocol_IsMessageAvailable()){ // Every loop, checks for protocol messages
            
            // 2. Respond correctly to protocol ID_FEEDBACK_SET_GAINS
            if (Protocol_ReadNextID() == ID_FEEDBACK_SET_GAINS){    // If we set new gains
                // Grabs values
                Protocol_GetPayload(&values);
                
                // 3. Correctly decode and set the P, I, and D gains
                // Endian convert
                values.Proportional = Protocol_IntEndednessConversion(values.Proportional);
                values.Integral = Protocol_IntEndednessConversion(values.Integral);
                values.Derivative = Protocol_IntEndednessConversion(values.Derivative);
                
                // Set the values
                FeedbackControl_SetProportionalGain(values.Proportional);
                FeedbackControl_SetIntegralGain(values.Integral);
                FeedbackControl_SetDerivativeGain(values.Derivative);
                
                FeedbackControl_ResetController();  // Reset whenever PID changed
                // Respond
                Protocol_SendMessage(0, ID_FEEDBACK_SET_GAINS_RESP, '\0');
                Protocol_SendDebugMessage(testMessage);
            }
            
            // 4. Accept an ID_COMMANDED_RATE and update the target speed internally
            if (Protocol_ReadNextID() == ID_COMMANDED_RATE){    // integer commanded rate in raw ticks/count
                // Grabs value
                Protocol_GetPayload(&reference);
                
                // Endian convert
                reference = Protocol_IntEndednessConversion(reference);
            }
        }
        
        // 5. Calculate the motor speed at 1KHz, 1ms
        if (FreeRunningTimer_GetMilliSeconds() - prevTime1 >= 1){   // Calculate motor velocity (rate) every 5 ms
            prevTime1 = FreeRunningTimer_GetMilliSeconds(); // reset timer
            
            rate = rateCheck(prevTime1);   // Calculates the rate
        }
        
        // 6. Every 200Hz, 5ms
        if (FreeRunningTimer_GetMilliSeconds() - prevTime2 >= 5){     // Reports rate every 1ms
            prevTime2 = FreeRunningTimer_GetMilliSeconds(); // reset timer
            
            // A. Run the PID loop
            newSpeed = FeedbackControl_Update(reference, rate);
            
            // B. Scale the output of the PID loop appropriately
            newSpeed = ((newSpeed * MAXMOTORSPEED) >> FEEDBACK_MAXOUTPUT_POWER);
            
            // C. SET the motor speed
            DCMotorDrive_SetMotorSpeed(newSpeed);
            
            // D. Send an ID_REPORT_FEEDBACK
            feedback.error = reference - newSpeed;
            feedback.currentRate = rate;
            feedback.PWM = newSpeed;
            
            feedback.error = Protocol_IntEndednessConversion(feedback.error);
            feedback.currentRate = Protocol_IntEndednessConversion(feedback.currentRate);
            feedback.PWM = Protocol_IntEndednessConversion(feedback.PWM);
            Protocol_SendMessage(12, ID_REPORT_FEEDBACK, &feedback);
        }
    }
}