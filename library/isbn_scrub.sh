#!/bin/bash
# a script to take isbn into json

# empty output file
> ex_data.txt

echo "[" >> ex_data.txt
count=0

# read in raw ISBNs and output google api results json
while IFS='' read -r line || [[ -n "$line" ]]; do
	
	if [[ $count -ne 0 ]]; then
    	echo "," >> ex_data.txt
    fi

    prefix="https://www.googleapis.com/books/v1/volumes?q=isbn:"
    suffix=$line
    search=$prefix$suffix
    curl -s $search >> ex_data.txt

    sleep 0.5

    echo "line read: $line"
    count=$(($count+1))
done < "$1"

echo "]" >> ex_data.txt

python process.py