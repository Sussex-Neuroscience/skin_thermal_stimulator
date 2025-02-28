#include "temp.h"
#include "Arduino.h"

tempa::tempa(int pina, int pinb)
{
  _pina = pina;
  _pinb = pinb;
}
void tempa::begin()
{
  pinMode(_pina,OUTPUT);
  pinMode(_pinb,OUTPUT);
}
double tempa::gettemp()
{
   
  samples = 0;  //array to store the samples
  for (i = 0; i < samplingrate; i++) {
    samples += analogRead(ntc_pin);
    delay(10);
  }
 
  R = samples / samplingrate;
  
 // Calculate NTC resistance
  R = 1023 / R- 1;
  R = Rref / R;
  
  temp = R / nominal_resistance;     // (R/Ro)
  temp = log(temp);                  // ln(R/Ro)
  temp /= beta;                   // 1/B * ln(R/Ro)
  temp += 1.0 / (nominal_temeprature + 273.15); // + (1/To)
  temp = 1.0 / temp;                 // Invert
  temp -= 273.15;                         // convert absolute temp to C
  // Serial.print("Temperature ");
  // Serial.print(temp);
  // Serial.println(" *C");
  
  return temp;
}

double tempa::settemp()
{
  if(Serial.available() > 0)
  {
    String receivedString = Serial.readStringUntil('\n'); // Read the incoming string until newline
    receivedString.trim(); // Remove any leading or trailing whitespace (including CRLF)
    input = receivedString.toFloat(); // Convert the string to a float 
    heat = (input > preinput) ? true : false;
  }
  preinput = input ;
  return input;
}

int tempa::setdirection()
{
  if(heat == false && input < temp )
  { 
    currentMillis = millis();
    if(currentMillis - previousMillis > interval) 
    {
      pretemp = temp;
      previousMillis = currentMillis;   
      
    }
    Serial.println(pretemp);
    if(pretemp >= temp)
    {
      digitalWrite(_pina,LOW);
      digitalWrite(_pinb,HIGH);
      // Serial.println("cooling");
      return 1; 
    } else
    {
      // Serial.println("Shutdown");
      return 0;      
    }     
  }
  else
  {
    digitalWrite(_pina,HIGH);
    digitalWrite(_pinb,LOW);
    // Serial.println("heating");
    return 0;
  }
 
}
