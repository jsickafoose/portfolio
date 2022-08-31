#ifndef COMMON_H
#define COMMON_H

// The standard boolean values of 'true' and 'false' are included through the stdbool.h library.
#include <stdbool.h>

// We also include the uint8_t, int8_t, uint16_t, etc. datatypes from stdint.h.
#include <stdint.h>

// Define some standard error codes.
enum {
    SIZE_ERROR = -1,
    STANDARD_ERROR,
    SUCCESS
};

#endif // COMMON_H
