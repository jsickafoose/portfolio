/*
 * File:   ICM20948.h
 * Author: mdunne
 *
 * Software module to communicate with the IMU over I2C.
 * Provides access to each raw sensor axis along with raw temperature
 * 
 */

#ifndef ICM20948_H
#define ICM20948_H


/**
 * @Function ICM20948_Init(Rate)

 * @return 0 if error, 1 if succeeded
 * @brief  Initializes the ICM 20948 for usage. Sensors will be at Accel: 2g,Gyro:  250dps and Mag: 16-bit
 * @author Max Dunne */
char ICM20948_Init(void);


/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelX(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelY(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelZ(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroX(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroY(void);


/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroZ(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelX(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelY(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadAccelZ(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroX(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroY(void);


/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadGyroZ(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadMagX(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadMagY(void);

/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadMagZ(void);


/**
 * @Function ICM20948_Read*()
 * @param None
 * @return Returns raw sensor reading
 * @brief reads sensor axis as given by name
 * @author Max Dunne*/
int ICM20948_ReadTemp(void);

#endif