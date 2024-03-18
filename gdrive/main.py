
import re

def extract_folderid(url):
    pattern = r'/folders/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None
    
url = "https://drive.google.com/drive/folders/1Qlj0feD6CW2RdhSYSVdxhrRNjiUQQL5h"

folder_id = extract_folderid(url)
print(folder_id)