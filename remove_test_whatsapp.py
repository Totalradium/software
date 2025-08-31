#!/usr/bin/env python3
import os
import re
import glob

def remove_test_whatsapp_from_file(file_path):
    """Remove all test_whatsapp references from a file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove test_whatsapp URL references
    patterns_to_remove = [
        r'<a[^>]*href="[^"]*test_whatsapp[^"]*"[^>]*>.*?</a>',
        r'<a[^>]*href="\{% url \'test_whatsapp\' %\}"[^>]*>.*?</a>',
        r'<li[^>]*>\s*<a[^>]*href="[^"]*test_whatsapp[^"]*"[^>]*>.*?</a>\s*</li>',
        r'<li[^>]*>\s*<a[^>]*href="\{% url \'test_whatsapp\' %\}"[^>]*>.*?</a>\s*</li>',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up extra whitespace and empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)
    
    # Check if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    template_dir = r"c:\Users\A_R\Desktop\Brighway Site\website\bri\templates"
    html_files = glob.glob(os.path.join(template_dir, "*.html"))
    
    print("Removing all test_whatsapp references from templates...")
    print("=" * 50)
    
    cleaned = 0
    no_changes = 0
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            if remove_test_whatsapp_from_file(file_path):
                print(f"✓ Cleaned {filename}")
                cleaned += 1
            else:
                print(f"- No test_whatsapp found in {filename}")
                no_changes += 1
                
        except Exception as e:
            print(f"✗ Error processing {filename}: {e}")
    
    print(f"\nSummary:")
    print(f"✓ Files cleaned: {cleaned}")
    print(f"- Files unchanged: {no_changes}")
    print(f"\nAll test_whatsapp references have been removed!")

if __name__ == "__main__":
    main()