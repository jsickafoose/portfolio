///////////////////////////////////////////////////////
// Created by Jacob Sickafoose on 4/16/22            //
// Updated for the Crow Prototype                    //
// design is outlined in the deliverable, 4.?.?      //
///////////////////////////////////////////////////////
#include <Arduino.h>

//////////////////////
// PUBLIC # DEFINES //
//////////////////////
#define DAC PIN_A12   // Defines the DAC pin as A12 or 26
#define buttonIn 17    // Defines the button input pin as A4 or 18
#define period 10000 // Frequency of signal in microseconds
#define amplitude 2   // Sets the milliamp target amplitude we want, calculated out

#define IO_1_1 10     // Defines two IO pins switch the H-Bridge for pair 1
#define IO_1_2 11     // pair1_pin1 and pair1_pin2 corresponding to pin 10 and 11 on the board

/*-----------------------------------------------------------------------------------------------*/
/*----------------Beginning of the private section which should remain unchanged-----------------*/
/*-----------------------------------------------------------------------------------------------*/

///////////////////////
// PRIVATE # DEFINES //
///////////////////////
#define LED LED_BUILTIN   // Gives the LED a better name
#define MAX_DAC_VAL 4095  // MAX DAC value

///////////////////////
// PRIVATE Variables //
///////////////////////
elapsedMicros usec;           // Creates microsecond timer variable
uint8_t timerMode = 0;        // Stores the flipflop for IO pins to swap positions in time
int IO_Duty = 0;
int IO_Delay = 0;             // Stores delay number for IO
int Off_Delay = 0;

//////////////////////////////
// PRIVATE FUNCTION HEADERS //
//////////////////////////////
int8_t FreqChange(int8_t Mode);
// bool buttonPress(void);   // Might implement later for debouncing the button


///////////////////////
// PRIVATE FUNCTIONS //
///////////////////////

// This function just cycles changes the frequency and keeps track of the current mode
int8_t FreqChange(int8_t Mode){
  static int8_t freqMode = 1;  // Stores the current mode

  // If the mode given = 7, just cycle the modes. Otherwise, use the mode commanded
  if (Mode > 0){
    freqMode = Mode;
  }

  // Set the desired frequency based on the mode
  if (freqMode == 1){
    IO_Duty = 100;
  }
  else if (freqMode == 2){
    IO_Duty = 50;
  }
  else{
    IO_Duty = 100/freqMode;
  }

  IO_Delay = (IO_Duty*period)/200;
  Off_Delay = (period-(IO_Delay*2));

  // Ends by cycling the mode, let's it go 1-5 for a total of 5 modes
  if (Mode > 0){ // If we are picking our own mode, just return that and don't cycle modes
    return Mode;
  }
  else if (freqMode >= 5){         
    freqMode = 1;
    return 5;
  }
  else {
    freqMode++;
  }
  return (freqMode-1);
}



////////////////
// Board INIT //
////////////////
void setup() {
  // Intializing Pins as Outputs
  pinMode(DAC, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(IO_1_1, OUTPUT);
  pinMode(IO_1_2, OUTPUT);

  // Inits the buttonIn pin
  pinMode(buttonIn, INPUT);
  FreqChange(-1);

  analogWriteResolution(12);  // Sets the DAC analog resolution to 12-bits, the maximum
  // analogWrite(DAC, MAX_DAC_VAL);
  analogWrite(DAC, 0);
  digitalWrite(LED, LOW);     // Inits LED as off
  digitalWrite(IO_1_1, LOW);
  digitalWrite(IO_1_2, LOW);
}



///////////////
// MAIN LOOP //
///////////////
void loop() {
  // This part changes the frequency if if button is pressed
  if (!digitalRead(buttonIn)){ // If button is pressed, meaning logic LOW
    // Display LED on
    digitalWrite(LED, HIGH);

    FreqChange(-1);

    // Delay by 2 seconds for some debouncing
    delay(2000);
  }
  else {
    digitalWrite(LED, LOW); // LED off when it is not changing mode
  }


  // This sets the IO pins to the new values
  // Electrode High
  if (timerMode == 1 && usec > IO_Delay){

    digitalWrite(IO_1_1, HIGH);
    digitalWrite(IO_1_2, LOW);

    usec = 0;
    timerMode = 2;
  }
  // Electrode 0V
  else if (timerMode == 2 && usec > IO_Delay){
    digitalWrite(IO_1_1, LOW);
    digitalWrite(IO_1_2, LOW);

    usec = 0;
    timerMode = 0;
  }
  // Electrode LOW
  else if (timerMode == 0 && usec > Off_Delay){
    digitalWrite(IO_1_1, LOW);
    digitalWrite(IO_1_2, HIGH);

    usec = 0;
    timerMode = 1;
  }

  // digitalWrite(IO_1_1, LOW);
  // digitalWrite(IO_1_2, LOW);
}