#!/bin/bash
read volume1 volume2 <<< $(pactl get-sink-volume @DEFAULT_SINK@ | awk 'NR == 1 {printf $5 " " $12}')
echo "[$volume1%] [$volume2%]"
