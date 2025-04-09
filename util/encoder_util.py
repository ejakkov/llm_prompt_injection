import base64

def encode_to_base64(text: str) -> str:
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')