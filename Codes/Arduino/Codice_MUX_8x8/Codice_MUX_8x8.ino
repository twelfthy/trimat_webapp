
/* TEST BOARD FIRMWARE FOR ARDUINO AND THE ADG732BSUZ 32 CHANNEL MULTIPLEXER
 *  BOARD CALLED "MegaMUX"
 *  
 *  CONNECTION INSTRUCTIONS BELOW.
 *  This will connect 32 outputs to one pin on the arduino
 *  
 *  Created by Sean Hodgins 
 *  Watch the Video Tutorial on Youtube - http://youtube.com/seanhodginsfilms
 *  Support my Open Source Projects on Patreon! - https://patreon.com/seanhodgins
 *  
 *  This software is licences under cc-by-sa-nc-3.0
 */


// dev/cu.usbserial-14310

const int SPin[4] = {14, 15, 16, 17}; // 4 Pin usati per inviare il codice binario
const int EPin = 18; /* Pin Enable
                      - se impostato HIGH interrotto fisicamente il collegamento tra il pin SIG e quello Yxx scelto
                      - se impostato LOW viene stabilito il collegamento tra il pin SIG e quello Yxx scelto */

const int SIG = 19; // SIG pin

const int STable[16][4] = {
  // Crea un Array con i valori binari da richiamare in base al canale Y scelto
  // s0, s1, s2, s3, canale
  {0,  0,  0,  0}, // Y0
  {1,  0,  0,  0}, // Y1
  {0,  1,  0,  0}, // Y2
  {1,  1,  0,  0}, // Y3
  {0,  0,  1,  0}, // Y4
  {1,  0,  1,  0}, // Y5
  {0,  1,  1,  0}, // Y6
  {1,  1,  1,  0}, // Y7
  {0,  0,  0,  1}, // Y8
  {1,  0,  0,  1}, // Y9
  {0,  1,  0,  1}, // Y10
  {1,  1,  0,  1}, // Y11
  {0,  0,  1,  1}, // Y12
  {1,  0,  1,  1}, // Y13
  {0,  1,  1,  1}, // Y14
  {1,  1,  1,  1}  // Y15
};


int Matrix[8][8] = {{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0}};
const int timeClock = 0;

int S[5] = {13, 12, 11, 10, 9}; //A0, A1, A2, A3, A4 Respectively

int CS = 8;   // To change between different muxes
int WR = 7;   // To lock changes
int EN = 6;   // To enable/disable

int C[8] = {52, 50, 48, 46, 44, 42, 40, 38};

int INPIN = A0; //IO on MegaMUX

void setup() {
  // put your setup code here, to run once:
  for (int x = 0; x < 5; x++) {
    pinMode(S[x], OUTPUT);
    digitalWrite(S[x], LOW);
  }
  for (int x = 0; x < 8; x++) {
    pinMode(C[x], OUTPUT);
    digitalWrite(C[x], LOW);
  }
  pinMode(CS, OUTPUT);
  digitalWrite(CS, LOW);
  pinMode(WR, OUTPUT);
  digitalWrite(WR, LOW);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
  pinMode(INPIN, OUTPUT);
  digitalWrite(INPIN, LOW);
  Serial.begin(9600);

  //16MUX:
  pinMode(EPin, OUTPUT);// Inizializza EPin come OUTPUT
  digitalWrite(EPin, LOW); // presetta EPin LOW, leggere la nota all'inizio del programma per i dettagli
  
  pinMode(SIG, OUTPUT); // Inizializza SIG come OUTPUT
  digitalWrite(SIG, HIGH); // Presetta SIG HIGH, serve per il nostro esperimeto poi andrà settato a seconda delle necessità

  for (int i = 0; i < 4; i++)
  {
    pinMode(SPin[i], OUTPUT); // Inizializza tutti gli Spin come OUTPUT
    digitalWrite(SPin[i], LOW); // Setta tutti gli Spin LOW
  }
}

//void pinSelectSR(int x){
//  for (int i = 0; i<8; i++){
//    if (i == x){
//      digitalWrite(C[i], HIGH);
//    }
//    else digitalWrite(C[i], LOW);
//  }
//}

void YSelect(int Y){
  digitalWrite(SPin[0], STable[Y][0]);
  digitalWrite(SPin[1], STable[Y][1]);
  digitalWrite(SPin[2], STable[Y][2]);
  digitalWrite(SPin[3], STable[Y][3]);
}

void Read(int x, int y){
  if (analogRead(A0) <= 10) Matrix[x][y] = 0;
  else Matrix[x][y] = analogRead(A0);
  }

void Print_Matrix(){
  for (int i = 0; i<8; i++){
    for (int j = 7; j>=0; j--){
      Serial.print(Matrix[i][j]);
      if (j == 0&&i==7) break;
//      if (i == 7 && j == 0) break;
      else Serial.print(",");
    }
//    Serial.print(";");
//    Serial.println();   //Per lettura sul serial monitor
  }
  Serial.println();
}

void loop() {
  for (int x = 0; x<8; x++){
//    pinSelectSR(x);
    YSelect(x);
    for(int y = 0; y<8; y++){
    pinSelectMux(y);
    Read(x, y);
//    Serial.print(analogRead(A0));
    }
  }
  Print_Matrix();

  delay(timeClock);
  
}

void pinSelectMux(int pinnum){
  digitalWrite(WR, LOW);
    for (int x = 0; x<5; x++){
      byte state = bitRead(pinnum, x);
      digitalWrite(S[x], state);
//      Serial.print(state);
    }
//    Serial.println();
  digitalWrite(WR, HIGH);
}
