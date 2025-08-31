#!/usr/bin/env python3
import os
import re
import glob

def extract_content_between_tags(content, start_tag, end_tag):
    """Extract content between specific HTML tags"""
    pattern = f'{re.escape(start_tag)}(.*?){re.escape(end_tag)}'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""

def convert_template_to_base(file_path):
    """Convert a template to extend base_navbar.html"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already extends base_navbar
    if 'base_navbar.html' in content:
        return False, "Already extends base_navbar"
    
    # Skip login/dashboard pages that don't need navbar
    filename = os.path.basename(file_path)
    if filename in ['admin_dashboard.html', 'logout.html']:
        return False, "Login/logout page - skipping"
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "Brighway School Management"
    
    # Extract main content (everything inside main content area)
    # Look for common patterns in the existing templates
    main_content = ""
    
    # Pattern 1: Content inside col-md-10 or similar main area
    main_pattern = r'<div class="col-md-(?:9|10)[^>]*>(.*?)</div>\s*</div>\s*</div>'
    main_match = re.search(main_pattern, content, re.DOTALL)
    
    if main_match:
        main_content = main_match.group(1).strip()
    else:
        # Pattern 2: Content after sidebar
        sidebar_end = content.find('</div>\s*<!-- Main')
        if sidebar_end == -1:
            sidebar_end = content.find('<!-- Main Form Area -->')
        if sidebar_end == -1:
            sidebar_end = content.find('<div class="col-md-10')
        
        if sidebar_end != -1:
            remaining = content[sidebar_end:]
            # Find the main content div
            div_start = remaining.find('<div class="col-md-10')
            if div_start != -1:
                div_content = remaining[div_start:]
                # Extract content inside this div
                level = 0
                start_pos = div_content.find('>') + 1
                for i, char in enumerate(div_content[start_pos:], start_pos):
                    if char == '<':
                        if div_content[i:i+4] == '<div':
                            level += 1
                        elif div_content[i:i+6] == '</div>':
                            level -= 1
                            if level < 0:
                                main_content = div_content[start_pos:i].strip()
                                break
    
    # If we couldn't extract content properly, extract everything between body tags
    if not main_content:
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if body_match:
            body_content = body_match.group(1).strip()
            # Remove sidebar content
            sidebar_pattern = r'<div class="col-md-[23][^>]*sidebar[^>]*>.*?</div>'
            body_content = re.sub(sidebar_pattern, '', body_content, flags=re.DOTALL)
            main_content = body_content
    
    # Extract any extra CSS
    extra_css = ""
    style_matches = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_matches:
        extra_css = '\n'.join(f'<style>{style}</style>' for style in style_matches)
    
    # Extract any extra JS
    extra_js = ""
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    if script_matches:
        extra_js = '\n'.join(f'<script>{script}</script>' for script in script_matches if 'bootstrap' not in script and 'cdn.jsdelivr.net' not in script)
    
    # Create new template content
    new_content = f'''{% extends "base_navbar.html" %}

{% block title %}{title}{% endblock %}

{% block extra_css %}
{extra_css}
{% endblock %}

{% block content %}
{main_content}
{% endblock %}

{% block extra_js %}
{extra_js}
{% endblock %}'''
    
    return True, new_content

def main():
    template_dir = r"c:\Users\A_R\Desktop\Brighway Site\website\bri\templates"
    html_files = glob.glob(os.path.join(template_dir, "*.html"))
    
    print("Converting templates to use base_navbar.html...")
    print("=" * 50)
    
    converted = 0
    skipped = 0
    errors = 0
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        # Skip base template itself
        if filename == 'base_navbar.html':
            continue
            
        try:
            success, result = convert_template_to_base(file_path)
            
            if success:
                # Backup original
                backup_path = file_path + '.backup'
                with open(file_path, 'r', encoding='utf-8') as f:
                    original = f.read()
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original)
                
                # Write new content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                print(f"✓ Converted {filename}")
                converted += 1
            else:
                print(f"- Skipped {filename}: {result}")
                skipped += 1
                
        except Exception as e:
            print(f"✗ Error converting {filename}: {e}")
            errors += 1
    
    print(f"\nSummary:")
    print(f"Converted: {converted}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"\nBackup files created with .backup extension")

if __name__ == "__main__":
    main()