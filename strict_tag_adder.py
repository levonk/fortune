#!/usr/bin/env python3

def should_add_tags(entry_lines):
    """Check if we should add tags to this entry."""
    has_author = any(line.startswith('\t- ') for line in entry_lines)
    has_content = any(not line.startswith('\t') and line.strip() and line != '%' 
                     for line in entry_lines)
    return has_author and has_content

def get_simple_tag(content, author):
    """Return a simple tag based on content."""
    content_lower = content.lower()
    
    if any(word in content_lower for word in ['lead', 'leader', 'manage', 'team']):
        return '#leadership'
    if any(word in content_lower for word in ['business', 'company', 'market']):
        return '#business'
    if any(word in content_lower for word in ['learn', 'knowledge', 'wisdom']):
        return '#wisdom'
    if any(word in content_lower for word in ['work', 'effort', 'hard work']):
        return '#work'
    if any(word in content_lower for word in ['dream', 'vision', 'goal']):
        return '#goals'
    if any(word in content_lower for word in ['science', 'technology', 'computer']):
        return '#tech'
    if any(word in content_lower for word in ['art', 'create', 'imagine']):
        return '#creativity'
    
    return '#quote'

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
            if should_add_tags(current_entry):
                # Get content (all non-author, non-empty lines)
                content_lines = [l for l in current_entry 
                               if not l.startswith('\t- ') 
                               and l.strip() 
                               and l != '%']
                content = ' '.join(content_lines)
                
                # Get author (last line that starts with \t- )
                author_line = next((l for l in reversed(current_entry) 
                                  if l.startswith('\t- ')), '')
                
                # Get simple tag
                tag = get_simple_tag(content, author_line)
                
                # Insert tag before the closing %
                current_entry.insert(-1, f'\t{tag}')
            
            # Add all lines of the entry to output
            output.append('\n'.join(current_entry))
            current_entry = []
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python strict_tag_adder.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
    print(f"Strict tags added successfully to {output_file}")
