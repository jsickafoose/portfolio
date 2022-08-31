/*
 * Author: jsickafo
 *
 * Created on March 16, 2021, 1:17 PM
 */

#include "BOARD.h"
#include "Protocol.h"
#include "MessageIDs.h"
#include "FreeRunningTimer.h"
#include "DCMotorDrive.h"
#include "FeedbackControl.h"
#include "RotaryEncoder.h"
#include "NonVolatileMemory.h"
#include "ADCFilter.h"

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <xc.h>

#define page 64
#define COMMAND_MODE 0
#define SENSOR_MODE 1
#define RANGE_LIMIT 350000

int SoftwareSafetyLimit(int absAngle, int pwm);

// Struct for properly returning filtered and raw values in a single payload
static union {
    struct {
        short rawVal;
        short filteredVal;
    };
} values;

static union {
    struct {
        int P1;
        int I1;
        int D1;
        int P2;
        int I2;
        int D2;
    };
} gains;

static union {
    struct {
        int P;
        int I;
        int D;
    };
} tempGains;

static union {
    struct {
        int error;
        int reference;
        int sensor;
        int commandedPos;
    };
} feedback;

int main(void) {
    BOARD_Init();
    Protocol_Init();
    RotaryEncoder_Init(ENCODER_IC_MODE);
    DCMotorDrive_Init();
    FeedbackControl_Init();
    LEDS_INIT();
    NonVolatileMemory_Init();
//    FrequencyGenerator_Init();
    ADCFilter_Init();
    FreeRunningTimer_Init();
    
    // 1A. Send an ID_DEBUG message
    char testMessage[MAXPAYLOADLENGTH]; // Prints out time and date
    sprintf(testMessage, "Lab5Application Compiled at %s %s", __DATE__, __TIME__);
    Protocol_SendDebugMessage(testMessage);
    sprintf(testMessage, "");
    
    int prevTime1 = 0, prevTime2 = 0, commandedAngle, currAngle, rData, brakes, i, pot;
    long long int newSpeed = 0;
    uint8_t mode, prevMode, pin = 0;
    short filter[2][FILTERLENGTH];
    
    // For finding the average
//    uint8_t avgIndex = 0;
//    short average[69];
//    int averageSum;
    
    // 1B. Load PID gains for both modes from NVM
    NonVolatileMemory_ReadPage(0, (char)24, (unsigned char *)&gains);
    
    // 1C. Set PID mode to COMMAND_MODE
    mode = COMMAND_MODE;
    
    // 1D. Send an ID_LAB5_CUR_MODE message with current mode
    Protocol_SendMessage(1, ID_LAB5_CUR_MODE, &mode);
    
    // 1E. Send an ID_FEEDBACK_CUR_GAINS message with current gains
    tempGains.P = Protocol_IntEndednessConversion((unsigned int)gains.P1);
    tempGains.I = Protocol_IntEndednessConversion((unsigned int)gains.I1);
    tempGains.D = Protocol_IntEndednessConversion((unsigned int)gains.D1);
    Protocol_SendMessage(12, ID_FEEDBACK_CUR_GAINS, &tempGains);
    Protocol_SendDebugMessage(testMessage);
    
    // 1F. Set commanded angle to current absolute angle
    commandedAngle = CurrentAngle();
    
    // Reading Filter Weights from the NVM
    NonVolatileMemory_ReadPage((page*1), (char)64, (unsigned char *)filter[0]);
    NonVolatileMemory_ReadPage((page*2), (char)64, (unsigned char *)filter[1]);
    // Setting the filter weights
    ADCFilter_SetWeights(0, filter[0]);
    ADCFilter_SetWeights(1, filter[1]);
    
    while(1){
        // This IF statement selects input method if there is a message available
        if (Protocol_IsMessageAvailable()) {
            // 2. Respond to ID_FEEDBACK_SET_GAINS
            if (Protocol_ReadNextID() == ID_FEEDBACK_SET_GAINS){
                // Grabs values
                Protocol_GetPayload(&tempGains);
                
                // 3. Correctly decode and set the P, I, and D gains
                // Endianness conversion
                if (!(mode)){   // If command mode
                    gains.P1 = Protocol_IntEndednessConversion((unsigned int)tempGains.P);
                    gains.I1 = Protocol_IntEndednessConversion((unsigned int)tempGains.I);
                    gains.D1 = Protocol_IntEndednessConversion((unsigned int)tempGains.D);
                    
                    // Set the values
                    FeedbackControl_SetProportionalGain(gains.P1);
                    FeedbackControl_SetIntegralGain(gains.I1);
                    FeedbackControl_SetDerivativeGain(gains.D1);
                }
                else {          // Else
                    gains.P2 = Protocol_IntEndednessConversion((unsigned int)tempGains.P);
                    gains.I2 = Protocol_IntEndednessConversion((unsigned int)tempGains.I);
                    gains.D2 = Protocol_IntEndednessConversion((unsigned int)tempGains.D);
                    
                    // Set the values
                    FeedbackControl_SetProportionalGain(gains.P2);
                    FeedbackControl_SetIntegralGain(gains.I2);
                    FeedbackControl_SetDerivativeGain(gains.D2);
                }
                FeedbackControl_ResetController();              // Must reset whenever values are changed
                
                // Respond
                Protocol_SendMessage(0, ID_FEEDBACK_SET_GAINS_RESP, &gains);
                Protocol_SendDebugMessage(testMessage);
                
                // 4. Store the new gains in NVM
                NonVolatileMemory_WritePage(0, (char)24, (unsigned char *)&gains);
            }
            
            // 5. Respond to a ID_FEEDBACK_REQ_GAINS message by sending CUR_GAINS
            if (Protocol_ReadNextID() == ID_FEEDBACK_REQ_GAINS){
                Protocol_GetPayload(&rData);
                if (!(mode)){   // If command mode
                    tempGains.P = Protocol_IntEndednessConversion((unsigned int)gains.P1);
                    tempGains.I = Protocol_IntEndednessConversion((unsigned int)gains.I1);
                    tempGains.D = Protocol_IntEndednessConversion((unsigned int)gains.D1);
                }
                else {          // Else
                    tempGains.P = Protocol_IntEndednessConversion((unsigned int)gains.P2);
                    tempGains.I = Protocol_IntEndednessConversion((unsigned int)gains.I2);
                    tempGains.D = Protocol_IntEndednessConversion((unsigned int)gains.D2);
                }
                Protocol_SendMessage(12, ID_FEEDBACK_CUR_GAINS, &tempGains);
                Protocol_SendDebugMessage(testMessage);
            }
            
            // 6. Respond correctly to protocol ID_LAB5_SET_MODE by changing the mode
            if (Protocol_ReadNextID() == ID_LAB5_SET_MODE){
                prevMode = mode;
                Protocol_GetPayload(&mode); // Sets the mode
                // 7. If the mode changed, load the gains and send ID_FEEDBACK_CUR_GAINS message
                if (mode != prevMode){      // If the mode was changed
                    if (!(mode)){   // If command mode
                        tempGains.P = Protocol_IntEndednessConversion((unsigned int)gains.P1);
                        tempGains.I = Protocol_IntEndednessConversion((unsigned int)gains.I1);
                        tempGains.D = Protocol_IntEndednessConversion((unsigned int)gains.D1);
                    }
                    else {          // Else
                        tempGains.P = Protocol_IntEndednessConversion((unsigned int)gains.P2);
                        tempGains.I = Protocol_IntEndednessConversion((unsigned int)gains.I2);
                        tempGains.D = Protocol_IntEndednessConversion((unsigned int)gains.D2);
                    }
                    FeedbackControl_ResetController();
                    Protocol_SendMessage(12, ID_FEEDBACK_CUR_GAINS, &tempGains);
                    Protocol_SendDebugMessage(testMessage);
                }
            }
            
            // 8. Respond to ID_LAB5_REQ_MODE by sending back the current mode
            if (Protocol_ReadNextID() == ID_LAB5_REQ_MODE){
                Protocol_GetPayload(&rData);
                Protocol_SendMessage(1, ID_LAB5_CUR_MODE, &mode);
            }
            
            // 9. Respond correctly to the ID_COMMANDED_POSITION message
            if (Protocol_ReadNextID() == ID_COMMANDED_POSITION){    // integer commanded rate in raw ticks/count
                // Grabs value
                Protocol_GetPayload(&commandedAngle);
                
                // Endian convert
                commandedAngle = Protocol_IntEndednessConversion(commandedAngle);
                FeedbackControl_ResetController();
            }
            
            if (Protocol_ReadNextID() == ID_ADC_SELECT_CHANNEL){            // If we are changing channel
                Protocol_GetPayload(&pin);                                  // Set pin to be channel
                Protocol_SendMessage(1, ID_ADC_SELECT_CHANNEL_RESP, &pin);  // responds with pin value
            }
            // Respond to ID_ADC_FILTER_VALUES
            if (Protocol_ReadNextID() == ID_ADC_FILTER_VALUES){     // If we are told to change filter values
                Protocol_GetPayload(&filter[pin]);
                for (i = 0; i < FILTERLENGTH; i++){// Swaps endianness of each individual short
                    filter[pin][i] = Protocol_ShortEndednessConversion(filter[pin][i]);
                }
                ADCFilter_SetWeights(pin, filter[pin]);    // Sets the weights, then writes the page
                   
                // 8.1 Store new filter coefficients in the NVM
                NonVolatileMemory_WritePage((page*(pin+1)), (char)64, (unsigned char *)filter[pin]);
                Protocol_SendMessage(1, ID_ADC_FILTER_VALUES_RESP, &pin);
            }
        }
        
        if (FreeRunningTimer_GetMilliSeconds() - prevTime1 >= 1){   // Calculate motor velocity (rate) every 5 ms
            prevTime1 = FreeRunningTimer_GetMilliSeconds(); // reset timer
            
            currAngle = AccumulatedAngle();   // Calculates the rate
        }
        
        // Every 10ms or at 100Hz
        if (FreeRunningTimer_GetMilliSeconds() - prevTime2 >= 10){
            prevTime2 = FreeRunningTimer_GetMilliSeconds();
            
            // Stores ADC readings for calculating average
//            average[avgIndex] = ADCFilter_FilteredReading(pin);  // Stores filtered values
//            avgIndex++;
//            if (avgIndex > 68){    // Resets the average Index when it goes off the top
//                avgIndex = 0;
//            }
            
            // Depending on mode, updates FeedbackControl
            if (!(mode)){   // If command mode
                // 10A. Run the PID loop
                newSpeed = FeedbackControl_Update(commandedAngle, currAngle);
                // 10B. Scale the output appropriately
                newSpeed = ((newSpeed * MAXMOTORSPEED) >> FEEDBACK_MAXOUTPUT_POWER);
            }
            else {
//                averageSum = 0;
//                for (i = 0; i < 69; i++){   // Increments through all 69 samples, every 10ms which might be too much
//                    averageSum += average[i];
//                }
//                pot = averageSum / 69;
                pot = ADCFilter_FilteredReading(pin);
                pot = (pot - 512) * 685;
                newSpeed = FeedbackControl_Update(pot, currAngle);
                // 10B. Scale the output appropriately
                newSpeed = ((newSpeed * 400000) >> 27);
            }
            
            // 10C. Set the motor speed
            brakes = SoftwareSafetyLimit(currAngle, newSpeed);
            if (brakes > 0){
                LEDS_SET(0x0F);
            }
            else if (brakes < 0){
                LEDS_SET(0xF0);
            }
            else{
                LEDS_SET(0x00);
            }
            
            // 10D. Send an ID_LAB5_REPORT message to the ECE121 Console
            if (!(mode)){ // If command mode
                feedback.error = commandedAngle - currAngle;
                feedback.reference = commandedAngle;
                feedback.sensor = newSpeed;
                feedback.commandedPos = currAngle;
            }
            else{
                feedback.error = pot - currAngle;
                feedback.reference = pot;
                feedback.sensor = newSpeed;
                feedback.commandedPos = currAngle;
            }
            
            
            // Endedness conversions
            feedback.error = Protocol_IntEndednessConversion(feedback.error);
            feedback.reference = Protocol_IntEndednessConversion(feedback.reference);
            feedback.commandedPos = Protocol_IntEndednessConversion(feedback.commandedPos);
            feedback.sensor = Protocol_IntEndednessConversion(feedback.sensor);
            Protocol_SendMessage(16, ID_LAB5_REPORT, &feedback);
        }
    }
}

int SoftwareSafetyLimit(int absAngle, int pwm){
    if ((absAngle > RANGE_LIMIT) && (pwm > 0)){
        DCMotorDrive_SetBrake();
        return 1;
    }
    else if ((absAngle < -(RANGE_LIMIT)) && (pwm < 0)){
        DCMotorDrive_SetBrake();
        return -1;
    }
    else {
        DCMotorDrive_SetMotorSpeed(pwm);
        return 0;
    }
}