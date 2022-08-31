/* 
 * File:   I2C.c
 * Author: Max
 *
 * Created on February 22, 2018, 1:06 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include <BOARD.h>
#include <serial.h>
#include <I2C.h>
#include <xc.h>


/*******************************************************************************
 * PRIVATE #DEFINES                                                            *
 ******************************************************************************/

#define F_PB (BOARD_GetPBClock())

//#define DEBUG_I2C_CHANNEL


#ifdef DEBUG_I2C_CHANNEL
#define dbprintf(...) printf(__VA_ARGS__)
#else
#define dbprintf(...)
#endif
/*******************************************************************************
 * PRIVATE VARIABLES                                                           *
 ******************************************************************************/
static char I2C_Inited = FALSE;
static char lastCommandError = FALSE;

/*******************************************************************************
 * PUBLIC FUNCTIONS                                                           *
 ******************************************************************************/

/**
 * @Function I2C_Init(Rate)
 * @param Rate - Clock rate for the I2C system
 * @return The clock rate set for the I2C system, 0 if already inited
 * @brief  Initializes the I2C System for use with the IMU
 * @author Max Dunne */
unsigned int I2C_Init(unsigned int Rate) {
    unsigned int RealRate = 0;
    if (!I2C_Inited) {

        I2C1CONbits.ON = 0;

        I2C1BRG = (F_PB / (2 * Rate)) - 2;


        I2C1CONbits.ON = 1;
        I2C_Inited = TRUE;
        RealRate = (F_PB) / ((I2C1BRG + 2)*2);
        I2C1CONbits.PEN = 1;
    while (I2C1CONbits.PEN == 1);
    }
    
    return RealRate;
}


/**
 * @Function I2C_ReadRegister(unsigned char I2CAddress,unsigned char deviceRegisterAddress)
 * @param I2CAddresss - 7-bit address of I2C device wished to interact with
 * @param deviceRegisterAddress - 8-bit address of register on device
 * @return Value at Register or 0
 * @brief  Reads one device register on chosen I2C device
 * @author Max Dunne*/
unsigned char I2C_ReadRegister(unsigned char I2CAddress, unsigned char deviceRegisterAddress) {
    unsigned char regContents = 0;
    lastCommandError = FALSE;
    if (!I2C_Inited) {
        return 0;
    }

    I2C1CONbits.SEN = 1; // send a start condition
    while (I2C1CONbits.SEN == 1); //wait for it to end, this is internal and can not stall

    I2C1TRN = I2CAddress << 1; // load transmission buffer with address and R/W and transmit

    while (I2C1STATbits.TRSTAT != 0); //wait for it, again no error possible

    if (I2C1STATbits.ACKSTAT == 1) {
        dbprintf("\r\nDevice failed to ACK\r\n");
        return 0;
    }

    I2C1TRN = deviceRegisterAddress;

    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {
        dbprintf("\r\nDevice failed to ACK\r\n");
        return 0;
    }
    I2C1CONbits.RSEN = 1;

    while (I2C1CONbits.RSEN == 1);
    I2C1TRN = (I2CAddress << 1) + 1;

    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {
        dbprintf("\r\nDevice failed to ACK\r\n");
        return 0;
    }
    I2C1CONbits.RCEN = 1;
    while (I2C1STATbits.RBF != 1);
    regContents = I2C1RCV;
    I2C1CONbits.PEN = 1;
    while (I2C1CONbits.PEN == 1);
    return regContents;



    return regContents;
}


/**
 * @Function I2C_WriteReg(unsigned char I2CAddress, unsigned char deviceRegisterAddress, char data)
 * @param I2CAddresss - 7-bit address of I2C device wished to interact with
 * @param deviceRegisterAddress - 8-bit address of register on device
 * @param data - data wished to be written to register
 * @return 0 if error and 1 if success
 * @brief  Writes one device register on chosen I2C device
 * @author Max Dunne*/
unsigned char I2C_WriteReg(unsigned char I2CAddress,unsigned char deviceRegisterAddress, char data) {

    I2C1CONbits.SEN = 1;
    while (I2C1CONbits.SEN == 1);
    I2C1TRN = (I2CAddress << 1);
    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {
        //printf("Device Responded with NACK upon addressing");
        return 0;
    }

    I2C1TRN = deviceRegisterAddress;
    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {

        return 0;
    }
    I2C1TRN = data;
    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {
        return 0;
    }
    I2C1CONbits.PEN = 1;
    while (I2C1CONbits.PEN == 1);

    return 1;
}


