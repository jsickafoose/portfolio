/*
 * File:   ToneGeneration.c
 * Author: mdunne
 *
 */

#include "BOARD.h"
#include "serial.h"
#include "ToneGeneration.h"
#include <xc.h>
#ifdef TONEGENERATION_TEST
#include <stdio.h>
#endif

/*******************************************************************************
 * PRIVATE #DEFINES                                                            *
 ******************************************************************************/

#define F_PB (BOARD_GetPBClock())



/*******************************************************************************
 * PRIVATE VARIABLES                                                            *
 ******************************************************************************/

static unsigned char toneOn = FALSE;
static unsigned int toneFrequency = 0;
static unsigned char toneSystemActive = FALSE;

/*******************************************************************************
 * PRIVATE FUNCTION PROTOTYPES                                                            *
 ******************************************************************************/

#define TONEDUTY_REGISTER OC1RS
#define TONERESET_REGISTER OC1R
#define TONECONFIG_REGISTER OC1CON



/*******************************************************************************
 * PUBLIC FUNCTIONS                                                           *
 ******************************************************************************/

/**
 * @Function ToneGeneration_Init(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief  Initializes the timer and PWM for the tone system
 * @note  None.
 * @author Max Dunne */
char ToneGeneration_Init(void)
{
    if (toneSystemActive) {
        return ERROR;
    }

    toneSystemActive = TRUE;

    ToneGeneration_SetFrequency(DEFAULT_TONE);

    ToneGeneration_ToneOff();
    TONERESET_REGISTER = 0;
    TONECONFIG_REGISTER = (_OC1CON_ON_MASK | 0b110 << _OC1CON_OCM_POSITION | _OC1CON_OCTSEL_MASK);

    return SUCCESS;
}

/**
 * @Function ToneGeneration_SetFrequency(unsigned int NewFrequency)
 * @param NewFrequency - new frequency to set. 
 * @return SUCCESS OR ERROR
 * @brief  Changes the frequency of the ToneGeneration system.
 * @note  Behavior of ToneGeneration during Frequency change is undocumented
 * @author Max Dunne */
char ToneGeneration_SetFrequency(unsigned int NewFrequency)
{
    if (!toneSystemActive) {
        return ERROR;
    }

    if (NewFrequency == toneFrequency) {
        return SUCCESS;
    }
    if (NewFrequency < 1) {
        return ERROR;
    }

    T3CON = 0;

    if (NewFrequency <= 1000) {
        T3CONbits.TCKPS = 0b101; // set the prescaler to 1:32
        PR3 = F_PB / 32 / NewFrequency;
    } else {
        T3CONbits.TCKPS = 0;
    }

    TMR3 = 0;
    TONEDUTY_REGISTER = (PR3 + 1) >> 1;
    T3CONbits.ON = 1;
    toneFrequency = NewFrequency;

    return SUCCESS;
}

/**
 * @Function ToneGeneration_GetFrequency(void)
 * @return Frequency of system in Hertz
 * @brief  gets the frequency of the ToneGeneration system.
 * @author Max Dunne */
unsigned int ToneGeneration_GetFrequency(void)
{
    return toneFrequency;
}

void ToneGeneration_ToneOff(void)
{
    TONEDUTY_REGISTER = 0;
    toneOn = FALSE;
}

void ToneGeneration_ToneOn(void)
{
    if (toneOn) {
        return;
    }
    toneOn = TRUE;
    TONEDUTY_REGISTER = (PR3 + 1) >> 1;
    //    printf("Duty Cycles: %d\t%d\r\n", PR3, TONEDUTY_REGISTER);
}

/*******************************************************************************
 * PRIVATE FUNCTIONS                                                       *
 ******************************************************************************/


#ifdef TONEGENERATION_TEST

#define DELAY(x)    {int wait; for (wait = 0; wait <= x; wait++) {asm("nop");}}
#define A_BIT       18300
#define A_LOT       183000
static int ToneArray[] = {TONE_196, TONE_293, TONE_440, TONE_293, TONE_440, TONE_659};
#include <stdio.h>

int main(void)
{

    BOARD_Init();
    printf("Beginning Tone Generation Test\r\n");

    ToneGeneration_Init();

    int curIndex;
    while (1) {
        for (curIndex = 0; curIndex < 6; curIndex++) {
            ToneGeneration_SetFrequency(ToneArray[curIndex]);
            ToneGeneration_ToneOn();
            printf("\r\nOutputting Tone %d", ToneArray[curIndex]);
            DELAY(A_LOT);
        }
        printf("\r\nOutputting Tone %d", 0);
        ToneGeneration_ToneOff();
        DELAY(A_LOT);
    }
    return 0;
}

#endif