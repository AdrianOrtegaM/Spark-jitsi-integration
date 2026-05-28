#!/bin/bash

echo "Ejecutando producer..."
python producer_frames.py &

echo "Ejecutando consumer..."
python consumer_frames.py
