#ifndef CircularBuffer_H
#define CircularBuffer_H

#include <stdint.h>

#define MAX_BUFFER_LENGTH 256 // This is where you set max buffer length


typedef struct circBuff{
    unsigned int head;
    unsigned int tail;
    unsigned char data[MAX_BUFFER_LENGTH];
} circBuff;


/*
 * Sets the head and tail of the buffer array
 */
void Buffer_Init(circBuff *buff);

/*
 * Adds data to the buffer
 */
void AddData(unsigned char inData, circBuff *buff);

/*
 * Retrieves data from the buffer
 */
unsigned char GetData(circBuff *buff);

/*
 * Returns the number of items currently in the buffer
 */
int itemNumber(circBuff *buff);

/*
 * Returns the number empty slots
 */
int spaceLeft(circBuff *buff);

/*
 * Returns 1 if the buffer is full, 0 else
 */
uint8_t isFull(circBuff *buff);

#endif // CircularBuffer_H
