/*
 * File:   timers.c
 * Author: mdunne
 *
 * Created on November 15, 2011, 9:53 AM
 */

#include <xc.h>
#include <BOARD.h>
#include "timers.h"
#include <sys/attribs.h>


/*******************************************************************************
 * PRIVATE #DEFINES                                                            *
 ******************************************************************************/
//#define TIMERS_TEST

#define F_PB (BOARD_GetPBClock())
#define TIMER_FREQUENCY 1000

/*******************************************************************************
 * PRIVATE VARIABLES                                                           *
 ******************************************************************************/

static unsigned int milliSecondCount;
static unsigned int microSecondCount;

/*******************************************************************************
 * PUBLIC FUNCTIONS                                                           *
 ******************************************************************************/

/**
 * @Function TIMERS_Init(void)
 * @param none
 * @return None.
 * @brief  Initializes the timer module
 * @author Max Dunne */
void TIMERS_Init(void)
{
    T5CON = 0;
    T5CONbits.TCKPS = 0b01;
    PR5 = (F_PB / TIMER_FREQUENCY) >> 1;
    T5CONbits.ON = 1;
    IFS0bits.T5IF = 0;
    IPC5bits.T5IP = 3;
    IEC0bits.T5IE = 1;
}

/**
 * Function: TIMERS_GetMilliSeconds
 * @param None
 * @return the current MilliSecond Count
 * @author Max Dunne
 */
unsigned int TIMERS_GetMilliSeconds(void)
{
    return milliSecondCount;
}

/**
 * Function: TIMERS_GetMicroSeconds
 * @param None
 * @return the current MicroSecond Count, it will roll over in 1.9 hours
 * @author Max Dunne
 */

unsigned int TIMERS_GetMicroSeconds(void)
{
    return (microSecondCount + TMR5 / 20);
}

/**
 * @Function Timer5IntHandler(void)
 * @param None.
 * @return None.
 * @brief  This is the interrupt handler to support the timer module. It will increment 
 * time
 * @author Max Dunne */

void __ISR(_TIMER_5_VECTOR) Timer5IntHandler(void)
{
    IFS0bits.T5IF = 0;
    milliSecondCount++;
    microSecondCount += 1000;
}




#ifdef TIMERS_TEST
#include "serial.h"
#include "timers.h"
#include <stdio.h>

int main(void)
{
    int i = 0;
    BOARD_Init();
    int curMilliSeconds;
    int curMicroSeconds;
    printf("Welcome to The Timers Test, Module will Init and then print times, get a stopwatch and compare\r\n");
    while (!IsTransmitEmpty());

    TIMERS_Init();
    unsigned int tick = 0;
    //    while (1) {
    //        if (IsTransmitEmpty()) {
    //            printf("%d\r\n",TIMERS_GetMilliSeconds());
    //        }
    //    }
    while (1) {
        if (TIMERS_GetMilliSeconds() - tick >= 10) {
            tick = TIMERS_GetMilliSeconds();
            if (IsTransmitEmpty()) {
                curMicroSeconds = TIMERS_GetMicroSeconds();
                curMilliSeconds = TIMERS_GetMilliSeconds();
                printf("ms: %d\tus: %d\tus/1000: %d\r\n",
                        curMilliSeconds, curMicroSeconds, curMicroSeconds / 1000);
            }
        }
    }



    while (1);
}

#endif