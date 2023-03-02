#!/bin/bash

amount=0.1
maxBrightness=1.0
minBrightness=0.1

screenIndex=$1
if [ ! $screenIndex ]; then
	exit 1
fi

screenInfo=$(xrandr --current --verbose | grep -B7 -F "CRTC:       $screenIndex")
if [ ! "$screenInfo" ]; then
	exit 1
fi

screenName=$(echo "$screenInfo" | awk '/connected/ {print $1}')
if [ ! "$screenName" ]; then
	exit 1
fi

currentBrightness=$(echo "$screenInfo" | grep -F "Brightness:" | awk '{print $2}')
if [[ ! $currentBrightness || 
	"$currentBrightness" = "inf" || 
	"$currentBrightness" == *e* ]]; then
	xrandr --output $screenName --brightness $maxBrightness > /dev/null
	exit 0
fi

newBrightness=$(echo "$currentBrightness-$amount" | bc)
greaterThanMax=$(echo "$newBrightness>$maxBrightness" | bc)
lessThanMin=$(echo "$newBrightness<$minBrightness" | bc)

if [[ $greaterThanMax -eq 1 ]]; then
	newBrightness=$maxBrightness
fi

if [[ $lessThanMin -eq 1 ]]; then
	newBrightness=$minBrightness
fi


xrandr --output $screenName --brightness $newBrightness > /dev/null
echo $newBrightness
