const int numChannels = 8;
uint8_t relayPins[numChannels] = { 2, 3, 4, 5, 6, 7, 8, 9 };
bool relayStates[numChannels] = { HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH };
unsigned long stateDuration = 60000;

// void defineVaV() {
  // relayPins[0] = 2;
  // relayPins[1] = 3;
  // relayPins[2] = 4;
  // relayPins[3] = 5;
  // relayPins[4] = 6;
  // relayPins[5] = 7;
  // relayPins[6] = 8;
  // relayPins[7] = 9;

  // relayStates[0] = HIGH;
  // relayStates[1] = HIGH;
  // relayStates[2] = HIGH;
  // relayStates[3] = HIGH;
  // relayStates[4] = HIGH;
  // relayStates[5] = HIGH;
  // relayStates[6] = HIGH;
  // relayStates[7] = HIGH;
// }

void updateRelayStates(int start, int end, bool state) {
  for (int i = start; i <= end; ++i) {
    relayStates[i] = state;
    digitalWrite(relayPins[i], relayStates[i]);
  }
}

void setup() {
  // defineVaV();

  for (int i = 0; i < numChannels; ++i) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], relayStates[i]);
  }

  Serial.begin(9600);
  randomSeed(analogRead(0));

  Serial.println("\n\n\n\nBasliyor");
}

void controlRelays(bool relayState, unsigned long stateDelay, int groupStart, int groupEnd) {
  //Serial.println(String(stateDelay / 1000) + " saniye " + (relayState ? "ON" : "OFF") + " bekleyecegiz.");

  updateRelayStates(groupStart, groupEnd, relayState);
  delay(stateDelay);
}

void loop() {
  Serial.println("internet var");
  controlRelays(LOW, stateDuration, 0, 7);

  Serial.println("internet yok");
  controlRelays(HIGH, stateDuration, 0, 7);
}
