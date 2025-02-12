#include <ht1632c.h>

ht1632c ledMatrix = ht1632c(&PORTD, 7, 6, 4, 5, GEOM_32x16, 2);

const int SCREEN_SIZE = 64;
int receivedBytes = 0;

struct Packet {
    uint8_t COLOR;
    uint8_t DATA[SCREEN_SIZE];
    bool PRINT;
};

uint8_t buffer[sizeof(struct Packet)];


void setup() {
    ledMatrix.clear(); // Clean screen
    ledMatrix.pwm(10); // Set light level

    Serial.begin(921600); // Start serial communication
     // Wait for serial port to connect
    while (!Serial) {}
    //     Serial.println("Ready to receive...");
}

void loop() {
    if (read_data() == 0) {
        struct Packet packet;
        parse_packet(&packet);
        print_screen(&packet);
    }
}

/*
    Read data from serial and input it in buffer[]
    Return 0 if data is ready to be parsed, else return 1
*/
int read_data() {
    while (Serial.available() > 0) {
        buffer[receivedBytes] = Serial.read();
        receivedBytes++;
        if (receivedBytes >= sizeof(struct Packet)) {
            receivedBytes = 0; // Reset for next transmission
            return 0;
        }
    }
    return 1;
}

uint8_t parse_packet(struct Packet *packet) {
    memcpy(packet, buffer, sizeof(struct Packet));
}

void print_screen(struct Packet *packet) {
    ledMatrix.set_screen(packet->DATA, packet->COLOR);
    ledMatrix.sendframe();
}