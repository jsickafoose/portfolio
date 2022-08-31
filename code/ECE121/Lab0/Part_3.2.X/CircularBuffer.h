#ifndef CircularBuffer_H
#define CircularBuffer_H

/*
 * 
*/

#include <stdint.h>

/*
 * Sets the head and tail of the buffer array
 */
void Buffer_Init(void);

/*
 * Adds data to the buffer
 */
void AddData(char inData);

/*
 * Retrieves data from the buffer
 */
char GetData(void);

/*
 * Returns the number of items currently in the buffer
 */
unsigned int itemNumber(void);

#endif // CircularBuffer_H
