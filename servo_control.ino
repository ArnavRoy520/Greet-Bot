#include<Servo.h>

// SERVO INIT
Servo yawServo;
Servo pitchServo;
float yaw_setpt = 100;
float pitch_setpt = 110;
int yaw_error;
int pitch_error;
float vel = 2.5;

const byte dir1 = 24;   // Connect DIR1 of motor driver to pin 13
const byte dir2 =25;   // Connect DIR2 of motor driver to pin 12
const byte pwm1 = 3;   // Connect PWM1 of motor driver to pin 11
const byte pwm2 = 2;   // Connect PWM2 of motor driver to pin 10



//LEFT GROUND IS CONNECTED TO GND PIN OF ARDUINO
int followLine = 0;

// WHEELS INIT





void setup() {
  // SERVO
  yawServo.attach(12);
  pitchServo.attach(15);
  yawServo.write(int(yaw_setpt));
  pitchServo.write(int(pitch_setpt));

  // IR SENSOR
   for(byte i=4;i<=11;i++) {
    pinMode(i,INPUT);
  }

  pinMode(24,OUTPUT);
  pinMode(25,OUTPUT);
  pinMode(pwm1,OUTPUT);
  pinMode(pwm2,OUTPUT);

    // Setting the initial condition of motors
  // make sure both PWM pins are LOW
  digitalWrite(pwm1,LOW);
  digitalWrite(pwm2,LOW);
  
  delay(500);
  Serial.begin(9600);

}

void getError()
{
   yaw_error = 0;
   pitch_error = 0;
   //followLine = 0;
   if(Serial.available()!=0)
  {
    yaw_error = Serial.readStringUntil('#').toInt();
    pitch_error = Serial.readStringUntil('$').toInt();
    followLine = Serial.readStringUntil('@').toInt();
  }

}



void moveRightServo()
{
    yaw_setpt = yaw_setpt - vel;
    yawServo.write(int(yaw_setpt));
}



void moveLeftServo()
{
    yaw_setpt = yaw_setpt + vel;
    yawServo.write(int(yaw_setpt));
}




void moveUpServo()
{
    pitch_setpt = pitch_setpt + vel;
    pitchServo.write(int(pitch_setpt));
}



void moveDownServo()
{
    pitch_setpt = pitch_setpt - vel;
    pitchServo.write(int(pitch_setpt));
}




void lineFollower()
{
    if(digitalRead(6) && digitalRead(9))
  moveForward();
  
  
  // Checking for sensor number 1 and 2, if line detected, move left
  else if(digitalRead(5) || digitalRead(6))
  moveLeft();

  // Checking for sensor number 5 and 6, if line detected, move right
  else if(digitalRead(9) || digitalRead(10))
  moveRight();

  // Checking for sensors number 3 and 4, 
  // if line is detected by either of these sensor, move forward
  else if(digitalRead(7) || digitalRead(8))
  moveForward();

  // If no line is detected, stay at the position
  else
  wait();

  // Put some delay to avoid the robot jig while making a turn
  delay(100);
}

// The values work good in my case, you could use other values set
// to archieve a performance that satisfy you
void moveLeft() {
  // For robot to move left, right motor has to be faster than left motor]
  digitalWrite(dir1,HIGH);
  digitalWrite(dir2,HIGH);
  analogWrite(pwm2,95);
  analogWrite(pwm1,25);
}

void moveRight() {
  // For robot to move right, left motor has to be faster than right motor
  digitalWrite(dir1,HIGH);
  digitalWrite(dir2,HIGH);
  analogWrite(pwm2,19);
  analogWrite(pwm1,100);
}

void moveForward() {
  // For robot to move forward, both motors have to be same speed
  digitalWrite(dir1,HIGH);
  digitalWrite(dir2,HIGH);
  analogWrite(pwm1,90);
  analogWrite(pwm2,90);
}

void wait() {
  // Function to makes the robot stay
  digitalWrite(dir1,HIGH);
  digitalWrite(dir2,HIGH);
  analogWrite(pwm1,0);
  analogWrite(pwm2,0);
}



void loop() {
   getError();
   if(yaw_error == 1000)
   {
       yaw_setpt = 100;
       yawServo.write(yaw_setpt);
   }

   else if(yaw_error<0)
   {
      moveRightServo();
      //delay(10);
   }


   else if(yaw_error>0)
   {
      moveLeftServo();
      //delay(10);
   }

   if(pitch_error == 1000)
   {
       pitch_setpt = 110;
       pitchServo.write(pitch_setpt);
   }

  else if(pitch_error<0)
   {
     moveUpServo();
      //delay(10);
   }


   else if(pitch_error>0)
   {
     moveDownServo();
      //delay(10);
   }

  if(followLine==1)
  {
    lineFollower();
  }

  else
  {
    wait();
  }

//Serial.println(followLine);
}