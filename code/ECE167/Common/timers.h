/*
 * File:   timers.h
 * Author: mdunne
 *
 * Software module to enable a bank of software timers with a resolution time of
 * one msecond for each. The timers can be individually started, stopped, expired, etc.
 *
 * NOTE: Module uses TIMER5 for its interrupts.
 *
 * TIMERS_TEST (in the .c file) conditionally compiles the test harness for the code. 
 * Make sure it is commented out for module useage.
 *
 * Created on November 15, 2011, 9:54 AM
 */

/*******************************************************************************
 * PUBLIC #DEFINES                                                             *
 ******************************************************************************/
#ifndef timers_H
#define timers_H





/*******************************************************************************
 * PUBLIC FUNCTION PROTOTYPES                                                  *
 ******************************************************************************/

/**
 * @Function TIMERS_Init(void)
 * @param none
 * @return None.
 * @brief  Initializes the timer module
 * @author Max Dunne, 2011.11.15 */
void TIMERS_Init(void);

/**
 * Function: TIMERS_GetMilliSeconds
 * @param None
 * @return the current MilliSecond Count
 * @author Max Dunne
   */
unsigned int TIMERS_GetMilliSeconds(void);

/**
 * Function: TIMERS_GetMicroSeconds
 * @param None
 * @return the current MicroSecond Count, it will roll over in 1.9 hours
 * @author Max Dunne
   */
unsigned int TIMERS_GetMicroSeconds(void);



#endif
