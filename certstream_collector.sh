#!/bin/bash

# create source directory if it doesn't exist
mkdir -p source

# set the number of files to collect and the number of lines per file
num_files=100
lines_per_file=50000

# set the name of the output file
output_file="certstream_full.json"

# create an empty output file
echo "" > "source/$output_file"

# loop through the number of files to collect
for ((i=1;i<=$num_files;i++))
do
  # set the name of the current file
  current_file="certstream_full_$i.json"
  
  # listen for JSON files and save them to the current file
  certstream --json --full | head -n $(( $lines_per_file * 2 )) | awk 'NR==1{print "["}{if (NR>1) {print ","}}{print}END{print "]"}' n=$lines_per_file >> "source/$current_file"
  
  # add a comma to the end of the previous file if it's not empty
  if [[ $(wc -c < "source/$output_file") -gt 0 ]]
  then
    sed -i '$s/$/,/' "source/$output_file"
  fi

  # concatenate the current file to the output file
  cat "source/$current_file" >> "source/$output_file"
  
  # remove the current file
  #rm "source/$current_file"
done
