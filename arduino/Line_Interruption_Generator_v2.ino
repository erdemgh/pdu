// bool olabilecek degiskenler uzerine calisilmadi
// relayState uzerine dusunulmedi
// bombos bir boarda atilinca kod, ne oluyor bakilmadi
// relay pin adresi dogru buyuklukte mi emin degilim

#include <EEPROM.h>

#define ADDR_CONFIG_LOCATION 0
#define ADDR_RELAY_PIN 1
#define ADDR_RELAY_MODE 2
#define ADDR_TIMER_MODE 3
#define ADDR_DD_MIN 4
#define ADDR_DD_MAX 12
#define ADDR_CD_MIN 20
#define ADDR_CD_MAX 28


char config_location;
uint8_t relay_pin;
char relay_mode;
char timer_mode;
int relayState = LOW;
unsigned long ddmin;
unsigned long ddmax;
unsigned long cdmin;
unsigned long cdmax;
unsigned long ddcur;
unsigned long cdcur;
unsigned long previousMillis = 0;



void printUsageToSerial() {
  Serial.println("\nStarting\n");
  delay(1000);
  Serial.println("Commands:");
  Serial.println("gcl: \t\tget settings location");
  Serial.println("grp: \t\tget relay pin");
  Serial.println("grm: \t\tget relay mode");
  Serial.println("gtm: \t\tget timer mode");
  Serial.println("gcd: \t\tget connection durations");
  Serial.println("gdd: \t\tget disconnection durations");

  Serial.println("scl arg: \tset settings location. 0:ram, 1:eeprom");
  Serial.println("srp arg: \tset relay pin from. range:2-13");
  Serial.println("srm arg: \tset relay mode. 0:NO(Normally Open), 1:NC(Normally Closed)");
  Serial.println("stm arg: \tset timer mode. 0:timer off, 1:timer on");
  Serial.println("scd arg1 arg2: \tset connection duration, arg1:cdmin, arg2:cdmax");
  Serial.println("sdd arg1 arg2: \tset disconnection, arg1:ddmin, arg2:ddmax");

  Serial.println("rst: \t\trestart arduino");
  Serial.println("\n");
  delay(1000);
}


void defineVarVals() {
  config_location = EEPROM.read(ADDR_CONFIG_LOCATION);
  if (config_location != '1') {
    relay_pin = 7;
    relay_mode = '7';
    timer_mode = '7';
    ddmin = 7;
    ddmax = 7;
    cdmin = 7;
    cdmax = 7;
    Serial.println("\ntemporary setting allowed\n");
  } else {
    config_location = EEPROM.read(ADDR_CONFIG_LOCATION);
    relay_pin = EEPROM.read(ADDR_RELAY_PIN);
    relay_mode = EEPROM.read(ADDR_RELAY_MODE);
    timer_mode = EEPROM.read(ADDR_TIMER_MODE);
    EEPROM.get(ADDR_DD_MIN, ddmin);
    EEPROM.get(ADDR_DD_MAX, ddmax);
    EEPROM.get(ADDR_CD_MIN, cdmin);
    EEPROM.get(ADDR_CD_MAX, cdmax);
    Serial.println("\npermanent setting allowed\n");
  }
}


int splitCommand(String command, char separator, String parts[], int maxParts) {
  int partCount = 0;
  int partIndex = 0;
  int lastIndex = -1;
  for (int i = 0; i < command.length(); i++) {
    if (command.charAt(i) == separator) {
      if (partIndex < maxParts) {
        parts[partIndex] = command.substring(lastIndex + 1, i);
        partIndex++;
      }
      lastIndex = i;
      partCount++;
    }
  }
  if (lastIndex < command.length() - 1 && partIndex < maxParts) {
    parts[partIndex] = command.substring(lastIndex + 1, command.length());
    partCount++;
  }
  return partCount;
}

void setup() {
  //EEPROM.get(ADDR_RELAY_PIN, relay_pin);
  defineVarVals();
  pinMode(relay_pin, OUTPUT);
  Serial.begin(9600);
  printUsageToSerial();
  randomSeed(analogRead(0));
  setInitialDisconnectionDuration();

  Serial.println("Relay will be open for " + String(ddcur / 1000) + " seconds.");
  Serial.println("cdmin: " + String(cdmin) + "\t cdmax : " + String(cdmax) + "\t cdcur: " + String(cdcur / 1000));
  Serial.println("ddmin: " + String(ddmin) + "\t ddmax : " + String(ddmax) + "\t ddcur: " + String(ddcur / 1000));
  Serial.println("rm: " + String(relay_mode) + "\t\t rp : " + String(relay_pin) + "\t\t cl: " + String(config_location) + "\t\t tm: " + String(timer_mode));
}


