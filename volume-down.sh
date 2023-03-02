#!/bin/bash

volumeIncrement=2
volume=$(pactl get-sink-volume @DEFAULT_SINK@ | awk 'NR == 1 {print $5}' | sed 's/%//')
newVolume=$((volume - volumeIncrement))
if [ $newVolume -gt 100 ]; then
	newVolume=100
fi
if [ $newVolume -lt 0 ]; then
	newVolume=0
fi
pactl set-sink-volume @DEFAULT_SINK@ $newVolume%
