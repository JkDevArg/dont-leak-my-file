from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = cipher.iv
        return base64.urlsafe_b64encode(iv + ct_bytes).decode()

    def decrypt(self, enc_data):
        enc_data = base64.urlsafe_b64decode(enc_data)
        iv = enc_data[:AES.block_size]
        ct = enc_data[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()