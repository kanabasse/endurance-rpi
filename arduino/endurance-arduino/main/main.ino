#include <ht1632c.h>

ht1632c ledMatrix = ht1632c(&PORTD, 7, 6, 4, 5, GEOM_32x16, 2);

const int BUFFER_SIZE = 64;
uint8_t buffer[BUFFER_SIZE];
int receivedBytes = 0;

void setup() {
    ledMatrix.clear(); // Clean screen
    ledMatrix.pwm(10); // Set light level

    Serial.begin(921600); // Start serial communication
     // Wait for serial port to connect
    while (!Serial) {}
    //     Serial.println("Ready to receive...");
}

void loop() {
    while (Serial.available() > 0) {
        buffer[receivedBytes] = Serial.read();
        receivedBytes++;
        if (receivedBytes >= BUFFER_SIZE) {
            print_screen();
            receivedBytes = 0; // Reset for next transmission
        }
    }
}

void print_screen() {
//     for (int i = 0; i < BUFFER_SIZE; i++) {
//         Serial.print(buffer[i]);
//     }
//     Serial.println(BUFFER_SIZE);
//     Serial.println();

    ledMatrix.set_screen(buffer, GREEN);
    ledMatrix.sendframe();
}