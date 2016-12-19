#!/bin/bash

cd gifs/
mkdir ../mp4

for file in `ls`
do
	output="${file/.gif/.mp4}"
	output="../mp4/$output"
	echo $output

	dimensions=`identify -format "%w %h" $file`
	
	echo ${dimensions[0]}
	
	ffmpeg -f gif -i $file -vf "scale=iw*min(1280/iw\,720/ih):ih*min(1280/iw\,720/ih),pad=1280:720:(1280-iw)/2:(720-ih)/2" -r 30 $output
	echo "$file converted"
done

cd ../mp4

for f in `ls`; do echo "file $f" >> list.txt; done

ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
