#!/bin/bash

defaultSinkName=$(pactl get-default-sink)
sinkNames=($(pactl list short sinks | awk '{print $2}'))
sinkCount=${#sinkNames[*]}
nextSinkName=$defaultSinkName

for i in ${!sinkNames[*]}; do
        if [ ${sinkNames[$i]} == $defaultSinkName ]; then
                nextSinkIndex=$(((i - 1) % $sinkCount))
                nextSinkName=${sinkNames[$nextSinkIndex]}
                break
        fi
done

pactl set-default-sink $nextSinkName
sinkInputs=($(pactl list short sink-inputs | awk '{print $1}'))
for input in ${sinkInputs[*]}; do pactl move-sink-input $input $nextSinkName; done
