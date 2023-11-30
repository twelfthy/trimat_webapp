float tempo_inizio=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
    tempo_inizio = millis();

    delay(1000);

    Serial.println(tempo_inizio);

}
