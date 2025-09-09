#!/bin/bash

# Create a temporary file for the modified content
temp_file=$(mktemp)

# Process the file
awk '
/^[^\t]/ && !/^%/ {  # If line starts with non-tab and is not a %
    if (content != "") {
        # If we have content, print it and reset
        print content
        content = $0
    } else {
        content = $0
    }
    next
}

/^\t/ {  # If line starts with tab (author line)
    if ($0 ~ /#model #think #modelthink/) {
        # If tags are in the author line, move them to their own line
        author_line = $0
        gsub(/\s*#model #think #modelthink/, "", author_line)  # Remove tags from author line
        print author_line
        print "\t#model #think #modelthink"
    } else {
        print $0
    }
    content = ""
    next
}

/^%/ {  # If line is a % separator
    if (content != "") {
        print content
        content = ""
    }
    print $0
    next
}

{  # For all other lines
    if (content != "") {
        content = content "\n" $0
    } else {
        print $0
    }
}

END {
    if (content != "") {
        print content
    }
}
' levonkquotes > "$temp_file"

# Replace the original file
mv "$temp_file" levonkquotes

echo "Tags have been moved below the author lines."
