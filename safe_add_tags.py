#!/usr/bin/env python3

import re

def get_tags(content, author):
    """Generate descriptive tags based on content and author."""
    tags = set()
    content_lower = content.lower()
    
    # Topic-based tags
    topics = {
        'leadership': ['lead', 'leader', 'manage', 'team', 'vision', 'inspire', 'guide'],
        'success': ['succeed', 'achieve', 'accomplish', 'excellence', 'greatness'],
        'business': ['company', 'startup', 'entrepreneur', 'market', 'customer', 'product'],
        'wisdom': ['learn', 'knowledge', 'understand', 'insight', 'wise'],
        'work': ['effort', 'hard work', 'dedication', 'persevere', 'discipline'],
        'goals': ['dream', 'vision', 'goal', 'aspire', 'ambition'],
        'life': ['live', 'experience', 'journey', 'purpose', 'meaning'],
        'thinking': ['think', 'thought', 'mind', 'intellect', 'reasoning'],
        'tech': ['technology', 'computer', 'code', 'software', 'digital', 'ai', 'machine learning'],
        'creativity': ['art', 'create', 'imagination', 'innovate', 'design', 'invent'],
        'education': ['learn', 'teach', 'school', 'study', 'knowledge'],
        'philosophy': ['truth', 'meaning', 'existence', 'ethics', 'morality'],
        'science': ['research', 'discover', 'experiment', 'physics', 'biology', 'chemistry'],
        'history': ['past', 'historical', 'war', 'revolution', 'ancient'],
        'politics': ['government', 'power', 'democracy', 'freedom', 'rights'],
        'relationships': ['love', 'friend', 'family', 'partner', 'relationship'],
        'emotion': ['feel', 'emotion', 'happy', 'sad', 'angry', 'fear']
    }
    
    # Add topic tags based on content
    for topic, keywords in topics.items():
        if any(keyword in content_lower for keyword in keywords):
            tags.add(f'#{topic}')
    
    # Author-specific tags
    author_lower = author.lower()
    if 'edison' in author_lower:
        tags.update(['#invention', '#perseverance', '#innovation'])
    if 'einstein' in author_lower:
        tags.update(['#science', '#genius', '#physics'])
    if 'jobs' in author_lower:
        tags.update(['#innovation', '#design', '#technology'])
    if 'disney' in author_lower:
        tags.update(['#creativity', '#imagination', '#storytelling'])
    
    # If no specific tags matched, add general ones
    if not tags:
        words = re.findall(r'\b\w+\b', content_lower)
        if len(words) < 15:
            tags.add('#thought')
        else:
            tags.add('#insight')
    
    return ' '.join(sorted(tags))

def process_file(input_file, output_file):
    """Process the input file and write tagged output to output file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output = []
    current_entry = []
    
    for line in lines:
        line = line.rstrip()
        
        if line == '%':
            if current_entry:
                # Process the completed entry
                entry_text = '\n'.join(current_entry)
                # Find the last line that starts with a tab (author line)
                author_line = next((line for line in reversed(current_entry) if line.startswith('\t- ')), '')
                author = author_line[3:] if author_line else 'Unknown'
                
                # Get content (everything except author line)
                content_lines = [l for l in current_entry if not l.startswith('\t- ')]
                content = ' '.join(content_lines)
                
                # Only add tags if there's content and an author
                if content.strip() and author_line:
                    # Get tags
                    tags = get_tags(content, author)
                    # Add original content
                    output.extend(current_entry)
                    # Add tags
                    output.append(f'\t{tags}')
                else:
                    # Keep original content as is
                    output.extend(current_entry)
                
                output.append('%')
                current_entry = []
            else:
                output.append('%')
        else:
            current_entry.append(line)
    
    # Process any remaining entry
    if current_entry:
        output.extend(current_entry)
        output.append('%')
    
    # Write the output file with original line endings
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python safe_add_tags.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
    print(f"Tags added successfully to {output_file}")
