/**
 * @file    PING.h
 * @brief   Ultrasonic Ping Sensor sensing module
 * @author  Jacob Sickafoose
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
/*******************************************************************************
 * INCLUDES                                                                    *
 ******************************************************************************/
#include "BOARD.h"
#include "timers.h"
#include <xc.h>
#include <sys/attribs.h>



/*******************************************************************************
 * PRIVATE GLOBAL VARIABLES                                                    *
 ******************************************************************************/
enum state{
    WAITING_FOR_HEAD,
    READING_LENGTH,
    READING_PAYLOAD,
    READING_LEDS,
    READING_TAIL,
    COMPARE_CHECKSUM,
    READING_END1,
    READING_END2
};

static enum state state = WAITING_FOR_HEAD; // Creates the ENUM
static int mode = 0;
static int prevTime = 0;
static int elapsedTime = 0;

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
char PING_Init(void){
    // following block inits the timer
             T4CON = 0;
             T4CONbits.TCKPS = 0b110;
             PR4 = 0x927C;  // this is not the timer value wanted
             T4CONbits.ON = 1;
             IFS0bits.T4IF = 0;
             IPC4bits.T4IP = 3;
             IEC0bits.T4IE = 1;
  
             // following block inits change notify
             CNCONbits.ON = 1; // Change Notify On
             CNENbits.CNEN14 = 1;
             int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
             IFS1bits.CNIF = 0; // clear interrupt flag
             IPC6bits.CNIP = 1; //set priority
             IPC6bits.CNIS = 3; // and sub priority
             IEC1bits.CNIE = 1; // enable change notify
               //Anything else that needs to occur goes here
//    // following block inits the timer
//    T4CON = 0;
//    T4CONbits.TCKPS = 0b110;
//    PR4 = 0x927C;  // Sets timer to 37500 for a rollover of every 60ms
//    T4CONbits.ON = 1;
//    IFS0bits.T4IF = 0;
//    IPC4bits.T4IP = 3;
//    IEC0bits.T4IE = 1;
// 
//    // following block inits change notify
//    CNCONbits.ON = 1; // Change Notify On
//    CNENbits.CNEN14 = 1;
//    int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
//    IFS1bits.CNIF = 0; // clear interrupt flag
//    IPC6bits.CNIP = 1; //set priority
//    IPC6bits.CNIS = 3; // and sub priority
//    IEC1bits.CNIE = 1; // enable change notify
    
    //Anything else that needs to occur goes here
    TRISFbits.TRISF1 = 0;   // Sets pin 4 as output for trigger
    TRISDbits.TRISD5 = 1;   // Sets pin 34 as input for the echo
    LATFbits.LATF1 = 0;     // Inits trigger pin to low
    TIMERS_Init();          // Makes sure timers.c is initialized because we utilize it here
}

/**
 * @function    PING_GetDistance(void)
 * @brief       Returns the calculated distance in mm using the sensor model determined
 *              experimentally. 
 *              No I/O should be done in this function
 * @return      distance in mm
 */
unsigned int PING_GetDistance(void){
    return ((elapsedTime*1000)/6536)+10; // Found using the least squares in Google Sheets
}

/**
 * @function    PING_GetTimeofFlight(void)
 * @brief       Returns the raw microsecond duration of the echo from the sensor.
 *              NO I/O should be done in this function.
 * @return      time of flight in uSec
 */
unsigned int PING_GetTimeofFlight(void){
    return elapsedTime;
}

void __ISR(_CHANGE_NOTICE_VECTOR) ChangeNotice_Handler(void) {
    static char readPort = 0;
    readPort = PORTD; // this read is required to make the interrupt work
    IFS1bits.CNIF = 0; 
    //Anything else that needs to occur goes here
    // If the port is high during this interupt, then we start the timer. Else, save the time elapsed
    if (PORTDbits.RD5){
        prevTime = TIMERS_GetMicroSeconds();
    }
    else{
        elapsedTime = TIMERS_GetMicroSeconds() - prevTime;
    }
}

void __ISR(_TIMER_4_VECTOR) Timer4IntHandler(void) {
    IFS0bits.T4IF = 0;
    //Anything else that needs to occur goes here
    if (!mode){
        LATFbits.LATF1 = 1; // Sets trigger high
        PR4 = 0x0007;       // Sets timer to trigger in 10microseconds
        mode = 1;
    }
    else{
        LATFbits.LATF1 = 0; // Sets trigger low
        PR4 = 0x927C;       // Sets timer back to 60ms
        mode = 0;
    }
}