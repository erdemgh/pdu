// 1 veya close inputu roleyi/anahtari kapatir, yani devreyi tamamlar, NO configinde enerji akisini mumkun kilar.
// 0 veya open inputu roleyi/anathari acar, yani devreyi keser, NO configinde enerji akisini durdurur.

#define RELAY_PIN 7
String relay_config = "NO";

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.toLowerCase();
    command.trim();

    if (command == "1" || command == "closed") {
      closeRelay(command);
    } else if (command == "0" || command == "open") {
      openRelay(command);
    } else if (command == "c" || command == "check") {
      checkRelayStatus(command);
    } else if (command == "t" || command == "type") {
      printRelayType();
    } else {
      Serial.println("Biyir?");
    }
  }
}

void closeRelay(String command) {
  digitalWrite(RELAY_PIN, HIGH);
  Serial.println(command);
}

void openRelay(String command) {
  digitalWrite(RELAY_PIN, LOW);
  Serial.println(command);
}

void checkRelayStatus(String command) {
  if (digitalRead(RELAY_PIN) == HIGH) {
    if (command == "c") {
      Serial.println("1");
    } else {
      Serial.println("closed");
    }
  } else {
    if (command == "c") {
      Serial.println("0");
    } else {
      Serial.println("open");
    }
  }
}


void printRelayType() {
  Serial.println("NO " + String(RELAY_PIN));
}
