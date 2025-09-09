#!/usr/bin/env python3

def is_complete_entry(entry):
    """Check if entry has both content and author."""
    has_author = any(line.startswith('\t- ') for line in entry)
    has_content = any(not line.startswith('\t') and line.strip() and line != '%' 
                     for line in entry)
    return has_author and has_content

def get_simple_tag(content):
    """Return a simple tag based on content."""
    content_lower = content.lower()
    if any(word in content_lower for word in ['lead', 'leader', 'manage', 'team', 'vision', 'foresight', 'ahead of the curve']):
        return '#leadership #foresight'
    if any(word in content_lower for word in ['business', 'company', 'market']):
        return '#business'
    if any(word in content_lower for word in ['learn', 'knowledge', 'wisdom']):
        return '#wisdom'
    if any(word in content_lower for word in ['success', 'succeed', 'achievement']):
        return '#success'
    return '#quote'

def process_file(input_file, output_file):
    """Process the input file and write tagged output to output file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]
    
    output = []
    current_entry = []
    
    for line in lines:
        current_entry.append(line)
        
        if line == '%':
            if is_complete_entry(current_entry):
                # Get content (all non-author, non-empty lines)
                content_lines = [l for l in current_entry 
                               if not l.startswith('\t- ') 
                               and l.strip() 
                               and l != '%']
                content = ' '.join(content_lines)
                
                # Get simple tag
                tag = get_simple_tag(content)
                if tag:
                    # Insert tag before the closing %
                    current_entry.insert(-1, f'\t{tag}')
            
            # Add all lines of the entry to output
            output.extend(current_entry)
            current_entry = []
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add_tags_to_complete_entries.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
    print(f"Tags added only to complete entries in {output_file}")
