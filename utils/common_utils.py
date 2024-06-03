import base64
import json


def decode_jwt_without_verification(token):
    # JWTs are split into three parts: header, payload, and signature
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT token")

    header = parts[0]
    payload = parts[1]

    # Base64 decode the header and payload
    header_decoded = base64.urlsafe_b64decode(header + '==')
    payload_decoded = base64.urlsafe_b64decode(payload + '==')

    # Convert from bytes to string
    header_str = header_decoded.decode('utf-8')
    payload_str = payload_decoded.decode('utf-8')

    # Convert from string to dictionary
    header_json = json.loads(header_str)
    payload_json = json.loads(payload_str)

    return header_json, payload_json

