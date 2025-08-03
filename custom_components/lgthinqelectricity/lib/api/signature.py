import hashlib
import hmac
from base64 import b64encode


class Signature:
    @staticmethod
    def calculate_signature(data: str) -> str:
        key = b"c053c2a6ddeb7ad97cb0eed0dcb31cf8"
        hmac_signature = hmac.new(key, data.encode('utf-8'), hashlib.sha1).digest()
        return b64encode(hmac_signature).decode('utf-8')