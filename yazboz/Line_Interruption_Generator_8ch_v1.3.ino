const int numChannels = 8;
uint8_t relayPins[numChannels] = { 2, 3, 4, 5, 6, 7, 8, 9 };
bool relayStates[numChannels] = { HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH };
unsigned long minDelay = 1;
unsigned long maxDelay = 30000;

unsigned long randomiseDelay;


void updateRelayStates(int start, int end, bool state) {
  for (int i = start; i <= end; ++i) {
    relayStates[i] = state;
    digitalWrite(relayPins[i], relayStates[i]);
  }
}

void setup() {

  for (int i = 0; i < numChannels; ++i) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], relayStates[i]);
  }

  Serial.begin(9600);
  randomSeed(analogRead(0));

  Serial.println("\n\n\n\nBasliyor");
}

void controlRelays(bool relayState, unsigned long maxDelay, int groupStart, int groupEnd) {
  //Serial.println(String(stateDelay / 1000) + " saniye " + (relayState ? "ON" : "OFF") + " bekleyecegiz.");

  updateRelayStates(groupStart, groupEnd, relayState);
  delay(maxDelay);
}

void loop() {
  randomiseDelay = random(minDelay, maxDelay);
  Serial.println(String(randomiseDelay / 1000) + " saniye bagli duracak");
  controlRelays(LOW, randomiseDelay, 0, 7);

  randomiseDelay = random(minDelay, maxDelay);
  Serial.println(String(randomiseDelay / 1000) + " saniye kopuk kalacak");
  controlRelays(HIGH, randomiseDelay, 0, 7);
}
