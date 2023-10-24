// 1 veya close inputu roleyi/anahtari kapatir, yani devreyi tamamlar, NO configinde enerji akisini mumkun kilar.
// 0 veya open inputu roleyi/anathari acar, yani devreyi keser, NO configinde enerji akisini durdurur.

const int RELAY_PIN = 7;
String command = "";
String relay_config = "NO";

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char serial_input = Serial.read();
    if (serial_input != '\n') {
      command += serial_input;
    } else {
      processCommand(command);
      command = "";
    }
  }
}

void processCommand(String cmd) {
  if (cmd == "1" || cmd == "closed") {
    closeRelay();
  } else if (cmd == "0" || cmd == "open") {
    openRelay();
  } else if (cmd == "c" || cmd == "check") {
    checkRelayStatus();
  } else if (cmd == "t" || cmd == "type") {
    printRelayType();
  } else {
    Serial.println("biyir?");
  }
}

void closeRelay() {
  digitalWrite(RELAY_PIN, HIGH);
  Serial.println(command);
}

void openRelay() {
  digitalWrite(RELAY_PIN, LOW);
  Serial.println(command);
}


void checkRelayStatus() {
  if (command == "c" ) {

  if (digitalRead(RELAY_PIN) == HIGH) {
    Serial.println("1");
  } else {
    Serial.println("0");
  }
  } else if (command == "check") {
      if (digitalRead(RELAY_PIN) == HIGH) {
    Serial.println("closed");
  } else {
    Serial.println("open");
  }
}
}

void printRelayType() {
  Serial.println(relay_config + " " + String(RELAY_PIN));
}
