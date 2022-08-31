/* 
 * @file    QEI.c
 * @brief   Quadrature Encoder sensing module
 * @author  Jacob SickafooseS
 * @date    4/27/2022
 * @detail  This module uses the change notify peripheral to interface to a quadrature encoder. 
 *          If you are unfamiliar with change notify please read the lab appendix before beginning.
 *          The peripheral is configured to generate an interrupt on any change in input of pins RD6
 *          or RD7 (pins 36 and 37 on the Uno32). The interrupt will not tell you which pin changed
 *          states so you will need to implement a simple state machine to handle the transitions and
 *          keep track of the encoder count.
 *          NOTE: Encoder A and B must be input to pins 36 and 37
 */

/*******************************************************************************
 * INCLUDES                                                                    *
 ******************************************************************************/
#include "BOARD.h"
#include <xc.h>
#include <sys/attribs.h>


/*******************************************************************************
 * PUBLIC #DEFINES                                                             *
 ******************************************************************************/
 
 
 /******************************************************************************
 * Module level variables                                                      *
 ******************************************************************************/
static int count = 0;
static int temp = 0;
static int A = 0;
static int B = 0;
static uint8_t tickFlag = 0;

enum state {
    START,
    COUNT_UP,
    COUNT_DOWN
};

static enum state state = START; // Creates the ENUM
void RunStateMachine(int A, int B);

/**
 * @function QEI_Init(void)
 * @param none
 * @brief  Enables the Change Notify peripheral and sets up the interrupt, anything
 *         else that needs to be done to initialize the module. 
 * @return SUCCESS or ERROR (as defined in BOARD.h)
*/
char QEI_Init(void){
    // INIT Change notify
    CNCONbits.ON = 1; // Change Notify On
    CNENbits.CNEN15 = 1; //enable one phase
    CNENbits.CNEN16 = 1; //enable other phase
    int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
    IFS1bits.CNIF = 0; // clear interrupt flag
    IPC6bits.CNIP = 1; //set priority
    IPC6bits.CNIS = 3; // and sub priority
    IEC1bits.CNIE = 1; // enable change notify
    // the rest of the function goes here
    TRISDbits.TRISD6 = 1; // Sets pin 36 as input for pin A
    TRISDbits.TRISD7 = 1; // Sets pin 37 as input for pin B
 }

/**
 * @function QEI_GetPosition(void) 
 * @param none
 * @brief This function returns the current count of the Quadrature Encoder in ticks.      
*/
int QEI_GetPosition(){
    return count;
}

/**
 * @Function QEI_ResetPosition(void) 
 * @param  none
 * @return none
 * @brief  Resets the encoder such that it starts counting from 0.
*/
void QEI_ResetPosition(){
    count = 0;
}

void __ISR(_CHANGE_NOTICE_VECTOR) ChangeNotice_Handler(void) {
    static char readPort = 0;
    readPort = PORTD; // this read is required to make the interrupt work
    IFS1bits.CNIF = 0;
    A = PORTDbits.RD6;
    B = PORTDbits.RD7;
    RunStateMachine(A, B);
 }

// I only needed 3 states. Not counting, counting up, and counting down
void RunStateMachine(int A, int B){
    switch(state){
        case START:
            tickFlag = 0; // Flag so it only ticks when it stops for a moment
            if (A == 0 && B == 1){ // Depending on which one goes high, counts up or down
                state = COUNT_UP;
            }
            else if (A == 1 && B == 0){
                state = COUNT_DOWN;
            }
            break;
        
        case COUNT_UP:
            if (!tickFlag){ // Prevents double ticks
                count++;
                if (count > 360){
                    count -= 361;
                }
                tickFlag = 1;
            }
            if (A == 1 && B == 1){
                state = START;
            }
            break;
            
        case COUNT_DOWN:
            if (!tickFlag){
                count--;
                if (count < -360){
                    count += 361;
                }
                tickFlag = 1;
            }
            if (A == 1 && B == 1){
                state = START;
            }
            break;
    }
}