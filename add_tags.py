#!/usr/bin/env python3

import re

def get_tags(content, author):
    """Determine appropriate tags based on content and author."""
    tags = set()
    content_lower = content.lower()
    
    # Common tags based on content
    if any(word in content_lower for word in ['leadership', 'leader', 'manage', 'team']):
        tags.add('#leadership')
    if any(word in content_lower for word in ['success', 'achieve', 'succeed']):
        tags.add('#success')
    if any(word in content_lower for word in ['business', 'company', 'startup', 'entrepreneur']):
        tags.add('#business')
    if any(word in content_lower for word in ['learn', 'knowledge', 'wisdom', 'understand']):
        tags.add('#wisdom')
    if any(word in content_lower for word in ['work', 'effort', 'hard work']):
        tags.add('#work')
    if any(word in content_lower for word in ['dream', 'vision', 'goal']):
        tags.add('#goals')
    if any(word in content_lower for word in ['life', 'live', 'experience']):
        tags.add('#life')
    if any(word in content_lower for word in ['think', 'thought', 'mind']):
        tags.add('#thinking')
    if any(word in content_lower for word in ['science', 'technology', 'tech', 'computer']):
        tags.add('#tech')
    if any(word in content_lower for word in ['art', 'creative', 'create', 'imagination']):
        tags.add('#creativity')
    
    # Special case for known authors
    if 'edison' in author.lower():
        tags.add('#invention')
        tags.add('#perseverance')
    if 'einstein' in author.lower():
        tags.add('#science')
        tags.add('#genius')
    if 'jobs' in author.lower():
        tags.add('#innovation')
        tags.add('#design')
    
    # If no tags matched, add a general one
    if not tags:
        tags.add('#quote')
    
    return ' '.join(sorted(tags))

def process_file(input_file, output_file):
    """Process the input file and write tagged output to output file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]
    
    output = []
    current_entry = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line == '%':
            if current_entry:
                # Process the completed entry
                entry_text = '\n'.join(current_entry)
                # Find the last line that starts with a tab (author line)
                author_line = next((line for line in reversed(current_entry) if line.startswith('\t- ')), '')
                author = author_line[3:] if author_line else 'Unknown'
                
                # Get content (everything except author line and empty lines)
                content_lines = [l for l in current_entry if l.strip() and not l.startswith('\t- ')]
                content = ' '.join(content_lines)
                
                # Get tags
                tags = get_tags(content, author)
                
                # Rebuild the entry with original structure plus tags
                output_entry = []
                # Add all lines except the author line
                output_entry = [line for line in current_entry if not line.startswith('\t- ')]
                
                # Add author line if it exists
                if author_line:
                    output_entry.append(author_line)
                
                # Add tags
                output_entry.append(f'\t{tags}')
                
                # Add to output
                output.extend(output_entry)
                output.append('%')
                current_entry = []
            else:
                output.append('%')
        else:
            current_entry.append(line)
            
        i += 1
    
    # Process any remaining entry
    if current_entry:
        author_line = next((line for line in reversed(current_entry) if line.startswith('\t- ')), '')
        author = author_line[3:] if author_line else 'Unknown'
        
        # Get content (everything except author line and empty lines)
        content_lines = [l for l in current_entry if l.strip() and not l.startswith('\t- ')]
        content = ' '.join(content_lines)
        
        # Get tags
        tags = get_tags(content, author)
        
        # Rebuild the entry with original structure plus tags
        output_entry = [line for line in current_entry if not line.startswith('\t- ')]
        
        # Add author line if it exists
        if author_line:
            output_entry.append(author_line)
        
        # Add tags
        output_entry.append(f'\t{tags}')
        
        # Add to output
        output.extend(output_entry)
        output.append('%')
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add_tags.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
    print(f"Tags added successfully. Output written to {output_file}")
