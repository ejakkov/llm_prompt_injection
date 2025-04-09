import re

def sanitize_input(prompt: str) -> str:
    sanitized = re.sub(r'[\n\r\t\\\'\"]', ' ', prompt)  
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()  
    
    return sanitized