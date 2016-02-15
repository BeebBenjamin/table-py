#include <AFMotor.h>

char incomingByte;

double total_steps_1 = 2048; //5v stepper

double total_steps_2 = 200;  //12v stepper
 
int motor_port_2 = 2;

double angle_1 = 10;

double angle_2 = 10.8;
 
double number_of_steps = 0; 
  
AF_Stepper stepper_motor_2(total_steps, motor_port_2);
 
void setup()
{
  stepper_motor_2.setSpeed(5);
  Serial.begin(9600);
}
 
void loop()
{
  uint8_t i;

  if (Serial.available() > 0) 
  {
    incomingByte = Serial.read();
  }
  else
  {
    if(incomingByte =='1')
    {
      number_of_steps = angle_1 / (360 / total_steps_1);
      
      stepper_motor_2.step(number_of_steps, FORWARD,DOUBLE);

      Serial.write('D');
      
      incomingByte ='D';
    }    
    if(incomingByte =='2')
    {
      number_of_steps = angle_2 / (360 / total_steps_2);
      
      stepper_motor_2.step(number_of_steps, FORWARD,DOUBLE);

      Serial.write('D');
      
      incomingByte ='D';
    }
    if(incomingByte =='N')
    {
      stepper_motor_2.release();
    }
  }
}
