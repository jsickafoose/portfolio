/**
 * @file    CAPTOUCH.h
 * @brief   Capacitive touch sensing module
 * @author  CMPE167 Staff
 * @date    1/15/2019
 * @detail  This module uses the input capture peripheral to detect touch inputs.
 *          If you are unfamiliar with input capture please read the lab appendix before beginning.
 *          The peripheral is configured to generate an interrupt every rising edge which means
 *          that the difference of two interrupts gives you the period of the signal.
 *          NOTE: Given the limited number of timers on board this module is incompatible with PWM
 * 
 *          To alleviate setup headaches the code for setting up the peripheral and the interrupt is below.
 *          The library is using IC4 or pin 35 for the input capture. The timer is configured with a 1:8 
 *          prescaler to to have the timer period be reasonable and useful.
 * 
 *          char CAPTOUCH_Init(void)
 *          {
 // following block inits the timer
 *             T2CON = 0;
 *             T2CONbits.TCKPS = 0b011;
 *             PR2 = 0xFFFF;
 *             T2CONbits.ON = 1;
    
 *             //this block inits input capture
 *             IC4CON = 0;
 *             IC4CONbits.ICTMR = 1;
 *             IC4CONbits.ICM = 0b010;
    
 *             IFS0bits.IC4IF = 0;
 *             IPC4bits.IC4IP = 7;
 *             IEC0bits.IC4IE = 1;
 *             IC4CONbits.ON = 1;
 *             // whatever else you need to do to initialize your module
 *          }
 * 
 *          void __ISR(_INPUT_CAPTURE_4_VECTOR) InputCapture_Handler(void)
 *          {
 *              IFS0bits.IC4IF = 0;
 *              // IC4BUF contains the timer value when the rising edge occurred.
 *          }
 *          
 */

#ifndef CAPTOUCH_H
#define CAPTOUCH_H

/*******************************************************************************
 * INCLUDES                                                                    *
 ******************************************************************************/
#include "BOARD.h"
#include <xc.h>
#include <sys/attribs.h>

/*******************************************************************************
 * PUBLIC #DEFINES                                                             *
 ******************************************************************************/


/*******************************************************************************
 * PUBLIC FUNCTION PROTOTYPES                                                  *
 ******************************************************************************/

/**
 * @function    CAPTOUCH_Init(void)
 * @brief       This function initializes the module for use. Initialization is 
 *              done by opening and configuring timer 2, opening and configuring the input capture
 *              peripheral, and setting up the interrupt.
 * @return      SUCCESS or ERROR (as defined in BOARD.h)
 */
char CAPTOUCH_Init(void);

/**
 * @function    CAPTOUCH_IsTouched(void)
 * @brief       Returns TRUE if finger is detected. Averaging of previous measurements 
 *              may occur within this function, however you are NOT allowed to do any I/O
 *              inside this function.
 * @return      TRUE or FALSE
 */
char CAPTOUCH_IsTouched(void);

#endif  /* CAPTOUCH_H */