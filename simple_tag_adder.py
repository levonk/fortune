#!/usr/bin/env python3

import re

def get_tags(content, author):
    """Generate simple tags based on content and author."""
    tags = set()
    content_lower = content.lower()
    
    # Simple topic detection
    topics = {
        'leadership': ['lead', 'leader', 'manage', 'team', 'vision', 'inspire'],
        'business': ['company', 'startup', 'entrepreneur', 'market', 'customer'],
        'wisdom': ['learn', 'knowledge', 'understand', 'insight', 'wise'],
        'work': ['effort', 'work', 'dedication', 'persevere', 'discipline'],
        'success': ['succeed', 'achieve', 'accomplish', 'excellence', 'greatness'],
        'life': ['live', 'experience', 'journey', 'purpose', 'meaning']
    }
    
    for topic, keywords in topics.items():
        if any(keyword in content_lower for keyword in keywords):
            tags.add(f'#{topic}')
    
    if not tags:
        tags.add('#quote')
    
    return ' '.join(sorted(tags))

def process_file(input_file, output_file):
    """Process the input file and write tagged output to output file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output = []
    current_entry = []
    
    for line in lines:
        line = line.rstrip()
        current_entry.append(line)
        
        if line == '%':
            # Process the completed entry
            if len(current_entry) > 1:  # Not just a single %
                # Find author line (last line that starts with \t- )
                author_line = next((l for l in reversed(current_entry[:-1]) if l.startswith('\t- ')), '')
                author = author_line[3:] if author_line else ''
                
                # Get content (all lines except author and %)
                content_lines = [l for l in current_entry if l != '%' and not l.startswith('\t- ')]
                content = ' '.join(content_lines)
                
                # Only add tags if we have both content and author
                if content.strip() and author:
                    tags = get_tags(content, author)
                    # Insert tags before the closing %
                    current_entry.insert(-1, f'\t{tags}')
            
            # Add all lines of the entry to output
            output.append('\n'.join(current_entry))
            current_entry = []
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python simple_tag_adder.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
    print(f"Simple tags added successfully to {output_file}")
