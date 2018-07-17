#!/bin/bash
# a script to take isbn into json

# empty output file
> ex_data_proper.txt

echo "[" >> ex_data_proper.txt
count=0

# read in raw ISBNs and output google api results json
while IFS='' read -r line || [[ -n "$line" ]]; do
	
	if [[ $count -ne 0 ]]; then
    	echo "," >> ex_data_proper.txt
    fi

    prefix="https://www.googleapis.com/books/v1/volumes?q=isbn:"
    suffix=$line
    admin="&key=AIzaSyB1j7GLnJulfxV4yDyEGTwOCEj--qAdnmQ"
    search=$prefix$suffix$admin
    curl -s $search >> ex_data_proper.txt

    sleep 1.1

    echo "line read: $line"
    count=$(($count+1))
done < "$1"

echo "]" >> ex_data_proper.txt