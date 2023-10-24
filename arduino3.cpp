#define RELAY_PIN 7
char command;
//relay_config = 'NO';

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();
    if (command == '1') {
      digitalWrite(RELAY_PIN, HIGH);
      Serial.println(command);
    } else if (command == '0') {
      digitalWrite(RELAY_PIN, LOW);
      Serial.println(command);
    } else if (command == 'c') {
      if (digitalRead(RELAY_PIN) == HIGH) {
        Serial.println("1");
      } else {
        Serial.println("0");
      }
    }
    }
  }

