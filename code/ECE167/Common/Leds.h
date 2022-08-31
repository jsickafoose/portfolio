#ifndef LEDS_H
#define LEDS_H

/**
 * @file
 * This library provides an interface for controlling the LEDs on the Explorer16 development board.
 *
 * Use of this library follows a standard INIT() + SET()/GET() interface in a header-only library
 * through the user of macros. LEDS_INIT() must be called before either LEDS_SET() or LEDS_GET() are
 * called. LEDS_SET() allows for the entire bank of LEDs to be updated at once.
 */

/**
 * This macro initializes all LEDs for use. It enables the proper pins as outputs and also turns all
 * LEDs off.
 */
#define LEDS_INIT() do {LATECLR = 0xFF; TRISECLR = 0xFF;} while (0)

/**
 * Provides a way to quickly get the status of all 8 LEDs into a uint8, where a bit is 1 if the LED
 * is on and 0 if it's not. The LEDs are ordered such that bit 7 is LED8 and bit 0 is LED0.
 */
#define LEDS_GET() (LATE & 0xFF)

/**
 * This macro sets the LEDs on according to which bits are high in the argument. Bit 0 corresponds
 * to LED0.
 * @param leds Set the LEDs to this value where 1 means on and 0 means off.
 */
#define LEDS_SET(leds) do { LATE = (leds); } while (0)

#endif // LEDS_H
