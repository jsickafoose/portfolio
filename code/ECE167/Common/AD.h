/*
 * File:   AD.h
 * Author: mdunne
 *
 * Software module to enable the Analog to Digital converter of the Uno32 boards.
 * NOTE: Analog pins automatically take over digital I/O regardless of which TRIS
 *       state it is in. There remains an error in the ADC code such that if all 12
 *       pins are enabled, one of them does not respond.
 *
 * AD_TEST (in the .c file) conditionally compiles the test harness for the code. 
 * Make sure it is commented out for module useage.
 *
 * Created on November 22, 2011, 8:57 AM
 */

#ifndef AD_H
#define AD_H

/*******************************************************************************
 * PUBLIC #DEFINES                                                             *
 ******************************************************************************/


#define AD_A0 (1<<0) // NOte that this is also the pot on board
#define AD_A1 (1<<1)
#define AD_A2 (1<<2)
#define AD_A3 (1<<3)
#define AD_A4 (1<<4)
#define AD_A5 (1<<5)


/*******************************************************************************
 * PUBLIC FUNCTION PROTOTYPES                                                  *
 ******************************************************************************/

/**
 * @function AD_Init(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief Initializes the A/D subsystem and enable battery voltage monitoring
 * @author Max Dunne, 2013.08.10 */
char AD_Init(void);

/**
 * @function AD_AddPins(unsigned int AddPins)
 * @param AddPins - Use #defined AD_XX OR'd together for each A/D Pin you wish to add
 * @return SUCCESS OR ERROR
 * @brief Remove pins from the A/D system.  If any pin is not active it returns an error
 * @author Max Dunne, 2013.08.15 */
char AD_AddPins(unsigned int AddPins);

/**
 * @function AD_RemovePins(unsigned int RemovePins)
 * @param RemovePins - Use #defined AD_XX OR'd together for each A/D Pin you wish to remove
 * @return SUCCESS OR ERROR
 * @brief Remove pins from the A/D system. If any pin is not active it returns an error
 * @author Max Dunne, 2013.08.15 */
char AD_RemovePins(unsigned int RemovePins);

/**
 * @function AD_ActivePins(void)
 * @param None
 * @return Listing of all A/D pins that are active
 * @brief Returns a variable of all active A/D pins. An individual pin can be determined if
 *        active by "anding" with the AD_XX Macros.
 * @note This will not reflect changes made with AD_AddPins or AD_RemovePins until the next A/D
 *       interrupt cycle.
 * @author Max Dunne, 2013.08.15 */
unsigned int AD_ActivePins(void);

/**
 * @function AD_IsNewDataReady(void)
 * @param None
 * @return TRUE or FALSE
 * @brief This function returns a flag indicating that the A/D has new values since the last
 *        read of a value
 * @author Max Dunne, 2013.08.15 */
char AD_IsNewDataReady(void);

/**
 * @function AD_ReadADPin(unsigned int Pin)
 * @param Pin - Used #defined AD_XX to select pin
 * @return 10-bit AD Value or ERROR
 * @brief Reads current value from buffer for given pin
 * @author Max Dunne, 2011.12.10 */
unsigned int AD_ReadADPin(unsigned int Pin);

/**
 * @function AD_End(void)
 * @param None
 * @return None
 * @brief Disables the A/D subsystem and release the pins used
 * @author Max Dunne, 2013.09.20 */
void AD_End(void);

#endif