void save_cdmin_cdmax(unsigned long cdmin, unsigned long cdmax) {
  if (config_location == '1') {
    EEPROM.put(ADDR_CD_MIN, cdmin);
    EEPROM.put(ADDR_CD_MAX, cdmax);
    Serial.println("cdmin, cdmax saved to EEPROM!");
  } else {
    Serial.println("cdmin, cdmax saved to RAM!");
  }
}


void save_ddmin_ddmax(unsigned long ddmin, unsigned long ddmax) {
  if (config_location == '1') {
    EEPROM.put(ADDR_DD_MIN, ddmin);
    EEPROM.put(ADDR_DD_MAX, ddmax);
    Serial.println("ddmin, ddmax saved to EEPROM!");
  } else {
    Serial.println("ddmin, ddmax saved to RAM!");
  }
}


void save_cl(char config_location) {
  EEPROM.put(ADDR_CONFIG_LOCATION, config_location);
  Serial.println("config_location settings saved to EEPROM!");
}

void update_cl(char new_cl) {
  config_location = new_cl;
  Serial.println("set OK!");
  Serial.println("cl: " + config_location);
}


void save_rm(char relay_mode) {
  if (config_location == '1') {
    EEPROM.put(ADDR_RELAY_MODE, relay_mode);
    Serial.println("relay_mode settings saved to EEPROM!");
  }
}

void update_rm(uint8_t new_rm) {
  relay_mode = new_rm;
  Serial.println("set OK!");
  Serial.println("rm: " + relay_mode);
}

void save_rp(uint8_t relay_pin) {
  if (config_location == '1') {
    EEPROM.put(ADDR_RELAY_PIN, relay_pin);
    Serial.println("relay_pin saved to EEPROM!");
  }
}

void update_rp(uint8_t new_rp) {
  relay_pin = new_rp;
  Serial.println("set OK!");
  Serial.println("rp: " + String(relay_pin));
}

void save_tm(char timer_mode) {
  if (config_location == '1') {
    EEPROM.put(ADDR_TIMER_MODE, timer_mode);
    Serial.println("timer_mode settings saved to EEPROM!");
  }
}

void update_tm(char char_tm) {
  timer_mode = char_tm;
  Serial.println("set OK!");
  if (timer_mode == '1') {
    Serial.println("timer_mode:1(on)");
    Serial.println("tm: " + timer_mode);
  } else {
    Serial.println("timer_mode:0(off)");
    Serial.println("tm: " + timer_mode);
  }
}


void updateDisconnectionDuration(unsigned long new_ddmin, unsigned long new_ddmax) {
  ddmin = new_ddmin;
  ddmax = new_ddmax;
  ddcur = random(ddmin * 1000, ddmax * 1000 + 1);
  previousMillis = millis();
  relayState = LOW;
  digitalWrite(relay_pin, relayState);
}

void updateConnectionDuration(unsigned long new_cdmin, unsigned long new_cdmax) {
  cdmin = new_cdmin;
  cdmax = new_cdmax;
  cdcur = random(cdmin * 1000, cdmax * 1000 + 1);
  previousMillis = millis();
  relayState = HIGH;
  digitalWrite(relay_pin, relayState);
}

void setInitialDisconnectionDuration() {
  ddcur = random(ddmin * 1000, ddmax * 1000 + 1);
  previousMillis = millis();
  relayState = LOW;
  digitalWrite(relay_pin, relayState);
}


