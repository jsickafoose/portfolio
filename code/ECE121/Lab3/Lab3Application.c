/*
 * Author: jsickafo
 *
 * Created on January 9, 2021, 1:24 PM
 */

#include "BOARD.h"
#include "Protocol.h"
#include "MessageIDs.h"
#include "FreeRunningTimer.h"
#include "NonVolatileMemory.h"
#include "ADCFilter.h"

#include <stdio.h>
#include <string.h>
#include <xc.h>

#define page 64

// Struct for properly returning filtered and raw values in a single payload
static union {
    struct {
        short rawVal;
        short filteredVal;
    };
} values;

int main(void) {
    BOARD_Init();
    Protocol_Init();
    LEDS_INIT();
    NonVolatileMemory_Init();
    ADCFilter_Init();
    FreeRunningTimer_Init();
    
    TRISDbits.TRISD8 = 1;   // Sets the pins for the switches to be inputs
    TRISDbits.TRISD9 = 1;
    TRISDbits.TRISD10 = 1;
    TRISDbits.TRISD11 = 1;
    
    // 1. Send an ID_DEBUG message
    char testMessage[MAXPAYLOADLENGTH]; // Prints out time and date
    sprintf(testMessage, "Lab3Application Compiled at %s %s", __DATE__, __TIME__);
    Protocol_SendDebugMessage(testMessage);

    uint8_t timerFlag = 1, leds = 0xFF, pin = 0, peakIndex = 0, 
            SW1LastValue = 5, SW3LastValue= 5, change = 0;
    int targetMilli, i, ledMath;
    unsigned char freqState, channel_filter;
    short peakMax, peakMin;
    short filter1[4][FILTERLENGTH], filter2[4][FILTERLENGTH], peak2peak[69];
    unsigned short CurFrequency;
    
    // 2. Load in all 8 of the existing filter coefficients from NVM on startup
    NonVolatileMemory_ReadPage((page*0), (char)64, (unsigned char *)filter1[0]);
    NonVolatileMemory_ReadPage((page*0), (char)64, (unsigned char *)filter2[0]);
    NonVolatileMemory_ReadPage((page*1), (char)64, (unsigned char *)filter1[1]);
    NonVolatileMemory_ReadPage((page*1), (char)64, (unsigned char *)filter2[1]);
    NonVolatileMemory_ReadPage((page*2), (char)64, (unsigned char *)filter1[2]);
    NonVolatileMemory_ReadPage((page*2), (char)64, (unsigned char *)filter2[2]);
    NonVolatileMemory_ReadPage((page*3), (char)64, (unsigned char *)filter1[3]);
    NonVolatileMemory_ReadPage((page*3), (char)64, (unsigned char *)filter2[3]);
    
    if (!(PORTDbits.RD10)){    // If SW3 is down, initialize as filter 1
        ADCFilter_SetWeights(0, filter1[0]);
        ADCFilter_SetWeights(1, filter1[1]);
        ADCFilter_SetWeights(2, filter1[2]);
        ADCFilter_SetWeights(3, filter1[3]);
    }
    else{                   // Else, filter 2
        ADCFilter_SetWeights(0, filter2[0]);
        ADCFilter_SetWeights(1, filter2[1]);
        ADCFilter_SetWeights(2, filter2[2]);
        ADCFilter_SetWeights(3, filter2[3]);
    }
    
    
    while(1){
        // This IF statement selects input method if there is a message available
        if (Protocol_IsMessageAvailable()) {
            // I don't even think the application interface let's us change channel but just in case
            if (Protocol_ReadNextID() == ID_ADC_SELECT_CHANNEL){            // If we are changing channel
                Protocol_GetPayload(&pin);                                  // Set pin to be channel
                Protocol_SendMessage(1, ID_ADC_SELECT_CHANNEL_RESP, &pin);  // responds with pin value
            }
            // 7. Respond correctly to protocol ID_ADC_FILTER_VALUES
            if (Protocol_ReadNextID() == ID_ADC_FILTER_VALUES){     // If we are told to change filter values
                if (!(PORTDbits.RD10)){                             // If SW3 is down, filter 1 values are set
                    Protocol_GetPayload(&filter1[pin]);
                    for (i = 0; i < FILTERLENGTH; i++){// Swaps endianness of each individual short
                        filter1[pin][i] = Protocol_ShortEndednessConversion(filter1[pin][i]);
                    }
                    ADCFilter_SetWeights(pin, filter1[pin]);    // Sets the weights, then writes the page
                    
                    // 8.1 Store new filter coefficients in the NVM
                    NonVolatileMemory_WritePage((page*pin), (char)64, (unsigned char *)filter1[pin]);
                }
                else{                                           // If SW3 is up, change filter 2
                    Protocol_GetPayload(&filter2[pin]);
                    for (i = 0; i < FILTERLENGTH; i++){// Swaps endianness of each individual short
                        filter2[pin][i] = Protocol_ShortEndednessConversion(filter2[pin][i]);
                    }
                    ADCFilter_SetWeights(pin, filter2[pin]);    // Sets the weights, then writes the page
                    
                    // 8.2 Store new filter coefficients in the NVM
                    NonVolatileMemory_WritePage((page*pin), (char)64, (unsigned char *)filter2[pin]);
                }
                Protocol_SendMessage(1, ID_ADC_FILTER_VALUES_RESP, &pin);
            }
            
            // For the frequency generator
            if (Protocol_ReadNextID() == ID_LAB3_SET_FREQUENCY){
                Protocol_GetPayload(&CurFrequency);
                CurFrequency = Protocol_ShortEndednessConversion(CurFrequency);
                FrequencyGenerator_SetFrequency(CurFrequency);
            }
            if (Protocol_ReadNextID() == ID_LAB3_FREQUENCY_ONOFF){
                Protocol_GetPayload(&freqState);
                if (freqState) {
                    FrequencyGenerator_On();
                } else {
                    FrequencyGenerator_Off();
                }
            }
        }
        
        
        
        if (timerFlag == 1){
            targetMilli = (FreeRunningTimer_GetMilliSeconds() + 10); // Stops the timer every 10ms
            timerFlag = 0;
        }
        if (FreeRunningTimer_GetMilliSeconds() >= targetMilli){
            // I required initializing LEDs at FF each time, then bit shifting out enough 1's
            leds = 0xFF;
            
            // 3. Set channel based on SW1 and SW2
            // Creates the 2 bit number based on switch orientation
            pin = (PORTDbits.RD8 & 0b0001) | ((PORTDbits.RD9<<1) & 0b0010);
            if (pin != SW1LastValue){ // Sets flag saying switch change has occured
                SW1LastValue = pin;
                change = 1;
            }
            
            // 4. Set high or low pass based on SW3
            if (SW3LastValue != PORTDbits.RD10){ // Sets flag saying change occured
                SW3LastValue = PORTDbits.RD10;
                change = 1;
            }
            if (!(PORTDbits.RD10) && change){   // If SW3 is down, filter 1
                ADCFilter_SetWeights(pin, filter1[pin]);
            }
            else if (PORTDbits.RD10 && change){ // If no changes occured, doesn't do this for speed
                ADCFilter_SetWeights(pin, filter2[pin]);
            }
            
            // Stores 69 samples of filtered readings for peak2peak computation
            peak2peak[peakIndex] = ADCFilter_FilteredReading(pin);  // Stores filtered values
            peakIndex++;
            
            // 5. Display either peak to peak or absolute value on LEDS
            if (!(PORTDbits.RD11)){    // If SW4 is down
                ledMath = ADCFilter_FilteredReading(pin); // Just show raw reading
                if (ledMath < 0){
                    ledMath *= -1;
                }
                leds <<= (8 - (ledMath / 127)); // Shifts bits out of leds, depending on what number it shouuld display between 0 and 8
            }
            else{
                if (peakIndex > 68){    // Resets the peak Index when it goes off the top
                    peakIndex = 0;
                }
                peakMax = -32768;   // Initializes min and max at impossible values
                peakMin = 32767;
                for (i = 0; i < 69; i++){   // Increments through all 69 samples, every 10ms which might be too much
                    if (peakMax < peak2peak[i]){
                        peakMax = peak2peak[i];
                    }
                    if (peakMin > peak2peak[i]){
                        peakMin = peak2peak[i];
                    }
                }
                
                ledMath = (peakMax - peakMin); // Finds the difference, then does  the same math as above
                leds <<= (8 - (ledMath / 127));
            }
            
            // 6. Report back with ID_LAB3_CHANNEL_FILTER when switches are changed
            if (change > 0){
                change = 0;
                channel_filter = 0x00;  // Initializes payload byte to 0, for masking
                if (!(PORTDbits.RD10)){
                    channel_filter = (pin<<4)|(0b00000001); // Creates payload for filter 1
                }
                else{
                    channel_filter = (pin<<4)|(0b00000010); // Creates payload for filter 2
                }
                Protocol_SendMessage(1, ID_LAB3_CHANNEL_FILTER, &channel_filter);
            }
            
            // 9. Every 10ms, report back an ID_ADC_READING
            values.filteredVal = Protocol_ShortEndednessConversion(ADCFilter_FilteredReading(pin));
            values.rawVal = Protocol_ShortEndednessConversion(ADCFilter_RawReading(pin));
            Protocol_SendMessage(4, ID_ADC_READING, &values);
            LEDS_SET(leds); // And update LEDS
            timerFlag = 1;
        }
        
    }
}