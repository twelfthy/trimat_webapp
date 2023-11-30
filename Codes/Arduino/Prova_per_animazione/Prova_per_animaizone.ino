int sensorValues[4] = {1000,200,3,800};
int sensorValues2[4] = {800,100,3,600};

void setup(){
  Serial.begin(9600);
  
}

void loop(){
  
  Serial.print(sensorValues[0]);
  Serial.print(",");
  Serial.print(sensorValues[1]);
  Serial.print(",");
  Serial.print(sensorValues[2]);
  Serial.print(",");
  Serial.print(sensorValues[3]);
  Serial.println();

  delay(100);

  Serial.print(sensorValues2[0]);
  Serial.print(",");
  Serial.print(sensorValues2[1]);
  Serial.print(",");
  Serial.print(sensorValues2[2]);
  Serial.print(",");
  Serial.print(sensorValues2[3]);
  Serial.println();
  
  delay(100);
  
}
