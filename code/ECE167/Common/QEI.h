/* 
 * @file    QEI.h
 * @brief   Quadrature Encoder sensing module
 * @author  CMPE167 Staff
 * @date    1/15/2019
 * @detail  This module uses the change notify peripheral to interface to a quadrature encoder. 
 *          If you are unfamiliar with change notify please read the lab appendix before beginning.
 *          The peripheral is configured to generate an interrupt on any change in input of pins RD6
 *          or RD7 (pins 36 and 37 on the Uno32). The interrupt will not tell you which pin changed
 *          states so you will need to implement a simple state machine to handle the transitions and
 *          keep track of the encoder count.
 *          NOTE: Encoder A and B must be input to pins 36 and 37
 *
 *          To alleviate setup headaches the code for setting up the peripheral and the interrupt is below.
 *
 *          char QEI_Init(void) {
 *               // INIT Change notify
 *               CNCONbits.ON = 1; // Change Notify On
 *               CNENbits.CNEN15 = 1; //enable one phase
 *               CNENbits.CNEN16 = 1; //enable other phase
 *               int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
 *               IFS1bits.CNIF = 0; // clear interrupt flag
 *               IPC6bits.CNIP = 1; //set priority
 *               IPC6bits.CNIS = 3; // and sub priority
 *               IEC1bits.CNIE = 1; // enable change notify
 * 
 *                // the rest of the function goes here
 *          }
 *
 *          void __ISR(_CHANGE_NOTICE_VECTOR) ChangeNotice_Handler(void) {
 *               static char readPort = 0;
 *               readPort = PORTD; // this read is required to make the interrupt work
 *               IFS1bits.CNIF = 0;
 *               //anything else that needs to happen goes here
 *          }
 */

#ifndef QEI_H
#define	QEI_H

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
 * @function QEI_Init(void)
 * @param none
 * @brief  Enables the Change Notify peripheral and sets up the interrupt, anything
 *         else that needs to be done to initialize the module. 
 * @return SUCCESS or ERROR (as defined in BOARD.h)
*/
char QEI_Init(void);

/**
 * @function QEI_GetPosition(void) 
 * @param none
 * @brief This function returns the current count of the Quadrature Encoder in ticks.      
*/
int QEI_GetPosition(void);

/**
 * @Function QEI_ResetPosition(void) 
 * @param  none
 * @return none
 * @brief  Resets the encoder such that it starts counting from 0.
*/
void QEI_ResetPosition(); 

#endif	/* QEI_H */

