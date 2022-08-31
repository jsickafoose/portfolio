/**
 * @file    PING.h
 * @brief   Ultrasonic Ping Sensor sensing module
 * @author  CMPE167 Staff
 * @date    1/15/2019
 * @detail  This module uses the timer and the change notify peripheral to interface to an
 *          ultrasonic ranging sensor. 
 *          If you are unfamiliar with change notify or timers, please read the lab appendix before beginning.
 *          The timer peripheral is used to create the required trigger pulses. To do so you will need to modify when
 *          the next interrupt occurs by modifying the PR4 register to create the periodic pulse.
 *          The timer has already been set up with a 64:1 prescaler. The trigger pin has not been set and is up to you.
 *
 *          The change notify is configured to operate on CN14 or pin 34 on the I/O shield.  
 *          Instead of using a hardware timer we will use the TIMERS library to calculate the duration of the pulse
 *          in microseconds.
 *          To alleviate setup headaches the code for setting up the peripherals and interrupts is below.
 *
 *          char PING_Init(void) {
 *            // following block inits the timer
 *            T4CON = 0;
 *            T4CONbits.TCKPS = 0b110;
 *            PR4 = 0xFFFF;  // this is not the timer value wanted
 *            T4CONbits.ON = 1;
 *            IFS0bits.T4IF = 0;
 *            IPC4bits.T4IP = 3;
 *            IEC0bits.T4IE = 1;
 * 
 *            // following block inits change notify
 *            CNCONbits.ON = 1; // Change Notify On
 *            CNENbits.CNEN14 = 1;
 *            int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
 *            IFS1bits.CNIF = 0; // clear interrupt flag
 *            IPC6bits.CNIP = 1; //set priority
 *            IPC6bits.CNIS = 3; // and sub priority
 *            IEC1bits.CNIE = 1; // enable change notify
 *              //Anything else that needs to occur goes here
 *          }
 * 
 *          void __ISR(_CHANGE_NOTICE_VECTOR) ChangeNotice_Handler(void) {
 *              static char readPort = 0;
 *              readPort = PORTD; // this read is required to make the interrupt work
 *              IFS1bits.CNIF = 0; 
 *              //Anything else that needs to occur goes here
 *          }
 * 
 *          void __ISR(_TIMER_4_VECTOR) Timer4IntHandler(void) {
 *              IFS0bits.T4IF = 0;
 *              //Anything else that needs to occur goes here
 *          }
 *          
 */

#ifndef PING_H
#define PING_H

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
 * @function    PING_Init(void)
 * @brief       Sets up both the timer and Change notify peripherals along with their
 *              respective interrupts.  Also handles any other tasks needed such as pin 
 *              I/O directions, and any other things you need to initialize the sensor.
 *              TIMERS library must be inited before this library.
 * @return      SUCCESS or ERROR (as defined in BOARD.h)
 */
char PING_Init(void);

/**
 * @function    PING_GetDistance(void)
 * @brief       Returns the calculated distance in mm using the sensor model determined
 *              experimentally. 
 *              No I/O should be done in this function
 * @return      distance in mm
 */
unsigned int PING_GetDistance(void);

/**
 * @function    PING_GetTimeofFlight(void)
 * @brief       Returns the raw microsecond duration of the echo from the sensor.
 *              NO I/O should be done in this function.
 * @return      time of flight in uSec
 */
unsigned int PING_GetTimeofFlight(void);

#endif