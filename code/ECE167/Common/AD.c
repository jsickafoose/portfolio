/*
 * File:   AD.c
 * Author: mdunne
 *
 * Created on November 22, 2011, 8:57 AM
 */

#include <xc.h>
#include <BOARD.h>
#include <AD.h>

#include <sys/attribs.h>

#include <serial.h>

#include <stdio.h>

/*******************************************************************************
 * PRIVATE #DEFINES                                                            *
 ******************************************************************************/

//#define AD_DEBUG_VERBOSE


#define NUM_AD_PINS 6
#define NUM_AD_PINS_UNO 16


//#define AD_DEBUG_VERBOSE
#ifdef AD_DEBUG_VERBOSE
#include "serial.h"
#define dbprintf(...) while(!IsTransmitEmpty()); printf(__VA_ARGS__)
#else
#define dbprintf(...)
#endif



#define ALLADPINS (AD_A0|AD_A1|AD_A2|AD_A3|AD_A4|AD_A5)




/*******************************************************************************
 * PRIVATE VARIABLES                                                            *
 ******************************************************************************/
static unsigned int AD1PCFG_MASKS[NUM_AD_PINS] = {_AD1PCFG_PCFG2_MASK, _AD1PCFG_PCFG4_MASK,
    _AD1PCFG_PCFG8_MASK, _AD1PCFG_PCFG10_MASK, _AD1PCFG_PCFG12_MASK, _AD1PCFG_PCFG14_MASK};

static unsigned int AD1CSSL_MASKS[NUM_AD_PINS] = {_AD1CSSL_CSSL2_MASK, _AD1CSSL_CSSL4_MASK, 
    _AD1CSSL_CSSL8_MASK, _AD1CSSL_CSSL10_MASK, _AD1CSSL_CSSL12_MASK, _AD1CSSL_CSSL14_MASK};

static unsigned int AD1PCFG_POS[NUM_AD_PINS] = {_AD1PCFG_PCFG2_POSITION, _AD1PCFG_PCFG4_POSITION,
    _AD1PCFG_PCFG8_POSITION, _AD1PCFG_PCFG10_POSITION, _AD1PCFG_PCFG12_POSITION, _AD1PCFG_PCFG14_POSITION};


static unsigned int ActivePins;
static unsigned int PinsToAdd;
static unsigned int PinsToRemove;
static unsigned int PinCount;
static unsigned int ADValues[NUM_AD_PINS];
static int PortMapping[NUM_AD_PINS];

static char ADActive;
static char ADNewData = FALSE;



/*******************************************************************************
 * PRIVATE FUNCTION PROTOTYPES                                                            *
 ******************************************************************************/
char AD_SetPins(void);

/*******************************************************************************
 * PUBLIC FUNCTIONS                                                           *
 ******************************************************************************/

/**
 * @function AD_Init(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief Initializes the A/D subsystem and enable battery voltage monitoring
 * @author Max Dunne, 2013.08.10 */
char AD_Init(void)
{

    if (ADActive) {
        return ERROR;
    }
    int pin = 0;
	ADActive = TRUE;
    AD_SetPins();
    for (pin = 0; pin < NUM_AD_PINS; pin++) {
        ADValues[pin] = -1;
    }
    IEC1bits.AD1IE = 0;
    IFS1bits.AD1IF = 0;
    IPC6bits.AD1IP = 1;
    IPC6bits.AD1IS = 3;
    IEC1bits.AD1IE = 1;
    AD1CON1bits.ON = 1;
    ADNewData = FALSE;
    //wait for first reading to ensure  battery monitor starts in the right spot
    while (!AD_IsNewDataReady()) {
#ifdef AD_DEBUG_VERBOSE
        PutChar('.');
#endif
    }
    //set the first values for the battery monitor filter

    return SUCCESS;
}

/**
 * @function AD_AddPins(unsigned int AddPins)
 * @param AddPins - Use #defined AD_XX OR'd together for each A/D Pin you wish to add
 * @return SUCCESS OR ERROR
 * @brief Remove pins from the A/D system.  If any pin is not active it returns an error
 * @author Max Dunne, 2013.08.15 */
char AD_AddPins(unsigned int AddPins)
{
    if (!ADActive) {
        dbprintf("%s called before enable\r\n", __FUNCTION__);
        return ERROR;
    }
    if ((AddPins == 0) || (AddPins > ALLADPINS)) {
        dbprintf("%s returning ERROR with pins outside range: %X\r\n", __FUNCTION__, AddPins);
        return ERROR;
    }
    if (ActivePins & AddPins) {
        dbprintf("%s Returning ERROR for pins already in state: %X \r\n", __FUNCTION__, AddPins);
        return ERROR;
    }
    //setting the pins to be added during the next interrupt cycle
    PinsToAdd |= AddPins;
    return SUCCESS;
}

