#include <nRF24L01.h>
#include <RF24.h>
#include <SPI.h>

#define CE_PIN 9
#define CSN_PIN 10

int up_btn = 2;
int down_btn = 4;
int left_btn = 5;
int right_btn = 3;
int start_btn = 6;
int select_btn = 7;
int analog_btn = 8;
int x_axis = A0;
int y_axis = A1;

int threshold_x = 512;
int threshold_y = 503;

int buttons[] = {up_btn, down_btn, left_btn, right_btn, start_btn, select_btn, analog_btn};

const uint64_t pipe = 0xE8E8F0F0E1LL;
RF24 radio(CE_PIN, CSN_PIN);
char msg[20] = "";

void setup() {
  // put your setup code here, to run once:
  for (int i; i< 7;i++){
    pinMode(buttons[i], INPUT);
    digitalWrite(buttons[i], HIGH);
  }
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(pipe);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(up_btn) == LOW){
    char msg[] = "up";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("UP btn Pressed");
  }
  if(digitalRead(down_btn) == LOW){
    char msg[] = "down";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("DOWN btn Pressed");
  }
  if(digitalRead(left_btn) == LOW){
    char msg[] = "left";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("LEFT btn Pressed");
  }
  if(digitalRead(right_btn) == LOW){
    char msg[] = "right";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("RIGHT btn Pressed");
  }
  if(digitalRead(select_btn) == LOW){
    char msg[] = "select";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("SELECT btn Pressed");
  }
  if(digitalRead(analog_btn) == LOW){
    char msg[] = "analogbut";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("ANALOG btn Pressed");
  }
  //Serial.print("\n X = "), Serial.print(analogRead(x_axis)), Serial.print("\n Y = "), Serial.print(analogRead(y_axis));
  //Serial.println(" ");

  if (analogRead(x_axis) < threshold_x-2){
    char msg[] = "FORWARD";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("FORWARD");
  }
  
  else if (analogRead(x_axis) > threshold_x+2){
    char msg[] = "BACKWARD";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("BACKWARD");
  }

  else if (analogRead(y_axis) < threshold_y-2){
    char msg[] = "LEFT";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("LEFT");
  }
  
  else if (analogRead(y_axis) > threshold_y+2){
    char msg[] = "RIGHT";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("RIGHT");
  }
  else{
    char msg[] = "STOP";
    radio.write(&msg, sizeof(msg));
    delay(300);
    Serial.println("STOP");
  }



  delay(500);
  Serial.flush();
}
