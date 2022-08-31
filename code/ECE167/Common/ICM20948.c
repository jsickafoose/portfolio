#include <ICM20948.h>
#include <I2C.h>
#include <BOARD.h>
#include <xc.h>
#include <stdio.h>


/*******************************************************************************
 * PRIVATE #DEFINES                                                            *
 ******************************************************************************/

#define ACCGYR_I2C_ADDRESS 0x69
#define ACCGYR_WHO_AM_I_VAL 0xEA

#define MAG_AK09916_I2C_ADDR 0x0C
#define MAG_AK09916_WHO_AM_I_VAL 0x9

#define MAG_MODE_WANTED 0b01000

#define ICM_POWER_SETTING 0x02

#define ICM_BYPASS_EN 0x02

/*******************************************************************************
 * PRIVATE VARIABLES                                                           *
 ******************************************************************************/

static enum {
    ICM_WHO_AM_I = 0, // Value of 0xEA stored in ACCGYR_WHO_AM_I_VAL
    LP_CONFIG = 0x05,
    PWR_MGMT_1, // power controls including sleep bit
    PWR_MGMT_2,
    INT_PIN_CONFIG = 0x0F, //I2C bypass annoyance
    INT_ENABLE,
    INT_ENABLE_1,
    INT_ENABLE_2,
    INT_ENABLE_3,
    I2C_MST_STATUS = 0x17,
    INT_STATUS = 0x19,
    INT_STATUS_1,
    INT_STATUS_2,
    INT_STATUS_3,
    DELAY_TIMEH = 0x28,
    DELAY_TIMEL,
    ACCEL_XOUT_H = 0x2D,
    ACCEL_XOUT_L,
    ACCEL_YOUT_H,
    ACCEL_YOUT_L,
    ACCEL_ZOUT_H,
    ACCEL_ZOUT_L,
    GYRO_XOUT_H,
    GYRO_XOUT_L,
    GYRO_YOUT_H,
    GYRO_YOUT_L,
    GYRO_ZOUT_H,
    GYRO_ZOUT_L,
    TEMP_OUT_H,
    TEMP_OUT_L,
    REG_BANK_SEL = 0x7F

} ICM20948_REGISTERS;

static enum {
    MAG_WHO_AM_I = 0x1, // should read 0x9
    MAG_ST1 = 0x10,
    MAG_HXL = 0x11,
    MAG_HXH,
    MAG_HYL,
    MAG_HYH,
    MAG_HZL,
    MAG_HZH,
    MAG_ST2 = 0x18, // status register needs to be read every time so data actually changes
    MAG_CNTL1 = 0x30, // despite being named as a control register it is a dummy
    MAG_CNTL2, // allows setting of mode, section 9.3 of datasheet covers them
    MAG_CNTL3, // software reset


} AK09916_REGISTERS;

/*******************************************************************************
 * PRIVATE FUNCTION PROTOTYPES
 ******************************************************************************/
void DelayMicros(uint32_t microsec);

/*******************************************************************************
 * PUBLIC FUNCTIONS                                                           *
 ******************************************************************************/

/**
 * @Function ICM20948_Init(Rate)

 * @return 0 if error, 1 if succeeded
 * @brief  Initializes the ICM20948 for usage. This will set all sensors to approximately 100HZ
 * and Accel: 2g,Gyro:  250dps and Mag: 16-bit for the sensors
 * @author Max Dunne */
