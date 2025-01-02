//Below is the script runnning on the Arduino board to detect the signals from the computer

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(115200);  // Start serial communication
    digitalWrite(LED_BUILTIN, HIGH);  // Turn LED off initially
}

void loop() {
    if (Serial.available() > 0) {
        String input = Serial.readString();
        input.trim();  // Remove any newlines or extra spaces

        if (input == "ON") {
            digitalWrite(LED_BUILTIN, LOW);  // Turn the LED on
            Serial.println("LED is ON");  // Send confirmation
        } else if (input == "OFF") {
            digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED off
            Serial.println("LED is OFF");  // Send confirmation
        }
    }
}
