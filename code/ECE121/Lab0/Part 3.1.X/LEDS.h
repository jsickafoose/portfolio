#ifndef LEDS_H
#define LEDS_H

#include "BOARD.h"
#include <xc.h>

 //Initializes Leds by setting TRISE and LATE to 0
#define LEDS_Init() do { \
    TRISE = 0x00; \
    LATE = 0x00; \
} while (0)

//Sets LATE to input x
#define LEDS_SET(x) (LATE = x)

//Returns LATE value
#define LEDS_GET() LATE

#endif