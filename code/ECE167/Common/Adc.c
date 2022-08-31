#include "Adc.h"


#include <sys/attribs.h>


static uint16_t adcValue = 0;
static uint8_t adcHasNewData;


#define WINDOW_SIZE 1 

void AdcInit(void)
{

    // Set B2 to an input so AN0 can be used by the ADC.    
    TRISBbits.TRISB2 = 1;

    // Configure and start the ADC
    // Read AN0 as sample a. We don't use alternate sampling, so setting sampleb is pointless.


    AD1CHSbits.CH0SA = 2;
    AD1CON1 = 0;
    AD1CON1bits.ADON = 0; //turn off to be sure
    AD1CON1bits.FORM = 000; // set to 16 bit unsigned integers
    AD1CON1bits.SSRC = 0b111; // auto convert
    AD1CON1bits.ASAM = 1; //auto sample

    AD1CON2 = 0;
    AD1CON2bits.VCFG = 0; // use AVdd and AVss
    AD1CON2bits.OFFCAL = 0;
    AD1CON2bits.CSCNA = 0;
    AD1CON2bits.SMPI = 7; // 8 samples per interrupt
    AD1CON2bits.BUFM = 0;
    AD1CON2bits.ALTS = 0;

    AD1CON3 = 0;
    AD1CON3bits.ADRC = 0; // USE PB
    AD1CON3bits.SAMC = 29;
    AD1CON3bits.ADCS = 50;

    AD1PCFGbits.PCFG2 = 0;

    AD1CSSLbits.CSSL2 = 1;
    AD1CON1bits.ADON = 1;

    // Enable interrupts for the ADC
    IPC6bits.AD1IP = 2;
    IPC6bits.AD1IS = 0;
    IEC1bits.AD1IE = 1;

}

uint8_t AdcChanged(void)
{
    if (adcHasNewData) {
        adcHasNewData = FALSE;
        return TRUE;
    } else {
        return FALSE;
    }
}

uint16_t AdcRead(void)
{
    adcHasNewData = FALSE;
    return adcValue;
}

/**
 * This is the ISR for the ADC1 peripheral. It has been enabled to run
 * continuously. It maps the 10-bit ADC value into just a 3-bit value, and 
 * also filters out pot noise with a moving window strategy.
 */
void __ISR(_ADC_VECTOR, ipl2auto) AdcHandler(void)
{
    // Clear the interrupt flag.
//    IFS1CLR = 1 << 1;
    
    // Clear the interrupt flag.
    IFS1bits.AD1IF = 0;

    int16_t current_reading = (ADC1BUF0 + ADC1BUF1 + ADC1BUF2 + ADC1BUF3 +
            ADC1BUF4 + ADC1BUF5 + ADC1BUF6 + ADC1BUF7) >> 3;

    //check to see if ADC has left filtering window:
    if (((current_reading - adcValue) > WINDOW_SIZE) ||
            ((adcValue - current_reading) > WINDOW_SIZE)) {
        adcValue = current_reading;
        adcHasNewData = TRUE;
    }
    if (current_reading == 0 && adcValue != 0) {
        adcValue = current_reading;
        adcHasNewData = TRUE;
    }
    if (current_reading == 1023 && adcValue != 1023) {
        adcValue = current_reading;
        adcHasNewData = TRUE;
    }
}


#ifdef AD_TEST

#include <xc.h>
#include "BOARD.h"
#include <stdio.h>

int main(void)
{
    BOARD_Init();
    AdcInit();
    printf("AD Test Compiled at " __TIME__ "\n");
    while (1) {
        if (AdcChanged()) {
            printf("Reading: %d\n", AdcRead());
        }
    }
    while (1);
    return 0;
}


#endif