/**
 * @function AD_RemovePins(unsigned int RemovePins)
 * @param RemovePins - Use #defined AD_XX OR'd together for each A/D Pin you wish to remove
 * @return SUCCESS OR ERROR
 * @brief Remove pins from the A/D system. If any pin is not active it returns an error
 * @author Max Dunne, 2013.08.15 */
char AD_RemovePins(unsigned int RemovePins)
{
    if (!ADActive) {
        dbprintf("%s called before enable\r\n", __FUNCTION__);
        return ERROR;
    }
    if ((RemovePins == 0) || (RemovePins > ALLADPINS)) {
        dbprintf("%s returning ERROR with pins outside range: %X\r\n", __FUNCTION__, RemovePins);
        return ERROR;
    }
    if (!(ActivePins & RemovePins)) {
        dbprintf("%s Returning ERROR for pins already in state: %X \r\n", __FUNCTION__, RemovePins);
        return ERROR;
    }

    //setting the pins to be added during the next interrupt cycle
    PinsToRemove |= RemovePins;
    return SUCCESS;
}

/**
 * @function AD_ActivePins(void)
 * @param None
 * @return Listing of all A/D pins that are active
 * @brief Returns a variable of all active A/D pins. An individual pin can be determined if
 *        active by "anding" with the AD_PORTXX Macros.
 * @note This will not reflect changes made with AD_AddPins or AD_RemovePins until the next A/D
 *       interrupt cycle.
 * @author Max Dunne, 2013.08.15 */
unsigned int AD_ActivePins(void)
{
    return ActivePins;
}

/**
 * @function AD_IsNewDataReady(void)
 * @param None
 * @return TRUE or FALSE
 * @brief This function returns a flag indicating that the A/D has new values since the last
 *        read of a value
 * @author Max Dunne, 2013.08.15 */
char AD_IsNewDataReady(void)
{
    if (ADNewData) {
        ADNewData = FALSE;
        return TRUE;
    }
    return FALSE;
}

/**
 * @function AD_ReadADPin(unsigned int Pin)
 * @param Pin - Used #defined AD_XX to select pin
 * @return 10-bit AD Value or ERROR
 * @brief Reads current value from buffer for given pin
 * @author Max Dunne, 2011.12.10 */
unsigned int AD_ReadADPin(unsigned int Pin)
{
    if (!ADActive) {
        dbprintf("%s returning ERROR before enable\r\n", __FUNCTION__);
        return ERROR;
    }
    if (!(ActivePins & Pin)) {
        dbprintf("%s returning error with unactivated pin: %X %X\r\n", __FUNCTION__, Pin);
        return ERROR;
    }
    unsigned char TranslatedPin = 0;
    while (Pin > 1) {

        Pin >>= 1;
        TranslatedPin++;
    }
    return ADValues[PortMapping[TranslatedPin]];
}

/**
 * @function AD_End(void)
 * @param None
 * @return None
 * @brief Disables the A/D subsystem and release the pins used
 * @author Max Dunne, 2013.09.20 */
void AD_End(void)
{
    int pin;
    if (!ADActive) {
        return;
    }
    IEC1bits.AD1IE = 0;
    AD1CON1CLR = _AD1CON1_ON_MASK;
    PinsToRemove = ALLADPINS;
    AD_SetPins();
    for (pin = 0; pin < NUM_AD_PINS; pin++) {
        ADValues[pin] = -1;
    }
    ActivePins = 0;
    PinCount = 0;   
    AD1PCFG = 0xFF;
}

/*******************************************************************************
 * PRIVATE FUNCTIONS                                                       *
 ******************************************************************************/

/**
 * @function AD_SetPins(void)
 * @param None
 * @return SUCCESS OR ERROR
 * @brief Connects pins in PinstoAdd to the A/D system and removes the pins in PinsToRemove
 * @note Private Function. DO NOT USE.
 * @author Max Dunne, 2013.08.15 */
