#!/bin/bash
set -ex

BOARD="arduino:avr:uno"
SCHEMA="main/main.ino"
INTERFACE="/dev/ttyACM0"
CLI_DIR="$PWD/src/arduino"

pushd .
cd src/arduino

mkdir -p dist
rm -rf dist/ht1632c.zip
zip -r9 dist/ht1632c.zip endurance-arduino
"$CLI_DIR"/arduino-cli lib install --config-file arduino.yaml --zip-path dist/ht1632c.zip
"$CLI_DIR"/arduino-cli core install arduino:avr

cd endurance-arduino
# Compile and upload $SCHEMA to $BOARD
echo "Uploading main.ino..."
"$CLI_DIR"/arduino-cli compile --clean -b $BOARD $SCHEMA
"$CLI_DIR"/arduino-cli upload -b $BOARD -p $INTERFACE $SCHEMA
echo "Uploaded!"
popd