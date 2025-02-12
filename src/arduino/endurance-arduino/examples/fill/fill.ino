#include <ht1632c.h>

ht1632c ledMatrix = ht1632c(&PORTD, 7, 6, 4, 5, GEOM_32x16, 2);
int GEOM_WIDTH=32;
int GEOM_HEIGHT=16;


void setup() {
  ledMatrix.clear();
}

void loop() {
  for (byte i=0; i<GEOM_WIDTH; i++) {
    for (byte j=0; j<GEOM_HEIGHT; j++) {
      ledMatrix.plot(i, j, RED);
      ledMatrix.sendframe();
      delay(1);
    }
  }

  for (byte i=0; i<GEOM_WIDTH; i++) {
    for (byte j=0; j<GEOM_HEIGHT; j++) {
      ledMatrix.plot(i, j, ORANGE);
      ledMatrix.sendframe();
      delay(1);
    }
  }

    for (byte i=0; i<GEOM_WIDTH; i++) {
    for (byte j=0; j<GEOM_HEIGHT; j++) {
      ledMatrix.plot(i, j, GREEN);
      ledMatrix.sendframe();
      delay(1);
    }
  }
  
  for (byte i=0; i<GEOM_WIDTH; i++) {
    for (byte j=0; j<GEOM_HEIGHT; j++) {
      ledMatrix.plot(i, j, BLACK);
      ledMatrix.sendframe();
      delay(1);
    }
  }
}