char AD_SetPins(void)
{
    if (!ADActive) {
        return ERROR;
    }
    unsigned int cssl = 0;
    unsigned int pcfg = 0;
    unsigned int rempcfg = 0;
    unsigned char CurPin = 0;
    unsigned int CurPinOrder = 0x00;
    int ADMapping[NUM_AD_PINS_UNO];
    AD1CON1CLR = _AD1CON1_ON_MASK; //disable A/D system and interrupt
    IEC1bits.AD1IE = 0;
    PinCount = 0;

    //determine the new set of active pins
    ActivePins |= PinsToAdd;
    ActivePins &= ~PinsToRemove;
    //initialize the mapping array to -1
    for (CurPin = 0; CurPin < NUM_AD_PINS_UNO; CurPin++) {
        ADMapping[CurPin] = -1;
    }
    for (CurPin = 0; CurPin < NUM_AD_PINS; CurPin++) {
        PortMapping[CurPin] = -1; //reset all ports to unmapped
        if ((ActivePins & (1 << CurPin)) != 0) { //if one of the pins is active
            //build masks and remap pins
            cssl |= AD1CSSL_MASKS[CurPin];
            pcfg |= AD1PCFG_MASKS[CurPin];
            ADMapping[AD1PCFG_POS[CurPin]] = CurPin;
            PinCount++;
        }
        if ((PinsToRemove & (1 << CurPin)) != 0) {//generate removal masks
            rempcfg |= AD1PCFG_MASKS[CurPin];
        }
    }
    for (CurPin = 0; CurPin < NUM_AD_PINS_UNO; CurPin++) {//translate AD Mapping to Port Mapping
        if (ADMapping[CurPin] != -1) {
            PortMapping[ADMapping[CurPin]] = CurPinOrder;
            CurPinOrder++;
        }
    }
    
    // this realistically does not need to be done every time we add a pin but it makes sure it works
    // future revisions many of these settings should be handled in the init
    AD1CON1bits.FORM = 0; // output is unsigned integer
    AD1CON1bits.SSRC = 0b111; // internal counter handles timing of sampling an conversion
    AD1CON1bits.ASAM = 1; // start sampling again after conversion is complete

    AD1CON2bits.VCFG = 0; // use AVdd and AVss for + and -
    AD1CON2bits.CSCNA = 1; // mux inputs together
    AD1CON2bits.SMPI = PinCount - 1; // set the number to scan for 1 less than wanted as zero is 1 to scan
    AD1CON2bits.BUFM = 0; // configure bugger as one large buffer

    AD1CON3bits.ADRC = 0; // use Peripheral clock for timing
    AD1CON3bits.SAMC = 29; // set the sample time, completely arbitrary, nearly the slowest possible
    AD1CON3bits.ADCS = 0x32; // set the conversion time, again arbitrary 

    AD1PCFGCLR = pcfg;
    TRISBSET = pcfg;
    AD1CSSL = cssl;
    AD1PCFGSET = rempcfg;
    AD1CON1SET = _AD1CON1_ON_MASK;
    PinsToAdd = 0;
    PinsToRemove = 0;
    IEC1bits.AD1IE = 1;
    return SUCCESS;
}

/**
 * @function ADCIntHandler
 * @param None
 * @return None
 * @brief Interrupt Handler for A/D. Reads all used pins into buffer.
 * @note This function is not to be called by the user
 * @author Max Dunne, 2013.08.25 */
void __ISR(_ADC_VECTOR, ipl1auto) ADCIntHandler(void)
{
    unsigned char CurPin = 0;
    IFS1bits.AD1IF = 0;
    for (CurPin = 0; CurPin <= PinCount; CurPin++) {
        ADValues[CurPin] = (*(&ADC1BUF0+((CurPin) * 4))); //read in new set of values, pointer math from microchip
    }
    //calculate new filtered battery voltage

    //if pins are changed add pins
    if (PinsToAdd | PinsToRemove) {
        AD_SetPins();
    }
    ADNewData = TRUE;
}





//#define AD_TEST
#ifdef AD_TEST



#include <xc.h>
#include "serial.h"
#include "AD.h"
#include <stdio.h>

#define DELAY(x)    {int wait; for (wait = 0; wait <= x; wait++) {asm("nop");}}
#define A_BIT       18300
#define A_LOT       183000
//#define DISABLE_ADINIT
#define TIMES_TO_READ 4000

#define ODD_ACTIVE (AD_A1|AD_A3|AD_A5)
#define EVEN_ACTIVE (AD_A0|AD_A2|AD_A4)

#define ALLADMINUSBATT ALLADPINS 

//#define ADPinHasChanged(PinsAdded)

