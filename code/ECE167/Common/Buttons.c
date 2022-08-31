#include "Buttons.h"

// These masks are used for checking if the buttons have been the same value over all 4 tracked
// timesteps.
#define BUTTON1_STATE_MASK 0x11111
#define BUTTON2_STATE_MASK 0x22222
#define BUTTON3_STATE_MASK 0x44444
#define BUTTON4_STATE_MASK 0x88888

#define BUTTON1_DOWN_EVENT_MASK   0x01111
#define BUTTON1_UP_EVENT_MASK     0x10000
#define BUTTON2_DOWN_EVENT_MASK   0x02222
#define BUTTON2_UP_EVENT_MASK     0x20000
#define BUTTON3_DOWN_EVENT_MASK   0x04444
#define BUTTON3_UP_EVENT_MASK     0x40000
#define BUTTON4_DOWN_EVENT_MASK   0x08888
#define BUTTON4_UP_EVENT_MASK     0x80000

// Mask for the position of each button
#define BUTTON1_POS_MASK (1<<0)
#define BUTTON2_POS_MASK (1<<1)
#define BUTTON3_POS_MASK (1<<2)
#define BUTTON4_POS_MASK (1<<3)

void ButtonsInit(void)
{
    // Enable pin F1, D5, D6, D7 as inputs for buttons 1, 2, 3, and 4 respectively.
    TRISDSET = 0x00E0;
    TRISFSET = 0x0002;
}

uint8_t ButtonsCheckEvents(void)
{
    // The states of all buttons are tracked over the last 4 samples. Only once a button is read as
    // the same value over all 4 states does the estimated button state change.
    static uint16_t buttonSamples = 0;

    //Holds The Last Events for all four buttons.
    // An event only occurs if the last event is not the same.
    // We make the assumption that upon the first call no buttons are pressed.
    // A Button Up event means the bit is low

    static uint8_t LastButtonEvents = 0;

    uint8_t event = BUTTON_EVENT_NONE;

    // Append the current button state to our button state time vector. We do this before checking
    // for transitions as it simplifies things.
    uint32_t buttonSampleCheck = (((uint32_t) buttonSamples) << 4) | BUTTON_STATES();

    // Button 1 - From pressed to released
    if (((buttonSampleCheck & BUTTON1_STATE_MASK) == BUTTON1_UP_EVENT_MASK)
            &&(LastButtonEvents & BUTTON1_POS_MASK)) {
        event |= BUTTON_EVENT_1UP;
        LastButtonEvents &= ~BUTTON1_POS_MASK;
    }// Button 1 - From released to pressed
    else if (((buttonSampleCheck & BUTTON1_STATE_MASK) == BUTTON1_DOWN_EVENT_MASK)
            &&!(LastButtonEvents & BUTTON1_POS_MASK)) {
        event |= BUTTON_EVENT_1DOWN;
        LastButtonEvents |= BUTTON1_POS_MASK;
    }

    // Button 2 - From pressed to released
    if (((buttonSampleCheck & BUTTON2_STATE_MASK) == BUTTON2_UP_EVENT_MASK)
            &&(LastButtonEvents & BUTTON2_POS_MASK)) {
        event |= BUTTON_EVENT_2UP;
        LastButtonEvents &= ~BUTTON2_POS_MASK;
    }// Button 2 - From released to pressed
    else if (((buttonSampleCheck & BUTTON2_STATE_MASK) == BUTTON2_DOWN_EVENT_MASK)
            &&!(LastButtonEvents & BUTTON2_POS_MASK)) {
        event |= BUTTON_EVENT_2DOWN;
        LastButtonEvents |= BUTTON2_POS_MASK;
    }

    // Button 3 - From pressed to released
    if (((buttonSampleCheck & BUTTON3_STATE_MASK) == BUTTON3_UP_EVENT_MASK)
            &&(LastButtonEvents & BUTTON3_POS_MASK)) {
        event |= BUTTON_EVENT_3UP;
        LastButtonEvents &= ~BUTTON3_POS_MASK;
    }// Button 3 - From released to pressed
    else if (((buttonSampleCheck & BUTTON3_STATE_MASK) == BUTTON3_DOWN_EVENT_MASK)
            &&!(LastButtonEvents & BUTTON3_POS_MASK)) {
        event |= BUTTON_EVENT_3DOWN;
        LastButtonEvents |= BUTTON3_POS_MASK;
    }

    // Button 4 - From pressed to released
    if (((buttonSampleCheck & BUTTON4_STATE_MASK) == BUTTON4_UP_EVENT_MASK)
            &&(LastButtonEvents & BUTTON4_POS_MASK)) {
        event |= BUTTON_EVENT_4UP;
        LastButtonEvents &= ~BUTTON4_POS_MASK;
    }// Button 4 - From released to pressed
    else if (((buttonSampleCheck & BUTTON4_STATE_MASK) == BUTTON4_DOWN_EVENT_MASK)
            &&!(LastButtonEvents & BUTTON4_POS_MASK)) {
        event |= BUTTON_EVENT_4DOWN;
        LastButtonEvents |= BUTTON4_POS_MASK;
    }

    // And be sure to record the new button state samples.
    buttonSamples = (uint16_t) buttonSampleCheck;

    return event;
}
