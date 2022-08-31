/* 
 * File:   Protocol.c
 * Author: Jacob Sickafoose
 */
#include "Protocol.h"
#include "BOARD.h"
#include "CircularBuffer.h"
#include "MessageIDs.h"

#include <stdio.h>
#include <string.h>
#include <sys/attribs.h>
#include <xc.h>

/*******************************************************************************
 * PUBLIC #DEFINES                                                            *
 ******************************************************************************/
#define Protocol_test = 1
//#define PACKETBUFFERSIZE 5  // how many payloads the buffer has to store, not bytes
//
//#define MAXPAYLOADLENGTH 128 // note that this does include the ID
//
//#define HEAD 204
//#define TAIL 185

/*******************************************************************************
 * PUBLIC DATATYPES
 ******************************************************************************/
static circBuff TXBuffer; // Creates the static circular Buffers we will need
static circBuff RXBuffer;
static circBuff RXBuffLen;
static uint8_t led = 0x00;
static unsigned char RX; // Global variable for RX
static int GlobalError; // Global Error variable for error flag
static int i;

//typedef enum {}States;
//States STATE = IDLE;

enum state {
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

static uint8_t semaphore;
static uint8_t semaphoreRX;
uint8_t leds;
/*******************************************************************************
 * PUBLIC FUNCTIONS                                                           *
 ******************************************************************************/
/**
 * @Function Protocol_Init(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief 
 * @author mdunne */
int Protocol_Init(void){ // Basically all on page 724 of the Family Reference Manual
    Buffer_Init(&TXBuffer); // Inits buffers, and LED's
    Buffer_Init(&RXBuffer);
    Buffer_Init(&RXBuffLen);
    LEDS_INIT();
    
    semaphore = 0;
    semaphoreRX = 1;
    GlobalError = SUCCESS;
    
    // Clear Control Registers
    U1MODECLR = 0xFFFFFFFF;
    
    // Calculate Baud Rate Generator
    U1BRG = 21; // The chart said 21 in decimal for my desired baudrate of 115200
    
    // Initializes interrupts
    U1STAbits.UTXISEL0 = 0x02; // Sets interrupt to be generated when the transmit buffer becomes fully empty
    U1STAbits.URXISEL0 = 0; // Sets interrupt for RX when any character is received
    
    IFS0bits.U1TXIF = 0;    // Sets flags to 0 just in case I guess
    IFS0bits.U1RXIF = 0;
    
    IPC6bits.U1IP = 1;  // Sets the interrupt priority to 1 (lowest) for the UART
    
    IEC0bits.U1TXIE = 1; // These enable the interrupts for TX and RX
    IEC0bits.U1RXIE = 1;
    
    // Set UART1 for 8-N-1
    U1MODEbits.PDSEL = 0; // Sets PDSEL <1:0> (UxMODE<2:1>) bits to the 8bit data, no parity setting
    U1MODEbits.STSEL = 0; // Sets STSEL (Stop selection bit) to 1 stop bit
    
    // Enable UART1
    U1MODEbits.ON = 1;
    // Enable Transmission
    U1STAbits.UTXEN = 1;
    // Enable Reception
    U1STAbits.URXEN = 1;
    return SUCCESS;
}

/**
 * @Function int Protocol_SendMessage(unsigned char len, void *Payload)
 * @param len, length of full <b>Payload</b> variable
 * @param Payload, pointer to data, will be copied in during the function
 * @return SUCCESS or ERROR
 * @brief 
 * @author mdunne */
int Protocol_SendMessage(unsigned char len, unsigned char ID, void *Payload){
    unsigned char checksum = ID; // Initialize the checksum with the ID
    
    PutChar(0xCC); // Enqueue the HEAD
    PutChar(len + 1); // Enqueue the Length
    PutChar(ID); // Enqueue the ID
    
//    if (ID == 0x80){ // I tried using memcpy when my SendMessage wouldn't send char arrays, and it worked, but then sending LED state stopped working
//        unsigned char PayloadCpy[len]; // So I just have an if statement
//        memcpy(PayloadCpy, Payload, len);
//    
//        for (i = 0; i < (uint8_t)len;){
//            if (PutChar(PayloadCpy[i]) == SUCCESS){ // I can still only load so many characters into my circular buffer, then the cpu has to wait
//                checksum = Protocol_CalcIterativeChecksum(PayloadCpy[i], checksum);
//                i++;
//            }
//            else { asm("nop"); }
//        }
//    }
//    else {
        
        unsigned char payloadChar;
        for (i = 0; i < len; i++){
            payloadChar = ((unsigned char*)Payload)[i]; // I can't believe how long it took me to find this syntax, and then get it to work.
            PutChar(payloadChar);                       // I wish I wouldn't have even tried using my other syntax, even if it did work initially
            checksum = Protocol_CalcIterativeChecksum(payloadChar, checksum);
//            Payload = (char*)Payload+1;
        }
//        char payloadChar;
//        for (i = 0; i < len;){
//            payloadChar = (((char*)Payload)[i]);
//            if (PutChar(payloadChar) == SUCCESS){ // This forces CPU to wait if TXBuffer full
//                checksum = Protocol_CalcIterativeChecksum(payloadChar, checksum);
////                Payload = (char*)Payload+1;
//                i++;
//            }
//            else { asm("nop"); }
//        }
//    }
    
    
    PutChar((char)0xB9); // Enqueue the TAIL
    PutChar((char)checksum);
    PutChar((char)0x0D); // Enqueue \r
    PutChar((char)0x0A); // Enqueue \n
    
    return SUCCESS;
}

/**
 * @Function int Protocol_SendDebugMessage(char *Message)
 * @param Message, Proper C string to send out
 * @return SUCCESS or ERROR
 * @brief Takes in a proper C-formatted string and sends it out using ID_DEBUG
 * @warning this takes an array, do <b>NOT</b> call sprintf as an argument.
 * @author mdunne */
int Protocol_SendDebugMessage(char *Message){
    int leng = strlen(Message);
    char msg[MAXPAYLOADLENGTH];
    for (i = 0; i < leng; i++){
        msg[i] = Message[i];
//        Message++;
    }
    Protocol_SendMessage(leng, '\x80', msg);
}

/**
 * @Function unsigned char Protocol_ReadNextID(void)
 * @param None
 * @return Reads ID of next Packet
 * @brief Returns ID_INVALID if no packets are available
 * @author mdunne */
unsigned char Protocol_ReadNextID(void){
    if (Protocol_IsMessageAvailable()){
        return GetData(&RXBuffer);
    }
    else return 0;
}

/**
 * @Function int Protocol_GetPayload(void* payload)
 * @param payload, Memory location to put payload
 * @return SUCCESS or ERROR
 * @brief 
 * @author mdunne */
int Protocol_GetPayload(void* payload){
    if (Protocol_IsMessageAvailable() == FALSE){
        return ERROR;
    }
    else {
        int leng = (int)GetData(&RXBuffLen);
//        unsigned char payArray[4];
        for (i = 0; i < leng; i++){
//            ((unsigned char*)payload)[i] = GetData(&RXBuffer);
//            payload = ((int)payload << 8) | GetData(&RXBuffer);
//            payArray[i] = GetData(&RXBuffer);
            ((unsigned char*)payload)[i] = GetData(&RXBuffer);
//            payPointer = GetData(&RXBuffer);
//            payPointer++;
//            payload = (int)payload | GetData(&RXBuffer);
//            payload = (int)payload | ((GetData(&RXBuffer))>>(leng*2)/* & (0xFF)>>(leng*2)*/);
//            payload = (char*)payload + 1;
        }
//        for (i = 0; i < leng; i++){
//            ((unsigned char*)payload)[i] = payArray[i];
//        }
//        payload = payArray;
        return SUCCESS;
    }
}

/**
 * @Function char Protocol_IsMessageAvailable(void)
 * @param None
 * @return TRUE if Queue is not Empty
 * @brief 
 * @author mdunne */
char Protocol_IsMessageAvailable(void){
    if (itemNumber(&RXBuffer) > 0){
        return TRUE;
    }
    else return FALSE;
}

/**
 * @Function char Protocol_IsQueueFull(void)
 * @param None
 * @return TRUE is QUEUE is Full
 * @brief 
 * @author mdunne */
char Protocol_IsQueueFull(void){
    if (isFull(&TXBuffer)){
        return TRUE;
    }
    else return FALSE;
}

/**
 * @Function char Protocol_IsError(void)
 * @param None
 * @return TRUE if error
 * @brief Returns if error has occurred in processing, clears on read
 * @author mdunne */
char Protocol_IsError(void){
    if (GlobalError == ERROR){ // If the error is set
        GlobalError == SUCCESS; // Reset flag, and return TRUE
        return TRUE;
    }
    else return FALSE;
}

/**
 * @Function char Protocol_ShortEndednessConversion(unsigned short inVariable)
 * @param inVariable, short to convert endedness
 * @return converted short
 * @brief Converts endedness of a short. This is a bi-directional operation so only one function is needed
 * @author mdunne */
unsigned short Protocol_ShortEndednessConversion(unsigned short inVariable){
    unsigned short out = ((inVariable>>8) & 0x00FF | (inVariable<<8) & 0xFF00);
    return out;
}

/**
 * @Function char Protocol_IntEndednessConversion(unsigned int inVariable)
 * @param inVariable, int to convert endedness
 * @return converted short
 * @brief Converts endedness of a int. This is a bi-directional operation so only one function is needed
 * @author mdunne */
unsigned int Protocol_IntEndednessConversion(unsigned int inVariable){
    unsigned int out = ((inVariable>>24) & 0x000000FF | (inVariable>>8) & 0x0000FF00 | (inVariable<<8) & 0x00FF0000 | (inVariable<<24) & 0xFF000000);
    return out;
}


/*******************************************************************************
 * PRIVATE FUNCTIONS
 * generally these functions would not be exposed but due to the learning nature of the class they
 * are to give you a theory of how to organize the code internal to the module
 ******************************************************************************/
/**
 * @Function char Protocol_CalcIterativeChecksum(unsigned char charIn, unsigned char curChecksum)
 * @param charIn, new char to add to the checksum
 * @param curChecksum, current checksum, most likely the last return of this function, can use 0 to reset
 * @return the new checksum value
 * @brief Returns the BSD checksum of the char stream given the curChecksum and the new char
 * @author mdunne */
unsigned char Protocol_CalcIterativeChecksum(unsigned char charIn, unsigned char curChecksum){
    curChecksum = (curChecksum >> 1) + (curChecksum << 7);
    curChecksum += charIn;
    curChecksum &= 0xff;
    return curChecksum;
}

///**
// * @Function void Protocol_runReceiveStateMachine(unsigned char charIn)
// * @param charIn, next character to process
// * @return None
// * @brief Runs the protocol state machine for receiving characters, it should be called from 
// * within the interrupt and process the current character
// * @author mdunne */
void Protocol_RunReceiveStateMachine(unsigned char charIn){
    static uint8_t length; // static length of payload (including ID) variable
    static unsigned char payload[MAXPAYLOADLENGTH]; // static array of size max payload length, to temporarily store the payload
    static unsigned char cksum;
    static uint8_t ledFlag = 0;
    static char leds;
    static int j = 0;

    switch (state){
        case WAITING_FOR_HEAD:
            if (charIn == HEAD){ // If we receive a head
                state = READING_LENGTH; // Continue to the next state
            }
            break;
            
        case READING_LENGTH:
            length = (uint8_t)charIn;
            cksum = '\x00'; // Reset checksum
            j = 0; // Reset the i counter value
            ledFlag = 0; // Reset the LED flag
            state = READING_PAYLOAD;
            break;
            
        case READING_PAYLOAD:
            if (spaceLeft(&RXBuffer) <= length){ // If there isn't enough space for the message, just waits for the next one
                state = WAITING_FOR_HEAD;
                break;
            }
            if (j >= length - 1){ // If this will be the last run of the payload, set state to next
                state = READING_TAIL;
            }
            cksum = Protocol_CalcIterativeChecksum(charIn, cksum); // Keep calculating the running checksum
            if (j == 0 && charIn == 0x81){ // If the ID is LEDS_SET
                state = READING_LEDS; // Go to special LED set state
            }
            else if (j == 0 && charIn == 0x83){ // If the ID is LEDS_GET
                ledFlag = 2;
            }
            else {
                payload[j] = charIn; // Keep storing payload into temporary array
            }
            j++;
            break;
        case READING_LEDS:
            led = (uint8_t)charIn; // Now that we know the next char in will be an LED state, this sets it directly
            cksum = Protocol_CalcIterativeChecksum(charIn, cksum); // Keep calculating the running checksum
            ledFlag = 1;
            state = READING_TAIL;
            break;
        case READING_TAIL:
            if (charIn == TAIL){ // If the next charIn is the tail value
                state = COMPARE_CHECKSUM; // Move onto the next state
            }
            else { state = WAITING_FOR_HEAD;} // Else, 
            break;
            
        case COMPARE_CHECKSUM:
            if (cksum == charIn){ // If the calculated checksum is the same as this charIn which should be the checksum
                state = READING_END1; // Move on to the next state
            }
            else { state = WAITING_FOR_HEAD;} // Else, sends to start
            break;
            
        case READING_END1:
            if (charIn == 0x0D){ // If the penultimate char is correct
                state = READING_END2; // Scans for the next one
            }
            else { state = WAITING_FOR_HEAD;} // Else, sends to start
            break;
        case READING_END2:
            if (charIn == 0x0A){ // If the final char is correct
                if (ledFlag == 1){ // If it we were setting LEDs
                    LEDS_SET(led); // Set the LEDs now
                }
                else if (ledFlag == 2){
                    leds = LEDS_GET();
                    Protocol_SendMessage(1, '\x82', &leds);
                }
                else{
                    // Store length in RXBuff Len which stores the lengths of payloads in order
                    AddData(length - 1, &RXBuffLen);
                    for (j = 0; j < length; j++){
                        semaphoreRX = 1;
                        AddData(payload[j], &RXBuffer); // Adds all the data to the RXBuffer because it has been successfully vetted;
                        semaphoreRX = 0;
                    }
                }
            }
            state = WAITING_FOR_HEAD;
            break;
    }
}

/**
 * @Function char PutChar(char ch)
 * @param ch, new char to add to the circular buffer
 * @return SUCCESS or ERROR
 * @brief adds to circular buffer if space exists, if not returns ERROR
 * @author mdunne */
int PutChar(char ch){
    int out = ERROR;
    if (!(isFull(&TXBuffer))){ // If there is space on circBuff, write to it
        semaphore = 1; // Sets a variable, saying the TX Buffer is currently being modified
        AddData((unsigned char)ch, &TXBuffer);
        semaphore = 0;
        
        if (U1STAbits.TRMT){ // If the UART is idle, trigger the flag
            IFS0bits.U1TXIF = 1;
        }
        out = SUCCESS;
    }
    return out;
}

// Handles the UART Interrupt flags
void __ISR(_UART1_VECTOR) IntUart1Handler(void){
    if (IFS0bits.U1TXIF == 1){ // If it's the TX flag that went off
        IFS0bits.U1TXIF = 0; // Clear the transmit interrupt flag
        if (itemNumber(&TXBuffer) > 0/* && semaphore < 1*/){ // Only sets if buffer has something to set, and isn't in the middle of modifying any values
            U1TXREG = GetData(&TXBuffer); // Sets the U1TXRegister to the head of the circular buffer
        }
    }
    if (IFS0bits.U1RXIF == 1){
        IFS0bits.U1RXIF = 0; // Clear the receiver interrupt flag
//        if (semaphoreRX == 0){ // The moment I try any semaphores, everything breaks
            Protocol_RunReceiveStateMachine(U1RXREG); // Passes the RX register value directly into the run receive state machine
//        }
    }
    if (IFS0bits.U1EIF > 0){
        GlobalError = ERROR;
        IFS0bits.U1EIF = 0; // Error interrupt flag
    }
}

/**
 * This macro initializes all LEDs for use. It enables the proper pins as outputs and also turns all
 * LEDs off.
 */
#define LEDS_INIT() do {LATECLR = 0xFF; TRISECLR = 0xFF;} while (0)

/**
 * Provides a way to quickly get the status of all 8 LEDs into a uint8, where a bit is 1 if the LED
 * is on and 0 if it's not. The LEDs are ordered such that bit 7 is LED8 and bit 0 is LED0.
 */
#define LEDS_GET() (LATE & 0xFF)

/**
 * This macro sets the LEDs on according to which bits are high in the argument. Bit 0 corresponds
 * to LED0.
 * @param leds Set the LEDs to this value where 1 means on and 0 means off.
 */
#define LEDS_SET(leds) do { LATE = (leds); } while (0)

#ifdef Protocol_test

int main(void) {
    
    BOARD_Init();
    Protocol_Init();
    char testMessage[MAXPAYLOADLENGTH];
    sprintf(testMessage, "Protocol Test Compiled at %s %s", __DATE__, __TIME__);
    Protocol_SendDebugMessage(testMessage);
    while (1){
        int j;
        Protocol_SendDebugMessage("spam time");
        for (j = 0; j < 250000; j++){
            asm("nop");
        }
    }
    
    short shortTestValue = 0xDEAD;
    short shortResultValue;
    int intTestValue = 0xDEADBEEF;
    int intResultValue;
    
    shortResultValue = Protocol_ShortEndednessConversion(shortTestValue);
    sprintf(testMessage, "Short Endedness Conversion: IN: 0x%X OUT: 0x%X", shortTestValue&0xFFFF, shortResultValue&0xFFFF);
    Protocol_SendDebugMessage(testMessage);
    
    
    intResultValue = Protocol_IntEndednessConversion(intTestValue);
    sprintf(testMessage, "Int Endedness Conversion: IN: 0x%X OUT: 0x%X", intTestValue, intResultValue);
    Protocol_SendDebugMessage(testMessage);
    
    unsigned int pingValue = 0xfff;
    while (1) {
        if (Protocol_IsMessageAvailable()) {
            if (Protocol_ReadNextID() == ID_PING) {
                // send pong in response here
                Protocol_GetPayload(&pingValue);
                pingValue = Protocol_IntEndednessConversion(pingValue);
                pingValue>>=1;
                pingValue = Protocol_IntEndednessConversion(pingValue);
                pingValue;
                Protocol_SendMessage(4, ID_PONG, &pingValue);
            }
        }
    }
    while (1);
    
//    unsigned char hello[9]; //0XCC0183B9830D0A
//    hello[0] = '\xCC';
//    hello[1] = '\x01';
//    hello[2] = '\x83';
////    hello[3] = '\x78';
//    hello[3] = '\xB9';
//    hello[4] = '\x83';
//    hello[5] = '\x0D';
//    hello[6] = '\x0A';
//    hello[7] = '\0';
//    for (i = 0; hello[i] != '\0'; i++){
//        Protocol_RunReceiveStateMachine(hello[i]);
//    }
    
//    BOARD_Init();
//    Protocol_Init();
////    while (1){
////        if (RX != '\0'){
////            PutChar(RX);
////            RX = '\0';
////            asm("nop");
////        }
////        else { asm("nop"); }
////    }
//    char hello2[] = "Wow, I really wish this could have worked any other way, yet here we are...";
//    Protocol_SendDebugMessage(&hello2);
//    
//    Protocol_SendMessage(1, '\x82', 0x06);
//    
//    unsigned int dead = 0xDEADBEEF;
//    dead = Protocol_IntEndednessConversion(dead);
//    
//    unsigned short de = 0xDEAD;
//    unsigned short ad = 0xBEEF;
//    de = Protocol_ShortEndednessConversion(de);
//    ad = Protocol_ShortEndednessConversion(ad);

//    
//    
//    
//    while (1);
}

#endif