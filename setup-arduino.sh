#!/bin/bash
set -e

BOARD="arduino:avr:uno"
SCHEMA="main/main.ino"
INTERFACE="/dev/ttyACM0"

pushd .
cd src/arduino

rm -rf dist/ht1632c.zip
zip -r9 dist/ht1632c.zip endurance-arduino
arduino-cli lib install --config-file arduino.yaml --zip-path dist/ht1632c.zip

cd endurance-arduino
# Compile and upload $SCHEMA to $BOARD
arduino-cli compile --clean -b $BOARD $SCHEMA
arduino-cli upload -b $BOARD -p $INTERFACE $SCHEMA

popd