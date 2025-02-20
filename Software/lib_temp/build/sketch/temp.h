#line 1 "C:\\Users\\snn30\\OneDrive - University of Sussex\\Devs\\skin_thermal_stimulator\\Software\\lib_temp\\temp.h"
#ifndef TEMP_H
#define TEMP_H

#include "Arduino.h"

#define ntc_pin A3         // Pin,to which the voltage divider is connected
#define nominal_resistance 10000       //Nominal resistance at 25⁰C
#define nominal_temeprature 25   // temperature for nominal resistance (almost always 25⁰ C)
#define samplingrate 5    // Number of samples
#define beta 3976  // The beta coefficient or the B value of the thermistor (usually 3000-4000) check the datasheet for the accurate value.
#define Rref 10000   //Value of  resistor used for the voltage divider


class tempa 
{
  public:
    tempa(int pina, int pinb);
    void begin();
    int setdirection();
    double gettemp();
    double settemp();

    uint8_t i;
    float  R = 0;
    float tempsamples = 2;
    int samples = 0;   
    float input = 30;
    float temp = 0;
    float preinput = 0;
    float pretemp = 0;
    bool heat;

  private:
    int _pina;
    int _pinb;

};


#endif 