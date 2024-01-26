#include <Servo.h>

Servo myservo;
int pressPosition = 107;
int releasePosition = 90;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (isValidInput(input)) {
      int pressDuration = input.toInt();
      pressAndReleaseTheButton(pressDuration);
    } else {
      Serial.println("Geçersiz giriş. 1 ile 16 arasında bir değer girin.");
    }
  }
}

bool isValidInput(String input) {
  if (input.length() > 0 && isDigit(input[0])) {
    int inputVal = input.toInt();
    return (inputVal >= 1 && inputVal <= 16);
  }
  return false;
}

void pressAndReleaseTheButton(int pressDuration) {
  myservo.write(pressPosition);
  delay(pressDuration * 1000);
  myservo.write(releasePosition);
}
