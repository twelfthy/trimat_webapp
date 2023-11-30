#define s1 A0
#define s2 A1
#define s3 A2
#define s4 A3
#define s5 A4
#define s6 A5
#define s7 A6
#define s8 A7
#define s9 A8
#define s10 A9
#define s11 A10
#define s12 A11

int Matrix[12][12] = {{0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0}};
const int timeClock = 0;

void setup() {
  Serial.begin(9600);

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);
  
  pinMode(s1,INPUT);
  pinMode(s2,INPUT);
  pinMode(s3,INPUT);
  pinMode(s4,INPUT);
  pinMode(s5,INPUT);
  pinMode(s6,INPUT);
  pinMode(s7,INPUT);
  pinMode(s8,INPUT);
  pinMode(s9,INPUT);
  pinMode(s10,INPUT);
  pinMode(s11,INPUT);
  pinMode(s12,INPUT);

  delay(2000);
  
}

void printMatrix() {
  for ( int i = 0; i < 11; ++i ) {
//    Serial.print("Riga ");Serial.print(i+1);Serial.print("!      ");
      for ( int j = 0; j < 12; ++j ){
      Serial.print (Matrix[ i ][ j ] );
      Serial.print (",");
      }
      
      
//      Serial.println ();
   }
//   Serial.print("Riga 12");
      Serial.print(Matrix[11][0]);
      Serial.print (",");
      Serial.print(Matrix[11][1]);
      Serial.print (",");
      Serial.print(Matrix[11][2]);
      Serial.print (",");
      Serial.print(Matrix[11][3]);
      Serial.print (",");
      Serial.print(Matrix[11][4]);
      Serial.print (",");
      Serial.print(Matrix[11][5]);
      Serial.print (",");
      Serial.print(Matrix[11][6]);
      Serial.print (",");
      Serial.print(Matrix[11][7]);
      Serial.print (",");
      Serial.print(Matrix[11][8]);
      Serial.print (",");
      Serial.print(Matrix[11][9]);
      Serial.print (",");
      Serial.print(Matrix[11][10]);
      Serial.print (",");
      Serial.print(Matrix[11][11]);
}

void readRow(int x){

  digitalWrite(x+2, HIGH);
  
  Matrix[x][0] = analogRead(s1);
  Matrix[x][1] = analogRead(s2);
  Matrix[x][2] = analogRead(s3);
  Matrix[x][3] = analogRead(s4);
  Matrix[x][4] = analogRead(s5);
  Matrix[x][5] = analogRead(s6);
  Matrix[x][6] = analogRead(s7);
  Matrix[x][7] = analogRead(s8);
  Matrix[x][8] = analogRead(s9);
  Matrix[x][9] = analogRead(s10);
  Matrix[x][10] = analogRead(s11);
  Matrix[x][11] = analogRead(s12);
    digitalWrite(x+2, LOW);
  }

void loop() {

 for (int i = 0; i < 12; i++){

  readRow(i);

  delay(timeClock);
  
 }
 
printMatrix();
Serial.println();
 
}
