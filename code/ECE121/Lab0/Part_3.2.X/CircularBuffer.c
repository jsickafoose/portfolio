#include "CircularBuffer.h"
#include <xc.h> // This was not included in Buttons.h

#define MAX_BUFFER_LENGTH 16 // This is where you set max buffer length

static struct {
    unsigned int head;
    unsigned int tail;
    unsigned char data[MAX_BUFFER_LENGTH];
} circBuffer;



void Buffer_Init(void){
    circBuffer.head = 0;
    circBuffer.tail = 0;
}

void AddData(char inData){
    circBuffer.data[circBuffer.tail] = inData;
    circBuffer.tail = (circBuffer.tail + 1) % MAX_BUFFER_LENGTH;
}

char GetData(void){
    char output = circBuffer.data[circBuffer.head];
    circBuffer.head = (circBuffer.head + 1) % MAX_BUFFER_LENGTH;
    return output;
}

unsigned int itemNumber(void){
    int output = circBuffer.tail - circBuffer.head;
    return output;
}