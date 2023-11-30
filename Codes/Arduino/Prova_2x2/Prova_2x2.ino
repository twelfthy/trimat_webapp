#define s1 A0
#define s2 A1
//#define s3 A2
//#define s4 A3
int Matrix[2][2] = {{0,0},{0,0}};
const int timeClock = 50;

void setup() {
  Serial.begin(9600);

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);

  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  
  pinMode(s1,INPUT);
  pinMode(s2,INPUT);
//  pinMode(s3,INPUT);
//  pinMode(s4,INPUT);
  
}

void printMatrix() {
  for ( int i = 0; i < 2; ++i ) {
      for ( int j = 0; j < 2; ++j ){
      Serial.print (Matrix[ i ][ j ] );
      Serial.print (",");
      }
      
   }
   Serial.println ();
}

void loop() {

  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  Matrix[0][0] = analogRead(s1);
  Matrix[0][1] = analogRead(s2);

  delay(10);
  
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  Matrix[1][0] = analogRead(s1);
  Matrix[1][1] = analogRead(s2);
//  Serial.print(Matrix[0][0]);
//  Serial.print(",");
//  Serial.print(Matrix[0][1]);

//// %%%%%%%%%%%%%%%%%%%%%%%%%  For printing matrix on arduino Serial monitor
//  Serial.println("Matrix: ");
//  printMatrix();
//
//// %%%%%%%%%%%%%%%%%%%%%%%%%  For sending to processing program
  Serial.print(Matrix[0][0]);
  Serial.print(",");
  Serial.print(Matrix[0][1]);
  Serial.print(",");
  Serial.print(Matrix[1][0]);
  Serial.print(",");
  Serial.println(Matrix[1][1]);
//
//// %%%%%%%%%%%%%%%%%%%%%%%%%  For sending to pyton program
//  Serial.print(Matrix[0][0]);
//  Serial.print("-");
//  Serial.print(Matrix[0][1]);
//  Serial.print("-");
//  Serial.print(Matrix[1][0]);
//  Serial.print("-");
//  Serial.println(Matrix[1][1]);
  

  delay(timeClock);
  
}
