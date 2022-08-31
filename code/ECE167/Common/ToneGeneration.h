/*
 * File:   ToneGeneration.h
 * Author: mdunne
 *
 * Software module to run one PWM module for tone generation. 
 * PIN3 on the Uno32 is used for tone generation
 * 
 *

 */

#ifndef TONEGENERATION_H
#define TONEGENERATION_H

/*******************************************************************************
 * PUBLIC #DEFINES                                                             *
 ******************************************************************************/
#define MIN_TONE 1


#define TONE_196 196
#define TONE_293 293
#define TONE_440 440
#define TONE_659 659


#define DEFAULT_TONE TONE_440



/*******************************************************************************
 * PUBLIC FUNCTION PROTOTYPES                                                  *
 ******************************************************************************/


/**
 * @Function ToneGeneration_Init(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief  Initializes the timer and PWM for the tone system
 * @note  None.
 * @author Max Dunne */
char ToneGeneration_Init(void);

/**
 * @Function ToneGeneration_SetFrequency(unsigned int NewFrequency)
 * @param NewFrequency - new frequency to set. 
 * @return SUCCESS OR ERROR
 * @brief  Changes the frequency of the ToneGeneration system.
 * @note  Behavior of ToneGeneration during Frequency change is undocumented
 * @author Max Dunne */
char ToneGeneration_SetFrequency(unsigned int NewFrequency);


/**
 * @Function ToneGeneration_GetFrequency(void)
 * @return Frequency of system in Hertz
 * @brief  gets the frequency of the ToneGeneration system.
 * @author Max Dunne */
unsigned int ToneGeneration_GetFrequency(void);


/**
 * @Function ToneGeneration_ToneOff(void)
 * @return Turns Tone Off
 * @author Max Dunne */
void ToneGeneration_ToneOff(void);


/**
 * @Function ToneGeneration_ToneOn(void)
 * @return Turns Tone On
 * @author Max Dunne */

void ToneGeneration_ToneOn(void);



#endif
