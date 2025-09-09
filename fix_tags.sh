#!/bin/bash

# Create a temporary file for the modified content
temp_file=$(mktemp)

# Read the file line by line
while IFS= read -r line; do
    # If line contains the tags, process it
    if [[ "$line" == *"#model #think #modelthink"* ]]; then
        # Remove the tags from the current line
        clean_line=$(echo "$line" | sed 's/ #model #think #modelthink//')
        # Print the cleaned line
        echo "$clean_line"
        # Print the tags on a new line with indentation
        echo -e "\t#model #think #modelthink"
    else
        # Print other lines as-is
        echo "$line"
    fi
done < levonkquotes > "$temp_file"

# Replace the original file
mv "$temp_file" levonkquotes

echo "Tags have been moved below the author lines."
