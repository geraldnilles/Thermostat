#!/usr/bin/env bash


for size in 512 192 180 32 16
do

	ffmpeg -i input.png \
		-vf scale=$size:$size \
		icon-$size.png 

done


