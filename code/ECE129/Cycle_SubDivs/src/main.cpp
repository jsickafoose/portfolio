///////////////////////////////////////////////////////
// Created by Jacob Sickafoose on 4/16/22            //
// Updated for the Crow Prototype                    //
// design is outlined in the deliverable, 4.?.?      //
///////////////////////////////////////////////////////
#include <Arduino.h>

//////////////////////
// PUBLIC # DEFINES //
//////////////////////
#define buttonIn 4   // Defines the button input pin as 4
#define period 10000  // Frequency of signal in microseconds

#define IO_1 16     // Defines two IO pins switch the H-Bridge for pair 1
#define IO_2 19     // pair1_pin1 and pair1_pin2 corresponding to pin 10 and 11 on the board

/*-----------------------------------------------------------------------------------------------*/
/*----------------Beginning of the private section which should remain unchanged-----------------*/
/*-----------------------------------------------------------------------------------------------*/

///////////////////////
// PRIVATE # DEFINES //
///////////////////////
#define LED LED_BUILTIN   // Gives the LED a better name

///////////////////////
// PRIVATE Variables //
///////////////////////
elapsedMicros usec;           // Creates microsecond timer variable
elapsedMillis milli;

uint16_t LED_Delay = 0;
uint8_t timerMode = 0;        // Stores the flipflop for IO pins to swap positions in time
uint8_t LED_ON_FLAG = 0;
int IO_Duty = 0;
int IO_Delay = 0;             // Stores delay number for IO
int Off_Delay = 0;
uint16_t subdivisions = 1, counter = 1;
uint8_t pinChange = 1;

////////////////
// Board INIT //
////////////////
void setup() {
  // Intializing Pins as Outputs
  pinMode(LED, OUTPUT);
  pinMode(IO_1, OUTPUT);
  pinMode(IO_2, OUTPUT);

  // Inits the buttonIn pin
  pinMode(buttonIn, INPUT);

  digitalWrite(LED, LOW);     // Inits LED as off
  digitalWrite(IO_1, LOW);
  digitalWrite(IO_2, LOW);

  Off_Delay = period/2;
  IO_Delay = 1750;
}



///////////////
// MAIN LOOP //
///////////////
void loop() {
  // Changes the frequency if if button is pressed
  if (!digitalRead(buttonIn)){ // If button is pressed, meaning logic LOW
    // Display LED on
    digitalWrite(LED, HIGH);

    if (subdivisions == 4){
      subdivisions = 35;
    }
    else if (subdivisions == 35){
      subdivisions = 105;
    }
    else if (subdivisions == 105){
      subdivisions = 175;
    }
    else if (subdivisions >= 175){
      subdivisions = 1;
    }
    else {
      subdivisions++;
    }

    // Delay by 2 seconds for some debouncing
    delay(700);
  }
  else {
    digitalWrite(LED, LOW); // LED off when it is not changing mode
  }



  // Timer for LED flashing
  if (milli > LED_Delay){
    milli = 0;

    if (LED_ON_FLAG == 1) {
      digitalWrite(LED, HIGH);
      LED_ON_FLAG = 0;
      LED_Delay = 100;
    }
    else{
      digitalWrite(LED, LOW);
      LED_ON_FLAG = 1;
      LED_Delay = 2000;
    }
    
  }


  // Code to calculate IO_Delay from subdivisions
  IO_Delay = 1750/subdivisions;



  // Timer for setting IO High/Low Values
  // Electrode 0V
  if (timerMode == 0){
    if (pinChange){
      digitalWrite(IO_1, LOW);
      digitalWrite(IO_2, LOW);
      pinChange = 0;
    }
    if (usec > Off_Delay){
      usec = 0;

      timerMode = 1;
      pinChange = 1;
    }
  }
  // Electrode HIGH
  if (timerMode == 1){
    if (pinChange){
      digitalWrite(IO_1, HIGH);
      digitalWrite(IO_2, LOW);
      pinChange = 0;
    }
    if (usec > IO_Delay){
      usec = 0;

      timerMode = 2;
      pinChange = 1;
    }
  }
  // Electrode LOW
  if (timerMode == 2){
    if (pinChange){
      digitalWrite(IO_1, LOW);
      digitalWrite(IO_2, HIGH);
      pinChange = 0;
    }
    if (usec > IO_Delay){
      usec = 0;

      if (counter < subdivisions){ // Now the counter determines if it goes HIGH again or goes back to 0V state
        timerMode = 1;
        counter++;
      }
      else{
        counter = 1;
        timerMode = 0;
      }

      pinChange = 1;
    }
  }
}