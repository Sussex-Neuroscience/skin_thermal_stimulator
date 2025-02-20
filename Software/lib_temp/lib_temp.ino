#include "temp.h"
#include "PID_v1.h"

#define PIN_OUTPUT 9  // PWM pin to control power output

tempa ntc(8,11);
//Define Variables we'll be connecting to
double Setpoint, Input, Output;
//Specify the links and initial tuning parameters
double Kp=2, Ki=0.5, Kd=0;
int Direction = 1;

PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, P_ON_M, Direction);

void setup(void) {
  Serial.begin(9600);                 //initialize serial communication at a baud rate of 9600 
  ntc.begin();                        // setup the pin directions  
  myPID.SetMode(AUTOMATIC);           //turn the PID on
  
}
void loop(void) {
  Direction = ntc.setdirection();                  // set the peltier power leads direction and the PID direction
  myPID.SetControllerDirection(Direction);
  Input = ntc.gettemp();                          //get temperature readings
  Setpoint = ntc.settemp();                       // get the set temperature from serial
  myPID.Compute();                                // control temperature
  analogWrite(PIN_OUTPUT, Output);                // set the pwm value

  Serial.print("NTC: ");
  Serial.print(Input);
  Serial.print("SET: ");
  Serial.print(Setpoint);
  Serial.print("PWM: ");
  Serial.println(Output);

  delay(250);
}