/**
 * @Function I2C_ReadInt(char I2CAddress, char deviceRegisterAddress, char isBigEndian)
 * @param I2CAddresss - 7-bit address of I2C device wished to interact with
 * @param deviceRegisterAddress - 8-bit lower address of register on device
 * @param isBigEndian - Boolean determining if device is big or little endian
 * @return 0 if error and 1 if success
 * @brief  Reads two sequential registers to build a 16-bit value. isBigEndian
 * whether the first bits are either the high or low bits of the value
 * @author Max Dunne*/
int I2C_ReadInt(char I2CAddress, char deviceRegisterAddress, char isBigEndian) {
    short Data = 0;
    I2C1CONbits.SEN = 1;
    while (I2C1CONbits.SEN == 1);
    I2C1TRN = I2CAddress << 1;
    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {
        //printf("Device Responded with NACK");
        return 0;
    }
    I2C1TRN = deviceRegisterAddress;
    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {
        //printf("Device Responded with NACK");
        return 0;
    }
    I2C1CONbits.RSEN = 1;
    while (I2C1CONbits.RSEN == 1);
    I2C1TRN = (I2CAddress << 1) + 1;
    while (I2C1STATbits.TRSTAT != 0);
    if (I2C1STATbits.ACKSTAT == 1) {
        //printf("Device Responded with NACK");
        return 0;
    }
    I2C1CONbits.RCEN = 1;
    //while(I2C1CONbits.RCEN==1);
    while (I2C1STATbits.RBF != 1);
    if (isBigEndian) {
        Data = I2C1RCV << 8;
    } else {
        Data = I2C1RCV;
    }
    I2C1CONbits.ACKEN = 1;
    while (I2C1CONbits.ACKEN == 1);
    I2C1CONbits.RCEN = 1;

    while (I2C1STATbits.RBF != 1);
    if (isBigEndian) {
        Data |= I2C1RCV;
    } else {
        Data |= I2C1RCV << 8;
    }
    I2C1CONbits.ACKDT = 1;
    I2C1CONbits.ACKEN = 1;
    while (I2C1CONbits.ACKEN == 1);
    I2C1CONbits.ACKDT = 0;
    I2C1CONbits.PEN = 1;
    while (I2C1CONbits.PEN == 1);
    return Data;


}



#ifdef I2C_TEST_HARNESS

#define I2C_ADDRESS 0b1001000 

static enum {
    TEMPERATURE_REGISTER,
    CONFIGURATION_REGISTER,
    TEMPERATURE_HYST_REGISTER,
    TEMPERATURE_LIMIT_REGISTER
} TCN75A_REGISTERS;

int main(void) {

    BOARD_Init();


    char conRegister = 0;
    char newconRegister = 0;
    unsigned int temperatureValue = 0;

    printf("\r\nStarting I2C at %d and getting %d", I2C_DEFUALT_RATE, I2C_Init(I2C_DEFUALT_RATE));

    printf("\r\nWe will now read in a config register, alter its value, write it back, and confirm the change");

    conRegister = I2C_ReadRegister(I2C_ADDRESS, CONFIGURATION_REGISTER);
    printf("\r\nConfiguration register is currently 0X%X", conRegister);
    conRegister ^= 0b10;
    printf("\r\nWe wish to change con register to   0X%X", conRegister);
    printf("\r\nThis changes the alert pin which will have no side effects");
    I2C_WriteReg(I2C_ADDRESS, CONFIGURATION_REGISTER, conRegister);

    newconRegister = I2C_ReadRegister(I2C_ADDRESS, CONFIGURATION_REGISTER);

    if (newconRegister == conRegister) {
        printf("\r\nConfiguration successfully changed to 0X%X", newconRegister);
    } else {
        printf("\r\nFailed configuration change");
        while (1);
    }
    printf("The code will now print 16-bit temperature data at max serial rate");

    while (1) {
        if (IsTransmitEmpty()) {
            temperatureValue = I2C_ReadInt(I2C_ADDRESS, TEMPERATURE_REGISTER, TRUE);
            printf("\r\nCurrent Temperature is %f", (float) (temperatureValue >> 4) / 16.0); //need to convert to celsius fp
        }
    }
    while (1);
    return 1;
}

#endif