#define RELAY_PIN 7
char command;

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  Serial.begin(9600);
  //digitalWrite(RELAY_PIN, LOW);
  //Serial.println("0");
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();
    if (command == '1' || command == 'on') {
      digitalWrite(RELAY_PIN, HIGH);
      Serial.println("1");
    } else if (command == '0' || command == 'off') {
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("0");
    } else if (command == 'c') {
    if (digitalRead(RELAY_PIN) == HIGH) {
      Serial.println("1");
    } else {
      Serial.println("0");
    }
  }

  }
}