void processSerialCommands() {
  while (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.length() == 0) {
      Serial.println("\n");
      continue;
    }

    if (command.startsWith("sdd")) {
      String parts[3];
      int partCount = splitCommand(command, ' ', parts, 3);

      if (partCount == 3) {
        unsigned long new_ddmin = parts[1].toInt();
        unsigned long new_ddmax = parts[2].toInt();
        if (new_ddmin <= new_ddmax) {
          save_ddmin_ddmax(new_ddmin, new_ddmax);
          updateDisconnectionDuration(new_ddmin, new_ddmax);
          Serial.println("set OK!");
          Serial.println("ddmin: " + String(ddmin) + "\t ddmax : " + String(ddmax));
        } else {
          Serial.println("ddmin <= ddmax");
        }
      } else {
        Serial.println("yonnish");
      }
    } else if (command.startsWith("scd")) {
      String parts[3];
      int partCount = splitCommand(command, ' ', parts, 3);
      if (partCount == 3) {
        unsigned long new_cdmin = parts[1].toInt();
        unsigned long new_cdmax = parts[2].toInt();
        if (new_cdmin <= new_cdmax) {
          save_cdmin_cdmax(new_cdmin, new_cdmax);
          updateConnectionDuration(new_cdmin, new_cdmax);
          Serial.println("set OK!");
          Serial.println("cdmin: " + String(cdmin) + "\t cdmax : " + String(cdmax));
        } else {
          Serial.println("cdmin <= cdmax");
        }
      } else {
        Serial.println("yonnish");
      }
    } else if (command.startsWith("scl")) {
      String parts[2];
      int partCount = splitCommand(command, ' ', parts, 2);
      if (partCount == 2) {
        String new_string_cl = parts[1];
        if (new_string_cl == "1" || new_string_cl == "0") {
          char new_cl = new_string_cl.charAt(0);
          update_cl(new_cl);
          save_cl(new_cl);
        } else {
          Serial.println("yonnish");
        }
      } else {
        Serial.println("ayristirilamadi.");
      }
    } else if (command.startsWith("srp")) {
      String parts[2];
      int partCount = splitCommand(command, ' ', parts, 2);
      if (partCount == 2) {
        String new_string_rp = parts[1];
        uint8_t new_rp = new_string_rp.toInt();
        if (new_rp >= 2 && new_rp <= 13) {
          update_rp(new_rp);
          save_rp(new_rp);
        } else {
          Serial.println("yonnish");
        }
      } else {
        Serial.println("ayristirilamadi.");
      }
    } else if (command.startsWith("srm")) {
      String parts[2];
      int partCount = splitCommand(command, ' ', parts, 2);
      if (partCount == 2) {
        String new_rm = parts[1];
        if (new_rm == "0" || new_rm == "1") {
          char char_rm = new_rm.charAt(0);
          update_rm(char_rm);
          save_rm(char_rm);
        } else {
          Serial.println("yonnish");
        }
      } else {
        Serial.println("ayristirilamadi.");
      }
    } else if (command.startsWith("stm")) {
      String parts[2];
      int partCount = splitCommand(command, ' ', parts, 2);
      if (partCount == 2) {
        String new_tm = parts[1];
        if (new_tm == "0" || new_tm == "1") {
          char char_tm = new_tm.charAt(0);
          update_tm(char_tm);
          save_tm(char_tm);
        } else {
          Serial.println("yonnish");
        }
      } else {
        Serial.println("ayristirilamadi.");
      }
    } else if (command == "gdd") {
      Serial.println("ddmin: " + String(ddmin) + "\t ddmax : " + String(ddmax) + "\t ddcur: " + String(ddcur / 1000));
    } else if (command == "gcd") {
      Serial.println("cdmin: " + String(cdmin) + "\t cdmax : " + String(cdmax) + "\t cdcur: " + String(cdcur / 1000));
    } else if (command == "grm") {
      Serial.println("grm: " + String(relay_mode));
    } else if (command == "grp") {
      Serial.println("grp: " + String(relay_pin));
    } else if (command == "gcl") {
      Serial.println("gcl: " + String(config_location));
    } else if (command == "gtm") {
      Serial.println("gtm: " + String(timer_mode));
    } else if (command == "rst") {
      asm volatile("  jmp 0");
      Serial.println("\nrestarting\n");
    } else {
      Serial.println(command + " nedu? gafam almadi");
    }
  }
}

void loop() {
  unsigned long currentMillis = millis();
  processSerialCommands();
  if (timer_mode == '1') {
    if (relayState == LOW) {
      if (currentMillis - previousMillis >= ddcur) {
        updateConnectionDuration(cdmin, cdmax);
        Serial.println("Relay will be closed for " + String(cdcur / 1000) + " seconds.");
      }
    } else {
      if (currentMillis - previousMillis >= cdcur) {
        updateDisconnectionDuration(ddmin, ddmax);
        Serial.println("Relay will be open for " + String(ddcur / 1000) + " seconds.");
      }
    }
  } else {
    digitalWrite(relay_pin, HIGH);
    relayState = HIGH;
  }
}