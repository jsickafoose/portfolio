/*
 * File:   BOARD.c
 * Author: Max
 *
 * Created on December 19, 2012, 2:08 PM
 */
#ifdef _SUPPRESS_PLIB_WARNING
#undef _SUPPRESS_PLIB_WARNING
#endif

#include "BOARD.h"
#include <xc.h>




//#define _SUPPRESS_PLIB_WARNING
//#include <plib.h>
//#include <peripheral/osc.h>
//#include <peripheral/lock.h>

/*******************************************************************************
 * PRAGMAS                                                                     *
 ******************************************************************************/
// Configuration Bits
// SYSCLK = 80MHz
// PBCLK  = 40MHz
// using POSC w/ PLL, XT mode
#pragma config FPBDIV     = DIV_2
#pragma config FPLLIDIV   = DIV_2     // Set the PLL input divider to 2, seems to
#pragma config IESO       = OFF       // Internal/External Switch
#pragma config POSCMOD    = XT        // Primary Oscillator Configuration for XT osc mode
#pragma config OSCIOFNC   = OFF       // Disable clock signal output
#pragma config FCKSM      = CSECMD    // Clock Switching and Monitor Selection
#pragma config WDTPS      = PS1       // Specify the watchdog timer interval (unused)
#pragma config FWDTEN     = OFF       // Disable the watchdog timer
#pragma config ICESEL     = ICS_PGx2  // Allow for debugging with the Uno32
#pragma config PWP        = OFF       // Keep the program flash writeable
#pragma config BWP        = OFF       // Keep the boot flash writeable
#pragma config CP         = OFF       // Disable code protect
#pragma config FNOSC 		= PRIPLL	//Oscillator Selection Bits
#pragma config FSOSCEN 		= OFF		//Secondary Oscillator Enable
#pragma config FPLLMUL 		= MUL_20	//PLL Multiplier
#pragma config FPLLODIV 	= DIV_1 	//System PLL Output Clock Divide




/*******************************************************************************
 * PRIVATE #DEFINES                                                            *
 ******************************************************************************/

#define SYSTEM_CLOCK 80000000L
#define  PB_CLOCK SYSTEM_CLOCK/2
#define TurnOffAndClearInterrupt(Name) INTEnable(Name,INT_DISABLED); INTClearFlag(Name)

/**
 * @function BOARD_Init(void)
 * @param None
 * @return None
 * @brief Set the clocks up for the board, initializes the serial port, and turns on the A/D
 *        subsystem for battery monitoring
 * @author Max Dunne, 2013.09.15  */
void BOARD_Init()
{
    //sets the system clock to the optimal frequency given the system clock
    //SYSTEMConfig(SYSTEM_CLOCK, SYS_CFG_WAIT_STATES | SYS_CFG_PCACHE);
    //sets the divisor to 2 to ensure 40Mhz peripheral bus
    //OSCSetPBDIV(OSC_PB_DIV_2);


    //disables all A/D pins for a clean start
    AD1PCFG = 0xffff;
    
    // get rid of JTAG before it kills us
    DDPCONbits.JTAGEN = 0;
    
    //enables the interrupt system in the new style
    //    INTConfigureSystem(INT_SYSTEM_CONFIG_MULT_VECTOR);
    //    INTEnableInterrupts();

    // this section of code comes from microchips deprecated plib
    // dealing with the interrupt handler is tricky enough to the point of I have no desire to re-invent the wheel

    unsigned int val;
    // set the CP0 cause IV bit high
    asm volatile("mfc0   %0,$13" : "=r"(val));
    val |= 0x00800000;
    asm volatile("mtc0   %0,$13" : "+r"(val));
    INTCONSET = _INTCON_MVEC_MASK;
    unsigned int status = 0;
    asm volatile("ei    %0" : "=r"(status));


    //printf("CMPE118 IO stack is now initialized\r\n");

}

/**
 * @function BOARD_End(void)
 * @param None
 * @return None
 * @brief Shuts down all peripherals except for serial and A/D. Turns all pins into input
 * @author Max Dunne, 2013.09.20  */
void BOARD_End()
{

    // kill off all interrupts except serial and clear their flags
    IEC0CLR = ~(_IEC0_U1TXIE_MASK | _IEC0_U1RXIE_MASK);
    IFS0CLR = ~(_IFS0_U1TXIF_MASK | _IFS0_U1RXIF_MASK);

    // kill off all interrupts except A/D and clear their flags
    IEC1CLR = ~(_IEC1_AD1IE_MASK);
    IFS0CLR = ~(_IFS1_AD1IF_MASK);

    // set all ports to be digital inputs
    TRISB = 0xff;
    TRISC = 0xff;
    TRISD = 0xff;
    TRISE = 0xff;
    TRISF = 0xff;
    TRISG = 0xff;


}

/**
 * @function BOARD_GetPBClock(void)
 * @param None
 * @return PB_CLOCK - Speed the peripheral clock is running in hertz
 * @brief Returns the speed of the peripheral clock.  Nominally at 40Mhz
 * @author Max Dunne, 2013.09.01  */
unsigned int BOARD_GetPBClock()
{
    return PB_CLOCK;
}


#ifdef BOARD_TEST


#define MAXPOWTWO 20

int main(void)
{
    BOARD_Init();

    //    int curPow2 = 12;
    //    int i;
    TRISDbits.TRISD4 = 0;
    LATDbits.LATD4 = 0;
    //will do a pulse of each power of two
    //using scope can determine the length of timing for nops in test harnesses
    //    for(curPow2=0;curPow2<=MAXPOWTWO;curPow2++)
    //    {
    //    while (1) {
    //        LATDbits.LATD4 ^= 1;
    //        for (i = 0; i < 1830000; i++) {
    //            asm("nop");
    //        }
    //        //LATDbits.LATD4 = 0;
    //    }
    //will need a scope to test this module, the led should blink at the maximum rate
    while (1) {
        LATDbits.LATD4 ^= 1;
    }
}


#endif