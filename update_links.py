import re

file_path = '/Users/flavio/Documents/trae_projects/teco_app/index.html'

with open(file_path, 'r') as f:
    content = f.read()

# 1. Remove the old footer section
old_footer_pattern = r'<div class="d-flex flex-column justify-content-center pb-2 order-2">[\s\S]*?Accessibility</a>\s*</div>\s*</div>'
content = re.sub(old_footer_pattern, '', content)

# 2. Remove eGainChatWrapper
egain_pattern = r'<div id="eGainChatWrapper"[\s\S]*?</div>'
content = re.sub(egain_pattern, '', content)

# 3. Replace blue border with custom gray shadow block
content = content.replace('border border-primary', 'custom-gray-shadow-block')

# 4. Update all links
def replace_link(match):
    tag = match.group(0)
    href_match = re.search(r'href=["\'](.*?)["\']', tag)
    
    if href_match:
        url = href_match.group(1)
        if 'TECO.pdf' in url:
            return tag
        else:
            return re.sub(r'href=["\'].*?["\']', 'href="javascript:void(0)"', tag)
    return tag

link_pattern = r'<a\s+[^>]*?>'
content = re.sub(link_pattern, replace_link, content)

# 5. Remove Settings Column
# Locate the SettingsSection div
settings_marker = 'id="SettingsSection"'
settings_index = content.find(settings_marker)

if settings_index != -1:
    # Search backwards for the opening container div
    # The container is: <div class="col-lg-3 d-flex flex-column mt-2 mt-lg-0">
    container_start_tag = '<div class="col-lg-3 d-flex flex-column mt-2 mt-lg-0">'
    start_index = content.rfind(container_start_tag, 0, settings_index)
    
    if start_index != -1:
        # Now find the matching closing div
        # We start counting from the start_index
        
        # Find where the tag ends
        tag_end = content.find('>', start_index) + 1
        
        current_pos = tag_end
        open_divs = 1
        
        while open_divs > 0 and current_pos < len(content):
            # Find next open or close div
            next_div_open = content.find('<div', current_pos)
            next_div_close = content.find('</div>', current_pos)
            
            if next_div_close == -1:
                break # Should not happen if HTML is valid
                
            # We must check which one comes first
            if next_div_open != -1 and next_div_open < next_div_close:
                open_divs += 1
                # Advance past this tag
                current_pos = content.find('>', next_div_open) + 1
            else:
                open_divs -= 1
                current_pos = next_div_close + 6 # length of </div>
        
        if open_divs == 0:
            # We found the end
            end_index = current_pos
            # Remove the block
            print(f"Removing Settings block from {start_index} to {end_index}")
            content = content[:start_index] + content[end_index:]
        else:
            print("Could not find matching closing div for Settings block")
    else:
        print("Could not find container div for Settings block")
else:
    print("Could not find SettingsSection")

with open(file_path, 'w') as f:
    f.write(content)

print("Successfully updated index.html")
