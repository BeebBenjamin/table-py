//import the adafruit motor shield library
#include <AFMotor.h>

//define incomingByte to be used to store a character read from serial port
char incomingByte;

//define the total number of steps for the 5v stepper
double total_steps_1 = 2048; //5v stepper

//define the total number of steps for the 2v stepper
double total_steps_2 = 200;  //12v stepper
 
//define motor port in use
int motor_port_2 = 2;

//define the angle of stepping for the 5v stepper
double angle_1 = 10;

//define the angle of stepping for the 12v stepper
double angle_2 = 10.8;

//define variable to contain number of steps
double number_of_steps = 0; 

//initiate stepper motor conntected to port 2
AF_Stepper stepper_motor_2(total_steps, motor_port_2);

void setup()
{
  //set stepper speed to 5rpm
  stepper_motor_2.setSpeed(5);
 //open serial port connection with a baud rate of 9600 
 Serial.begin(9600);
}
 
void loop()
{
 //select character encoding utf-8
  uint8_t i;

  //if the serial connection works read continuously for incoming characters
  if (Serial.available() > 0) 
  {
    incomingByte = Serial.read();
  }
  else
  {
    //if the incoming character is equal to 1 then step the stepper motor by 10 degrees
    if(incomingByte =='1')
    {
      number_of_steps = angle_1 / (360 / total_steps_1);
      stepper_motor_2.step(number_of_steps, FORWARD,DOUBLE);
      //write a 'D' to the serial port for Python wrapper to read
      Serial.write('D');
      
      //set incomingByte to D to set machine to a 'done' state
      incomingByte ='D';
    }
    //if the incoming character is equal to 1 then step the stepper motor by 10.8 degrees
    if(incomingByte =='2')
    {
      number_of_steps = angle_2 / (360 / total_steps_2);
      stepper_motor_2.step(number_of_steps, FORWARD,DOUBLE);
      //write a 'D' to the serial port for Python wrapper to read
      Serial.write('D');
      
       //set incomingByte to D to set machine to a 'done' state
      incomingByte ='D';
    }
    //if the incoming character is equal to 'N' then turn off the stepper motor and release it
    if(incomingByte =='N')
    {
      stepper_motor_2.release();
    }
  }
}
