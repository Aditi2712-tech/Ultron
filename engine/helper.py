import re

def extract_yt_term(command):
    #reg exp pattern to capture search term
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    #use re.search to find match in command
    match = re.search(pattern, command, re.IGNORECASE)
    #if match found, return extracted search term, or return home
    return match.group(1) if match else None