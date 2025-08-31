#!/usr/bin/env python3
import os
import glob

def find_batch_management_files():
    """Find all HTML files with batch_management in navbar and check if they need Subject Management sub-option"""
    
    template_dir = r"c:\Users\A_R\Desktop\Brighway Site\website\bri\templates"
    html_files = glob.glob(os.path.join(template_dir, "*.html"))
    
    print("Finding HTML files with batch_management in navbar...")
    print("=" * 50)
    
    files_with_batch = []
    files_need_update = []
    files_already_correct = []
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if file has batch_management
            if 'batch_management' in content:
                files_with_batch.append(filename)
                
                # Check if it already has subject_management sub-option
                if 'subject_management' in content and 'margin-left: 20px' in content:
                    files_already_correct.append(filename)
                else:
                    files_need_update.append(filename)
                    
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    
    print(f"\nFiles with batch_management: {len(files_with_batch)}")
    for f in files_with_batch:
        print(f"  - {f}")
    
    print(f"\nFiles that NEED UPDATE: {len(files_need_update)}")
    for f in files_need_update:
        print(f"  - {f}")
    
    print(f"\nFiles ALREADY CORRECT: {len(files_already_correct)}")
    for f in files_already_correct:
        print(f"  - {f}")
    
    return files_need_update

def fix_batch_management_files(files_to_fix):
    """Add Subject Management sub-option to files that need it"""
    
    template_dir = r"c:\Users\A_R\Desktop\Brighway Site\website\bri\templates"
    
    for filename in files_to_fix:
        file_path = os.path.join(template_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace batch_management line
            old_pattern = 'href="{% url \'batch_management\' %}">Batch Management</a>'
            new_pattern = '''href="{% url 'batch_management' %}">Batch Management</a>
        <a href="{% url 'subject_management' %}" style="margin-left: 20px; font-size: 14px;">Subject Management</a>'''
            
            if old_pattern in content:
                updated_content = content.replace(old_pattern, new_pattern)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"✓ Updated {filename}")
            else:
                print(f"✗ Could not find pattern in {filename}")
                
        except Exception as e:
            print(f"✗ Error updating {filename}: {e}")

if __name__ == "__main__":
    print("Batch Management Navbar Checker")
    print("=" * 40)
    
    files_to_fix = find_batch_management_files()
    
    if files_to_fix:
        print(f"\nFound {len(files_to_fix)} files that need updating.")
        response = input("Do you want to fix them automatically? (y/n): ")
        
        if response.lower() == 'y':
            print("\nFixing files...")
            fix_batch_management_files(files_to_fix)
            print("\nDone!")
        else:
            print("No changes made.")
    else:
        print("\nAll files are already correct!")