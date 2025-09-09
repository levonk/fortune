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
    
    # Content type tags
    if '?' in content and not any(word in content_lower for word in ['what', 'why', 'how', 'when', 'where']):
        tags.add('#rhetorical')
    if any(word in content_lower for word in ['should', 'must', 'ought to', 'need to']):
        tags.add('#advice')
    if any(word in content_lower for word in ['because', 'reason', 'since', 'as a result']):
        tags.add('#reasoning')
    if len(content.split()) < 10:  # Very short quotes
        tags.add('#aphorism')
    
    # Author-specific tags
    author_lower = author.lower()
    if 'edison' in author_lower:
        tags.update(['#invention', '#perseverance', '#innovation'])
    if 'einstein' in author_lower:
        tags.update(['#science', '#genius', '#physics'])
    if 'jobs' in author_lower:
        tags.update(['#innovation', '#design', '#technology'])
    if 'king' in author_lower and ('martin luther' in author_lower or 'mlk' in author_lower):
        tags.update(['#civilrights', '#equality', '#justice'])
    if 'disney' in author_lower:
        tags.update(['#creativity', '#imagination', '#storytelling'])
    
    # If no specific tags matched, analyze content more deeply
    if len(tags) < 2:  # If we have very few tags
        words = re.findall(r'\b\w+\b', content_lower)
        word_count = len(words)
        
        # Add length-based tags
        if word_count < 5:
            tags.add('#short')
        elif word_count > 50:
            tags.add('#longform')
        
        # Add sentiment-based tags
        positive_words = ['love', 'great', 'wonderful', 'amazing', 'best', 'excellent']
        negative_words = ['hate', 'terrible', 'worst', 'never', 'cannot', 'fail']
        
        if any(word in content_lower for word in positive_words):
            tags.add('#positive')
        if any(word in content_lower for word in negative_words):
            tags.add('#negative')
        
        # If still no tags, add general ones based on content
        if not tags:
            if word_count < 15:
                tags.add('#thought')
            else:
                tags.add('#insight')
    
    # Ensure we have at least one tag
    if not tags:
        tags.add('#quote')
    
    # Sort tags alphabetically for consistency
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
                
                # Get tags
                tags = get_tags(content, author)
                
                # Rebuild the entry with original content plus tags
                output_entry = current_entry.copy()
                
                # Remove the author line if it exists
                if author_line in output_entry:
                    output_entry.remove(author_line)
                
                # Add author line back (if it exists) followed by tags
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
    
    # Process any remaining entry
    if current_entry:
        entry_text = '\n'.join(current_entry)
        author_line = next((line for line in reversed(current_entry) if line.startswith('\t- ')), '')
        author = author_line[3:] if author_line else 'Unknown'
        content_lines = [l for l in current_entry if not l.startswith('\t- ')]
        content = ' '.join(content_lines)
        
        # Get tags
        tags = get_tags(content, author)
        
        # Rebuild the entry with original content plus tags
        output_entry = current_entry.copy()
        
        # Remove the author line if it exists
        if author_line in output_entry:
            output_entry.remove(author_line)
        
        # Add author line back (if it exists) followed by tags
        if author_line:
            output_entry.append(author_line)
        
        # Add tags
        output_entry.append(f'\t{tags}')
        
        # Add to output
        output.extend(output_entry)
        output.append('%')
    
    # Write the output file with original line endings
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python improved_tags.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
    print(f"Improved tags added successfully. Output written to {output_file}")