char ICM20948_Init(void)
{
    unsigned int intReturn;
    unsigned char byteReturn;
    DelayMicros(250000 << 2); // delaying to ensure that successive programs do not glitch the sensor

    intReturn = I2C_Init(I2C_DEFAULT_RATE);
    if (intReturn != I2C_DEFAULT_RATE) {
        return FALSE;
    }
    
    I2C1CONbits.PEN = 1; // after the delay we are also going to send a stop condition to supposedly clear the bus
    while (I2C1CONbits.PEN == 1); 
    
    I2C_WriteReg(ACCGYR_I2C_ADDRESS, REG_BANK_SEL, 0); // need to be in bank 1 for the initial settings
    byteReturn = I2C_ReadRegister(ACCGYR_I2C_ADDRESS, ICM_WHO_AM_I);
    if (byteReturn != ACCGYR_WHO_AM_I_VAL) {
        printf("IMU Did not respond to Who Am I.");
        return FALSE;

    }
    // wake up the device from sleep along with setting the clock to a reasonable source
    I2C_WriteReg(ACCGYR_I2C_ADDRESS, PWR_MGMT_1, ICM_POWER_SETTING);

    // in default mode the device does not allow access to the mage directly, something we want so it needs to get changed
    I2C_WriteReg(ACCGYR_I2C_ADDRESS, INT_PIN_CONFIG, ICM_BYPASS_EN);

    byteReturn = I2C_ReadRegister(MAG_AK09916_I2C_ADDR, MAG_WHO_AM_I);
    if (byteReturn != MAG_AK09916_WHO_AM_I_VAL) {
        printf("Magnetometer Did not respond to Who Am I\r\n");
        return FALSE;
    }

    // turn on the mag at 100Hz
    byteReturn = I2C_WriteReg(MAG_AK09916_I2C_ADDR, MAG_CNTL2, MAG_MODE_WANTED);
    if (!byteReturn) {
        printf("Configuration of Mag Failed\r\n");
        return FALSE;
    }

    // TODO: using the default settings for the gyro/accel which does mean a DLPF is enabled
    // potentially it makes sense to disable it in future quarters


    I2C_WriteReg(ACCGYR_I2C_ADDRESS, REG_BANK_SEL, 0); // when config complete want to be in bank 0
    return TRUE;


}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelX(void)
{
    return I2C_ReadInt(ACCGYR_I2C_ADDRESS, ACCEL_XOUT_H, TRUE);
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelY(void)
{
    return I2C_ReadInt(ACCGYR_I2C_ADDRESS, ACCEL_YOUT_H, TRUE);
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelZ(void)
{
    return I2C_ReadInt(ACCGYR_I2C_ADDRESS, ACCEL_ZOUT_H, TRUE);
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroX(void)
{
    return I2C_ReadInt(ACCGYR_I2C_ADDRESS, GYRO_XOUT_H, TRUE);
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroY(void)
{
    return I2C_ReadInt(ACCGYR_I2C_ADDRESS, GYRO_YOUT_H, TRUE);
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroZ(void)
{
    return I2C_ReadInt(ACCGYR_I2C_ADDRESS, GYRO_ZOUT_H, TRUE);
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadMagX(void)
{
    int sensorValue = I2C_ReadInt(MAG_AK09916_I2C_ADDR, MAG_HXL, FALSE);
    I2C_ReadRegister(MAG_AK09916_I2C_ADDR, MAG_ST2); // read the status register to clear it
    return sensorValue;
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadMagY(void)
{
    int sensorValue = I2C_ReadInt(MAG_AK09916_I2C_ADDR, MAG_HYL, FALSE);
    I2C_ReadRegister(MAG_AK09916_I2C_ADDR, MAG_ST2); // read the status register to clear it
    return sensorValue;
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadMagZ(void)
{
    int sensorValue = I2C_ReadInt(MAG_AK09916_I2C_ADDR, MAG_HZL, FALSE);
    I2C_ReadRegister(MAG_AK09916_I2C_ADDR, MAG_ST2); // read the status register to clear it
    return sensorValue;
}

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadTemp(void)
{

    return I2C_ReadInt(ACCGYR_I2C_ADDRESS, TEMP_OUT_H, TRUE);
}

/*******************************************************************************
 * PRIVATE FUNCTIONS                                                           *
 ******************************************************************************/

void DelayMicros(uint32_t microsec)
{
    uint32_t tWait, tStart, tCurrent;

    // Calculate the amount of wait time in terms of core processor frequency.
    tWait = (80000000L / 2000000) * microsec;
    asm volatile("mfc0   %0, $9" : "=r"(tStart));
    tCurrent = tStart;
    while ((tCurrent - tStart) < tWait) {
        asm volatile("mfc0   %0, $9" : "=r"(tCurrent));
    }// wait for the time to pass
}


#ifdef ICM20948_TEST

#include "serial.h"
#include <xc.h>

#define POWERPIN_LAT LATFbits.LATF1
#define POWERPIN_TRIS TRISFbits.TRISF1

int main(void)
{
    char initResult;
    BOARD_Init();

    printf("Welcome to the ICM20948 test compiled at " __DATE__ " " __TIME__ ". Sensor will be brought up and then values displayed\r\n");
    while (!IsTransmitEmpty());
    POWERPIN_LAT = 0;
    POWERPIN_TRIS = 0;
    POWERPIN_LAT = 1;

    DelayMicros(100000);
    initResult = ICM20948_Init();
    if (initResult != TRUE) {
        printf("Initialization of IMU failed, stopping here\r\n");
    } else {
        printf("Initialization succeeded\r\n");
        while (1) {
            if (IsTransmitEmpty()) {
                printf("Gyro: (%+06d, %+06d, %+06d)   ", ICM20948_ReadGyroX(), ICM20948_ReadGyroY(), ICM20948_ReadGyroZ());
                printf("Accel: (%+06d, %+06d, %+06d)   ", ICM20948_ReadAccelX(), ICM20948_ReadAccelY(), ICM20948_ReadAccelZ());
                printf("Mag: (%+06d, %+06d, %+06d)   ", ICM20948_ReadMagX(), ICM20948_ReadMagY(), ICM20948_ReadMagZ());
                printf("Temp: %+06d", ICM20948_ReadTemp());
                printf("\r\n");
                DelayMicros(100000);
            }
        }
    }
    while (1);
}

#endif