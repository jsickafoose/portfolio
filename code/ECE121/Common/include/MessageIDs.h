/* 
 * File:   MessageIDs.h
 */

#ifndef MESSAGEIDS_H
#define MESSAGEIDS_H

typedef enum {
    ID_INVALID = 0, /** Invalid Packet, used as an error return from functions */
    ID_DEBUG = 128, /**  Array of chars displayed as a string<br>
                    * This string is <b>NOT</b> NULL terminated. */
    ID_LEDS_SET, /** A single char whose bits represent each of the LEDs 
                    * respectively, to be set on the uc32 IO-Shield. */
    ID_LEDS_STATE, /**  The ID for the response to ID_LEDS_GET. Corresponding 
                    * payload is a single char (byte). Ex: If LED1 is on, and 
                    * all others are off, respond with 0x01,  */
    ID_LEDS_GET, /**  A request for the current states of each of the LEDS. The 
                    * payload is of length one (just the ID). The response 
                    * packet to a packet with this ID should have an ID of 
                    * ID_LEDS_STATE. */
    ID_PING, /** Packet with this ID has payload of an unsigned int (4 bytes). */
    ID_PONG, /** Payload should be an unsigned int (4 bytes). This ID is used in 
                *  response to an ID_PING packet. */
    ID_ROTARY_ANGLE, /**  Raw angle from an encoder as an unsigned 14-bit short. */
    ID_PING_DISTANCE, /**  unsigned int of distance in millimeters. */
    ID_COMMAND_SERVO_PULSE, /** Number of servo ticks represented by an 
                            * unsigned int interpreted as microseconds. */
    ID_SERVO_RESPONSE, /** Unsigned int interpreted as microseconds requested */
    ID_LAB2_ANGLE_REPORT, /**  int of degrees*1000 followed by status char. */
    ID_LAB2_INPUT_SELECT, /** Designates which input to use in Lab2 Application: 0 PING SENSOR, 1 ENCODER */
    ID_LOG_INT_ONE, /** Log a single integers to a .csv file. */
    ID_LOG_INT_TWO, /** Log two integers to a .csv file. */
    ID_LOG_INT_THREE, /** Log three integers to a .csv file. */
    ID_LOG_INT_FOUR, /** Log four integers to a .csv file. */
    ID_LOG_INT_FIVE, /** Log five integers to a .csv file. */
    ID_ADC_SELECT_CHANNEL, /** Char between 0-3 to select a channel to work with */
    ID_ADC_SELECT_CHANNEL_RESP, /** Echo of channel set to to confirm channel change */
    ID_ADC_READING, /**  Two shorts holding the filtered and unfiltered values of a single channel */
    ID_ADC_FILTER_VALUES, /** Filter values consisting of an array of 32 shorts */
    ID_ADC_FILTER_VALUES_RESP, /** Char of channel filter values were applied to */
    ID_NVM_READ_BYTE, /** Integer address to read from */
    ID_NVM_READ_BYTE_RESP, /** Unsigned char value holding value stored in address */
    ID_NVM_WRITE_BYTE, /** Integer address and char value to store */
    ID_NVM_WRITE_BYTE_ACK, /** No payload but indicating that value was written. */
    ID_NVM_READ_PAGE, /** Integer page to read from. */
    ID_NVM_READ_PAGE_RESP, /** The 64 bytes of the requested page */
    ID_NVM_WRITE_PAGE, /** Integer address followed by 64 bytes of data to write */
    ID_NVM_WRITE_PAGE_ACK, /** No payload but indication that page was written */
    ID_LAB3_CHANNEL_FILTER, /** Byte with upper four bytes being channel and bottom 4 being filter, sent when there is a system change */
    ID_LAB3_SET_FREQUENCY, /** Unsigned short representing a new frequency in the valid range */
    ID_LAB3_FREQUENCY_ONOFF, /** Controls Frequency output: 0 Off, 1 ON */
    ID_COMMAND_OPEN_MOTOR_SPEED, /** Integer representing Motor speed in units of <b>Duty Cycle</b> (+/- 1000) for open loop control. */
    ID_COMMAND_OPEN_MOTOR_SPEED_RESP, /** No payload but indicating command was accepted */
    ID_REPORT_RATE, /** Signed integer representing the raw rate */
    ID_FEEDBACK_SET_GAINS, /** Trio of integers representing Porportional, Integral, and Derivative Gain */
    ID_FEEDBACK_SET_GAINS_RESP, /** No Payload indicating new gains were set */
    ID_FEEDBACK_REQ_GAINS, /** no payload but requesting current gains */
    ID_FEEDBACK_CUR_GAINS, /** Trio of integers representing Porportional, Integral, and Derivative Gain */
    ID_FEEDBACK_RESET_CONTROLLER, /** Reset the integrated value back to zero */
    ID_FEEDBACK_RESET_CONTROLLER_RESP, /** Integrated value has been clear response */
    ID_FEEDBACK_UPDATE, /** int reference followed by int sensorValue */
    ID_FEEDBACK_UPDATE_OUTPUT, /** int control output */
    ID_COMMANDED_RATE, /** integer commanded rate in raw ticks/count */
    ID_REPORT_FEEDBACK, /** Trio of integers representing error, current rate, and PWM
                        * <b> error = Commanded Rate - Current Rate */
    ID_COMMANDED_POSITION, /** signed integer represented commanded position in raw ticks */
    ID_ENCODER_ABS, /** signed integer representing absolute positon of motor accounting for rollovers */
    ID_LAB5_REPORT, /** Four signed integers with the following information
                    * <b>current error
                    * <b>Reference signal
                    * <b>Sensor signal
                    * <b>commanded position, yes there will be a duplicate value in command mode */
    ID_LAB5_ADC, /** two signed shorts of the filtered readings for both IR sensors */
    ID_LAB5_SET_MODE, /** one unsigned char representing the new mode required */
    ID_LAB5_REQ_MODE, /** no payload but micro must respond with current mode */
    ID_LAB5_CUR_MODE, /** one unsigned char representing the current mode of the lab 5 application
                        * <b>0: commanded position mode
                        * <b>1: sensor input mode */
} MessageIDS_t;

#endif	/* MESSAGEIDS_H */