/*
 * File:   FrequencyGenerator.h
 * Author: mdunne
 *
 * Software module to run one PWM module for frequency generation. 
 * PIN3 on the Uno32 is used for the output while it is slaved to timer 3
 * 
 *

 */

#ifndef FREQUENCY_GENERATOR_H
#define FREQUENCY_GENERATOR_H

/*******************************************************************************
 * PUBLIC #DEFINES                                                             *
 ******************************************************************************/
#define MIN_FREQ 1


#define TONE_196 196
#define TONE_293 293
#define TONE_440 440
#define TONE_659 659


#define DEFAULT_TONE TONE_440


/*******************************************************************************
 * TEMPLATE CODE FOR USE                                                             *
 ******************************************************************************/

#if 0
// This code fragment can be copied where needed and altered to fit the application
unsigned short CurFrequency;
unsigned char freqState;



    if (Protocol_IsMessageAvailable()) {
        if (Protocol_ReadNextID() == ID_LAB3_SET_FREQUENCY) {
            Protocol_GetPayload(&CurFrequency);
            CurFrequency = Protocol_ShortEndednessConversion(CurFrequency);
            FrequencyGenerator_SetFrequency(CurFrequency);
        }
        if (Protocol_ReadNextID() == ID_LAB3_FREQUENCY_ONOFF) {
            Protocol_GetPayload(&freqState);
            if (freqState) {
                FrequencyGenerator_On();
            } else {
                FrequencyGenerator_Off();
            }
        }
    }

#endif


/*******************************************************************************
 * PUBLIC FUNCTION PROTOTYPES                                                  *
 ******************************************************************************/


/**
 * @Function FrequencyGenerator_Init(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief  Initializes the timer and PWM for the tone system
 * @note  None.
 * @author Max Dunne */
char FrequencyGenerator_Init(void);

/**
 * @Function FrequencyGenerator_SetFrequency(unsigned int NewFrequency)
 * @param NewFrequency - new frequency to set. 
 * @return SUCCESS OR ERROR
 * @brief  Changes the frequency of the  system.
 * @note  Behavior of the output signal during Frequency change is undocumented
 * @author Max Dunne */
char FrequencyGenerator_SetFrequency(unsigned int NewFrequency);


/**
 * @Function FrequencyGenerator_GetFrequency(void)
 * @return Frequency of system in Hertz
 * @brief  gets the frequency of the  system.
 * @author Max Dunne */
unsigned int FrequencyGenerator_GetFrequency(void);


/**
 * @Function FrequencyGenerator_Off(void)
 * @return Turns output Off
 * @author Max Dunne */
void FrequencyGenerator_Off(void);


/**
 * @Function FrequencyGenerator_On(void)
 * @return Turns output On
 * @author Max Dunne */

void FrequencyGenerator_On(void);



#endif
