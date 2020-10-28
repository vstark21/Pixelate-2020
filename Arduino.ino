#include<SoftwareSerial.h>
#include<Servo.h>
SoftwareSerial mySer(9, 10);
int a;
char b;
int In1=7;
int In2=8; 
int In3=12;
int In4=13;
int ENA=5;
int ENB=6;
int SPED = 70;
int SPED1 = 70;
int sensor;
int green = 0;
int red = 1;
int blue = 2;
int i;
int servoPin = 3;
Servo Servo1;

void setup() {
  Serial.begin(9600);
  pinMode(1, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  Servo1.attach(servoPin);
  Servo1.write(40);
  mySer.begin(9600);
}

void loop(){
  if(1){
    a=mySer.read();
    
    if(a=='F')
    forward();
    if(a=='B')
    backward();
    if(a=='L')
    left();
    if(a=='R')
    right();
    if(a=='s')
    Stop();
    if(a=='D')
    servoDown();
    if(a=='U')
    servoUp();
    if(a=='r')
    Red();
    if(a=='b')
    Blue();
    if(a=='g')
    Green();
    if(a == 'x'){
      cut();
    }
    
  }
}


  void forward()
  {
     digitalWrite(In1,HIGH);
     digitalWrite(In2,LOW);
     analogWrite(ENA,SPED);

     digitalWrite(In3,HIGH);
     digitalWrite(In4,LOW);
     analogWrite(ENB,SPED1);
  }
void backward()
  {  digitalWrite(In1,LOW);
  digitalWrite(In2,HIGH);
  analogWrite(ENA,SPED);

 digitalWrite(In3,LOW);
  digitalWrite(In4,HIGH);
  analogWrite(ENB,SPED1); }
  
  
  void left()
{  digitalWrite(In1,HIGH);
  digitalWrite(In2,LOW);
  analogWrite(ENA,SPED+10);
  digitalWrite(In3,LOW);
  digitalWrite(In4,HIGH);
  analogWrite(ENB,SPED1+10);

}


void right()
{  
  digitalWrite(In3,HIGH);
  digitalWrite(In4,LOW);
  analogWrite(ENB,SPED1+10);
  digitalWrite(In1,LOW);
  digitalWrite(In2,HIGH);
  analogWrite(ENA,SPED+10);
 }

 void Stop()
 {  digitalWrite(In1,LOW);
    digitalWrite(In2,LOW);
    digitalWrite(In3,LOW);
    digitalWrite(In4,LOW);
    analogWrite(ENA,0);
    analogWrite(ENB,0);
  
  }
 void servoDown()
 {
  Servo1.write(90);
 }
 void servoUp()
  {
    Servo1.write(40);
  }
  void Red()
  {
    digitalWrite(red, HIGH);
    delay(2000);
    digitalWrite(red, LOW);
  }
  void Blue()
  {
    digitalWrite(blue, HIGH);
    
  }
  void cut(){
    digitalWrite(blue, LOW);
  }
  void Green()
  {
    digitalWrite(green, HIGH);
    delay(2000);
    digitalWrite(green, LOW);
  }
