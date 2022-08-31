#include "Buttons.h"
#include <xc.h> // This was not included in Buttons.h


//typedef enum {
//    BUTTON_EVENT_NONE = 0x00,
//    BUTTON_EVENT_1UP = 0x01,
//    BUTTON_EVENT_1DOWN = 0x02,
//    BUTTON_EVENT_2UP = 0x04,
//    BUTTON_EVENT_2DOWN = 0x08,
//    BUTTON_EVENT_3UP = 0x10,
//    BUTTON_EVENT_3DOWN = 0x20,
//    BUTTON_EVENT_4UP = 0x40,
//    BUTTON_EVENT_4DOWN = 0x80
//} ButtonEventFlags;

/**
 * This function initializes the proper pins such that the buttons 1-4 may be used by modifying
 * the necessary bits in TRISD/TRISF. Only the bits necessary to enable the 1-4 buttons are
 * modified so that this library does not interfere with other libraries.
 */
void Buttons_Init(void){
    TRISD = 0x00E0;
    TRISF = 0x0002;
}

/**
 * This function checks the button states and returns any events that have occured since the last
 * call. In the case of the first call to ButtonsCheckEvents() after ButtonsInit(), the function
 * should assume that the buttons start in an off state with value 0. Therefore if no buttons are
 * pressed when ButtonsCheckEvents() is first called, BUTTONS_EVENT_NONE should be returned. The
 * events are listed in the ButtonEventFlags enum at the top of this file. This function should be
 * called repeatedly.
 *
 * This function also performs debouncing of the buttons following the guide to debouncing in the lab.
 * Each call to ButtonsCheckEvents should sample the buttons once.
 *
 * NOTE: This will not work properly without ButtonsInit() being called beforehand.
 * @return A bitwise-ORing of the constants in the ButtonEventFlags enum or BUTTON_EVENT_NONE if no
 *         event has occurred.
 */
uint8_t ButtonsCheckEvents(void){
    uint8_t lastButtonState = BUTTON_STATES(); // Makes return value, counter, and a variable to keep track of the lastButtonState
    uint8_t events = BUTTON_EVENT_NONE;
    static int counter = 0;
    while (lastButtonState == BUTTON_STATES() && counter < 5){ // Checks 5 times to debounce
        counter++;
        lastButtonState = BUTTON_STATES();
    }
    
    if (counter == 5){ // If debounce was successful
        if ((lastButtonState & 0x01) == 0x01){ // If the button is being pushed down, sets value
            events |= BUTTON_EVENT_1DOWN;
        }
        else if ((lastButtonState & 0x01) == 0x00){ // If button 1 is not pushed up, event 1up set
            events |= BUTTON_EVENT_1UP;             // In my original BUTTONS.c from CE13, I never even had BUTTON_EVENT's UP setup
        }
        if ((lastButtonState & 0x02) == 0x02){
            events |= BUTTON_EVENT_2DOWN;
        }
        else if ((lastButtonState & 0x02) == 0x00){
            events |= BUTTON_EVENT_2UP;
        }
        if ((lastButtonState & 0x04) == 0x04){
            events |= BUTTON_EVENT_3DOWN;
        }
        else if ((lastButtonState & 0x04) == 0x00){
            events |= BUTTON_EVENT_3UP;
        }
        if ((lastButtonState & 0x08) == 0x08){
            events |= BUTTON_EVENT_4DOWN;
        }
        else if ((lastButtonState & 0x08) == 0x00){
            events |= BUTTON_EVENT_4UP;
        }
    }
    return events;
}