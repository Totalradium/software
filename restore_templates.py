import os
import shutil

template_dir = r"c:\Users\A_R\Desktop\Brighway Site\website\bri\templates"

# Get all backup files
backup_files = [f for f in os.listdir(template_dir) if f.endswith('.backup')]

for backup_file in backup_files:
    original_file = backup_file.replace('.backup', '')
    backup_path = os.path.join(template_dir, backup_file)
    original_path = os.path.join(template_dir, original_file)
    
    # Copy backup to original
    shutil.copy2(backup_path, original_path)
    print(f"Restored {original_file}")

# Remove base_navbar references from all files
for filename in os.listdir(template_dir):
    if filename.endswith('.html') and not filename.endswith('.backup'):
        filepath = os.path.join(template_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove base_navbar references
        if 'base_navbar.html' in content:
            lines = content.split('\n')
            cleaned_lines = []
            skip_block = False
            
            for line in lines:
                if 'extends "base_navbar.html"' in line:
                    skip_block = True
                    continue
                elif skip_block and ('{% block' in line or '{% endblock' in line):
                    if '{% endblock %}' in line:
                        skip_block = False
                    continue
                elif not skip_block:
                    cleaned_lines.append(line)
            
            new_content = '\n'.join(cleaned_lines)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned base_navbar from {filename}")

print("All templates restored to original working state")