#!/usr/bin/env python3
import os
import re
import glob

def convert_template(file_path):
    """Convert a template to extend base_navbar.html"""
    
    filename = os.path.basename(file_path)
    
    # Skip files that don't need conversion
    skip_files = [
        'base_navbar.html', 'admin_dashboard.html', 'logout.html', 
        'batch_management_backup.html'
    ]
    
    if filename in skip_files:
        return False, f"Skipping {filename}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already extends base_navbar
    if 'base_navbar.html' in content:
        return False, f"{filename} already extends base_navbar"
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "Brighway School Management"
    
    # Extract custom CSS
    extra_css = ""
    style_matches = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_matches:
        # Filter out common styles that are now in base
        filtered_styles = []
        for style in style_matches:
            # Remove sidebar and common styles
            style_clean = re.sub(r'\.sidebar[^}]*}', '', style)
            style_clean = re.sub(r'body\s*{[^}]*}', '', style_clean)
            if style_clean.strip():
                filtered_styles.append(style_clean.strip())
        
        if filtered_styles:
            extra_css = '<style>\n' + '\n'.join(filtered_styles) + '\n</style>'
    
    # Extract main content
    main_content = extract_main_content(content)
    
    # Extract custom JavaScript
    extra_js = ""
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    if script_matches:
        filtered_scripts = []
        for script in script_matches:
            # Skip Bootstrap and CDN scripts
            if ('bootstrap' not in script.lower() and 
                'cdn.jsdelivr.net' not in script and 
                'cdnjs.cloudflare.com' not in script and
                script.strip()):
                filtered_scripts.append(script.strip())
        
        if filtered_scripts:
            extra_js = '<script>\n' + '\n'.join(filtered_scripts) + '\n</script>'
    
    # Create new template
    new_content = '''{% extends "base_navbar.html" %}

{% block title %}''' + title + '''{% endblock %}

{% block extra_css %}
''' + extra_css + '''
{% endblock %}

{% block content %}
''' + main_content + '''
{% endblock %}

{% block extra_js %}
''' + extra_js + '''
{% endblock %}'''
    
    return True, new_content

def extract_main_content(content):
    """Extract the main content from various template patterns"""
    
    # Pattern 1: Look for main content area after sidebar
    patterns = [
        r'<!-- Main.*?-->\s*<div class="col-md-(?:9|10)[^>]*>(.*?)(?:</div>\s*){2,3}(?:</body>|$)',
        r'<div class="col-md-(?:9|10)[^>]*>(.*?)(?:</div>\s*){2,3}(?:</body>|$)',
        r'<!-- Main Form Area -->\s*<div class="col-md-10[^>]*>(.*?)(?:</div>\s*){2,3}(?:</body>|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            main_content = match.group(1).strip()
            # Clean up the content
            main_content = clean_main_content(main_content)
            return main_content
    
    # Fallback: extract body content and remove sidebar
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        # Remove sidebar
        sidebar_pattern = r'<div class="col-md-[23][^>]*sidebar[^>]*>.*?</div>'
        body_content = re.sub(sidebar_pattern, '', body_content, flags=re.DOTALL)
        # Remove container-fluid wrapper
        body_content = re.sub(r'<div class="container-fluid">\s*<div class="row">', '', body_content)
        body_content = re.sub(r'</div>\s*</div>\s*$', '', body_content)
        return clean_main_content(body_content)
    
    return "<!-- Content extraction failed -->"

def clean_main_content(content):
    """Clean up extracted main content"""
    # Remove extra Bootstrap and jQuery script tags
    content = re.sub(r'<script[^>]*src="[^"]*bootstrap[^"]*"[^>]*></script>', '', content)
    content = re.sub(r'<script[^>]*src="[^"]*jquery[^"]*"[^>]*></script>', '', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = content.strip()
    
    return content

def main():
    template_dir = r"c:\Users\A_R\Desktop\Brighway Site\website\bri\templates"
    html_files = glob.glob(os.path.join(template_dir, "*.html"))
    
    print("Converting all templates to use base_navbar.html...")
    print("=" * 60)
    
    converted = 0
    skipped = 0
    errors = 0
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        
        try:
            success, result = convert_template(file_path)
            
            if success:
                # Create backup
                backup_path = file_path + '.backup'
                if not os.path.exists(backup_path):
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
                print(f"- {result}")
                skipped += 1
                
        except Exception as e:
            print(f"✗ Error converting {filename}: {e}")
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"✓ Converted: {converted}")
    print(f"- Skipped: {skipped}")
    print(f"✗ Errors: {errors}")
    print(f"\nBackup files created with .backup extension")
    print(f"All templates now extend base_navbar.html with centralized navigation!")

if __name__ == "__main__":
    main()