int main(void)
{
    unsigned int wait = 0;
    int readcount = 0;
    unsigned int CurPin = 0;
    unsigned int PinListing = 0;
    char FunctionResponse = 0;
    char TestFailed = FALSE;
    BOARD_Init();
    AD_Init();
    AD_AddPins(AD_A0);
    while(1){
        if(AD_IsNewDataReady())
        {
            printf("\r\nReading: %d", AD_ReadADPin(AD_A0));
            DELAY(A_BIT);
        }
    }
//    //END MAXL
//    printf("\r\nUno A/D Test Harness\r\nThis will initialize all A/D pins and read them %d times\r\n", TIMES_TO_READ);
//    //printf("Value of pcfg before test: %X\r\n", AD1PCFG);
//    // while(!IsTransmitEmpty());
//    //AD_Init(BAT_VOLTAGE);
//    //AD_Init();
//    printf("Testing functionality before initialization\r\n");
//
//    /*adding pins individually */
//    printf("AD_AddPins on each pin indvidually which results in failure: ");
//    for (CurPin = 1; CurPin < ALLADPINS; CurPin <<= 1) {
//        FunctionResponse = AD_AddPins(CurPin);
//        if (FunctionResponse != ERROR) {
//            TestFailed = TRUE;
//            break;
//        }
//    }
//    if (TestFailed) {
//        printf("FAIL\r\n");
//    } else {
//        printf("PASSED\r\n");
//    }
//    TestFailed = FALSE;
//    /*removing pins individually*/
//    printf("AD_RemovePins on each pin indvidually which results in failure: ");
//    for (CurPin = 1; CurPin < ALLADPINS; CurPin <<= 1) {
//        FunctionResponse = AD_RemovePins(CurPin);
//        if (FunctionResponse != ERROR) {
//            TestFailed = TRUE;
//            break;
//        }
//    }
//    if (TestFailed) {
//        printf("FAIL\r\n");
//    } else {
//        printf("PASSED\r\n");
//    }
//    TestFailed = FALSE;
//    /*listing pins while inactive*/
//    printf("AD_ActivePins which should return 0: ");
//    PinListing = AD_ActivePins();
//    if (PinListing != 0x0) {
//        printf("FAILED\r\n");
//
//    } else {
//        printf("PASSED\r\n");
//    }
//    //    /*calling ned when inactive*/
//    //        printf("AD_End which should fail: ");
//    //        FunctionResponse = AD_End();
//    //        if (FunctionResponse != ERROR) {
//    //            printf("FAILED\r\n");
//    //        } else {
//    //            printf("PASSED\r\n");
//    //        }
//    /*activating module*/
//    printf("initializing using AD_Init: ");
//    FunctionResponse = AD_Init();
//    if (FunctionResponse != SUCCESS) {
//        printf("FAILED\r\n");
//    } else {
//        printf("PASSED\r\n");
//    }
//    /*attempting to reactivate*/
//    printf("initializing using AD_Init again returns error: ");
//    FunctionResponse = AD_Init();
//    if (FunctionResponse != ERROR) {
//        printf("FAILED\r\n");
//    } else {
//        printf("PASSED\r\n");
//    }
//    /*each pin added should succeed*/
//    printf("Adding each pin using AD_AddPins indivdually: ");
//    for (CurPin = 1; CurPin < ALLADMINUSBATT; CurPin <<= 1) {
//        PinListing = AD_ActivePins();
//        FunctionResponse = AD_AddPins(CurPin);
//        if (FunctionResponse != SUCCESS) {
//            TestFailed = TRUE;
//            break;
//        }
//        while (AD_ActivePins() != (PinListing | CurPin));
//    }
//    if (TestFailed) {
//        printf("FAIL\r\n");
//    } else {
//        printf("PASSED\r\n");
//    }
//    /*removing each pin should succeed */
//    printf("Removing each pin using AD_RemovePins indivdually: ");
//    for (CurPin = 1; CurPin < ALLADMINUSBATT; CurPin <<= 1) {
//        PinListing = AD_ActivePins();
//        FunctionResponse = AD_AddPins(CurPin);
//        if (FunctionResponse != SUCCESS) {
//            TestFailed = TRUE;
//            break;
//        }
//        while (AD_ActivePins() != (PinListing | CurPin));
//    }
//    if (TestFailed) {
//        printf("FAIL: %X\r\n", 0xFEED);
//    } else {
//        printf("PASSED\r\n");
//    }
//    while (1);
//    printf("We will now add the odd pins and wait for them to be activated");
//    AD_AddPins(ODD_ACTIVE);
//    while (!(AD_ActivePins() & ODD_ACTIVE)) {
//        if (IsTransmitEmpty()) {
//            printf("%X\r\n", AD_ActivePins());
//        }
//    }
//    printf("The Odd pins are now active as shown by Active pins: %X\r\n", AD_ActivePins());
//    printf("We will now enable the even pins and wait for them to be activated");
//    AD_AddPins(EVEN_ACTIVE);
//    while (!(AD_ActivePins() & EVEN_ACTIVE));
//    printf("The Even pins are now active as shown by Active pins: %X\r\n", AD_ActivePins());
//
//
//    char numtoread = NUM_AD_PINS;
//    unsigned char cur = 0;
//    DELAY(400000)
//    while (readcount <= TIMES_TO_READ) {
//        DELAY(100000);
//        printf("\r\n");
//        for (cur = 0; cur < numtoread; cur++) {
//            printf("%d\t", AD_ReadADPin(1 << cur));
//        }
//        printf("\r\n");
//        readcount++;
//    }
//    printf("Done Reading Them\r\n");
//    AD_End();
//    printf("Value of pcfg after test: %X", AD1PCFG);
//
//    return 0;
}
#endif