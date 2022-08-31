#include "CircularBuffer.h"
#include <xc.h> // This was not included in Buttons.h

void Buffer_Init(circBuff *buff){
    buff->head = 0;
    buff->tail = 0;
}

uint8_t isFull(circBuff *buff){
    if ((((buff->tail - buff->head)*2)/2) >= (MAX_BUFFER_LENGTH - 1)){
        return 1;
    }
    else { return 0;}
}

int itemNumber(circBuff *buff){
    int output = (((buff->tail - buff->head)*2)/2);
    return output;
}

int spaceLeft(circBuff *buff){
    int output = (MAX_BUFFER_LENGTH - (((buff->tail - buff->head)*2)/2));
    return output;
}

void AddData(unsigned char inData, circBuff *buff){
    int i;
    if (isFull(buff) < 1){
        buff->data[buff->tail] = inData;
        buff->tail = ((buff->tail + 1) % MAX_BUFFER_LENGTH);
    }
    i = buff->tail;
}

unsigned char GetData(circBuff *buff){
    if (itemNumber(buff) > 0){
        char output = buff->data[buff->head];
        buff->head = (buff->head + 1) % MAX_BUFFER_LENGTH;
        return output;
    }
    else {
        return '\0';
    }
}