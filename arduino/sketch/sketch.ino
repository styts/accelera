#include<stdlib.h>

const int xpin = A0;                  // x-axis of the accelerometer
const int ypin = A1;                  // y-axis
const int zpin = A2;                  // z-axis (only on 3-axis models)
String line = "";
char buff[20];

void setup()
{
  Serial.begin(9600);
}


void old(){
  Serial.print(analogRead(xpin));
  // print a tab between values:
  Serial.print("\t");
  Serial.print(analogRead(ypin));
  // print a tab between values:
  Serial.print("\t");
  Serial.print(analogRead(zpin));
  Serial.print("\n");
  // delay before next reading:
  delay(1);
}

int analog_x,analog_y,analog_z;
float vol_x,vol_y,vol_z;
float add_x,add_y,add_z;
float g_x,g_y,g_z;
float degree_x,degree_y,degree_z;

void wiki(){
 analog_x=analogRead(0);
 analog_y=analogRead(1);
 analog_z=analogRead(2);
  vol_x=analog_x*5.0/1024;//convert analog_x-->voltage value(v)
  vol_y=analog_y*5.0/1024;
  vol_z=analog_z*5.0/1024;
 //range x: 0.83 - 2.41    1.62
 //      y: 0.96 - 2.53    1.74
 //      z: 0.72 - 2.23    1.48
  add_x=vol_x-1.62;//calculate the added x axis voltage value
  add_y=vol_y-1.74;
  add_z=vol_z-1.48;
  g_x=add_x/0.8;//calculate the gram value
  g_y=add_y/0.8;
  g_z=add_z/0.8;

  if(g_x<=1&&g_x>=-1) //We use this condition to prevent the overflow of asin(x).( If x>1 or x<-1, asin(x)=0)
  {
  degree_x=asin(g_x)*180.0/PI;//calculate the degree value
  degree_y=asin(g_y)*180.0/PI;
  degree_z=asin(g_z)*180.0/PI;
  }
  //fix the overflow condition
  if(g_x>1)
  degree_x=90;
  if(g_x<-1)
  degree_x=-90;
  if(g_y>1)
  degree_y=90;
  if(g_y<-1)
  degree_y=-90;
  if(g_z>1)
  degree_z=90;
  if(g_z<-1)
  degree_z=-90;
 //#########################
 //print
 line = "";
// line = line + String.valueOf(degree_x);
 line = line + dtostrf(degree_x, 2, 2, buff);
 line = line + "\t";
 
 line = line + dtostrf(degree_y, 2, 2, buff);
 line = line + "\t";
 line = line + dtostrf(degree_z, 2, 2, buff);
 Serial.println(line);
 delay(10);
}

void loop()
{
  wiki();

}
