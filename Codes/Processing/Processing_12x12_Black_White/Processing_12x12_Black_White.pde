import processing.serial.*;

Serial myPort; // The serial port
int maxNumberOfSensors = 144; //CAMBIARE
float[] sensorValue = new float[maxNumberOfSensors]; // global variable for storing mapped sensor values
float[] previousValue = new float[maxNumberOfSensors]; // array of previous values
int rectSize = 60;
int x = 0;
int y = 0;
int step = 60;
int k;



void setup () {
  size(800, 800); // set up the window to whatever size you want
  println(Serial.list()); // List all the available serial ports
  String portName = Serial.list()[0];
  myPort = new Serial(this, "/dev/cu.usbserial-14410", 9600);
  myPort.clear();
  myPort.bufferUntil('\n'); // don’t generate a serialEvent() until you get a newline (\n) byte
  background(250); // set inital background
  smooth(); // turn on antialiasing
  rectMode(CORNER);
}

void draw () {
  x = 0;
  y = 0;
   k = 0;
  for (int i = 0; i < 12; i++){
    x = 0;
    for (int j = 0; j < 12; j++){
      fill(sensorValue[k]);
      rect(0+x, 0+y, rectSize, rectSize); //top left
      x = x + step;
      k++;
    }
    y = y + step;
  }
  
  //AGGIUNGERE e anche CAMBIARE /2 in /quello che serve
}

void serialEvent (Serial myPort) {
String inString = myPort.readStringUntil('\n'); // get the ASCII string

  if (inString != null) { // if it’s not empty
    inString = trim(inString); // trim off any whitespace
    int incomingValues[] = int(split(inString, ",")); // convert to an array of ints

    if (incomingValues.length <= maxNumberOfSensors && incomingValues.length > 0) {
      for (int i = 0; i < incomingValues.length; i++) {
        // map the incoming values (0 to 1023) to an appropriate gray-scale range (0-255):
        sensorValue[i] = map(incomingValues[i], 0, 60, 0, 255);
        if (sensorValue[i] < 30) sensorValue[i] = 0;
      }
    }
  }
  
}
