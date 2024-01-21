#include <nRF24L01.h>
#include <RF24.h>
#include <RF24_config.h> 
#include <Servo.h>
#include <SPI.h>
#include <NewPing.h>

#define trig_pin A1
#define echo_pin A2
int front_servo = 7;
const int DETECTION_THRESHOLD = 30;//cm for initial detection
const int ANGLES[] = {0, 180}; // Angles to check
const int NUM_ANGLES = 4;

int motor1pin1 = 2;
int motor1pin2 = 3;
int motor2pin1 = 4;
int motor2pin2 = 5;

#define servo1 6
#define CE_PIN 9
#define CSN_PIN 10

NewPing sonar(trig_pin, echo_pin, 200);

Servo frontServo;

char data[20]="";

RF24 radio(CE_PIN,CSN_PIN);
const uint64_t pipe = 0xE8E8F0F0E1LL;

float duration_us, distance_cm;
float maxDistance = 0;
int maxAngle = 0;
bool control = false;
int distance;

void setup() {
  // put your setup code here, to run once:
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
  
  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);

  Serial.begin(9600);

  frontServo.attach(front_servo);

  radio.begin();
  radio.openReadingPipe(0,pipe);
  radio.startListening();

  distance = readPing();
}

void loop() {
  // put your main code here, to run repeatedly:

  // First, check whether in front there is any fire or not
  // If yes, turn 180 degree and go back
  // ortherwise, keep go straight
  String msg="";
  if(Serial.available()){
    String data = Serial.readStringUntil('\n');
    if (data == "fire"){
      Serial.println("Received");
      moveStop();
      delay(500);
      turn180degree();
      moveStop();
      delay(500);
    }
//    else if(data == "not_fire"){
//      Serial.println("NAHHHHH");
//      moveStop();
//      delay(1000);
//    }
  }

  // check if there is any obstacle in the front
  // if there is, check surrounding and select the degree has the deepest space ============================================================================================================
  // if the control is not activate then autonomous driving then=======================================================================================================================================
  if(!control){
    if (distance < DETECTION_THRESHOLD) {
      
      moveStop();
  
      maxDistance = 0;
      maxAngle = 0;
      
      for (int i = 0; i < NUM_ANGLES; i++) {
        checkMaxDistanceAtAngle(ANGLES[i]);
      }
  
      // Move to the angle with the maximum distance
      frontServo.write(maxAngle);
      
      if (maxAngle == 0) {turnLeft90();moveStop();}
      else if(maxAngle == 180){turnRight90();moveStop();}
      
      frontServo.write(90);
  
      Serial.print("Max distance found at angle: ");
      Serial.println(maxAngle);
      
    }
    else{
      moveForward();
    }
  }

  
  distance = readPing();

  
  // Radio signal reading ============================================================================================================================================================================
  char msg1[4];
 
  if ( radio.available() )
  {
    Serial.println("reading radio");
    radio.read( msg1, 1 );
    Serial.println(*msg1);

  }
  if (strncmp(msg1, "rite", 4)){
    control = true;
  }
  else if(strncmp(msg1, "left", 4)){
    control = false;
  }


// if the control is activate ==================================================================================================================================
  if(control){
    if (msg1=="LEFT"){
      turnLeft();
    } 
    else if (msg1=="RIGHT"){
      turnRight();
    }
    else if (msg1=="FORWARD"){
      moveForward();
    }
    else if (msg1=="BACKWARD"){
     moveBackward();
    }
    else if(msg1=="STOP"){
      moveStop();
    }
  }


  delay(10);

}

// functions ===========================================================================================================================================================================================
void moveStop(){
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}


void moveForward(){


    digitalWrite(motor1pin1, HIGH);
    digitalWrite(motor2pin1, HIGH);
    digitalWrite(motor1pin2, LOW);
    digitalWrite(motor2pin2, LOW);
}


void moveBackward(){

  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin2, HIGH);
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor2pin1, LOW);
}


void turnRight(){

  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

}


void turnLeft(){

  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

}

//============================================================================================================================================================================================
void turnLeft90(){
  turnLeft();
  delay(500);
  moveStop();
}

void turnRight90(){
  turnRight();
  // for the 5v
  delay(500);
  moveStop();
}

void turn180degree(){
  turnRight();
  delay(1000);
  moveStop();
}
//===========================================================================================================================================================================================

void checkMaxDistanceAtAngle(int angle) {
  frontServo.write(angle);
  delay(1000); // Wait for servo to reach position

  float distance = readPing();
  Serial.print("Distance at angle ");
  Serial.print(angle);
  Serial.print(": ");
  Serial.println(distance);

  if (distance > maxDistance) {
    maxDistance = distance;
    maxAngle = angle;
  }
}

int readPing(){
  delay(70);
  int cm=sonar.ping_cm();
  if(cm == 0){
    cm = 250;
  }
  return cm;
}
