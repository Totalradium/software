import os
import re

template_dir = r"c:\Users\A_R\Desktop\Brighway Site\website\bri\templates"

for filename in os.listdir(template_dir):
    if filename.endswith('.html') and not filename.endswith('.backup'):
        filepath = os.path.join(template_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove test_whatsapp lines
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            if 'test_whatsapp' not in line.lower():
                cleaned_lines.append(line)
        
        new_content = '\n'.join(cleaned_lines)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned {filename}")

print("Done removing test_whatsapp references")