# pip install pycrypto --user
# pip install pycryptodomex
# post website

from Cryptodome.Cipher import AES
import string, base64


class AESCipher(object):
    def __init__(self, key,iv):
        self.key = key
        self.iv = iv

    def encrypt(self, raw):
        self.cipher = AES.new(self.key, AES.MODE_CFB,self.iv)
        ciphertext = self.cipher.encrypt(raw)
        encoded = base64.b64encode(ciphertext)
        return encoded

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        self.cipher = AES.new(self.key, AES.MODE_CFB,self.iv)
        decrypted = self.cipher.decrypt(decoded)
        return str(decrypted, 'utf-8')



key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = b'OWFJATh1Zowac2xr'

cipher = AESCipher(key, iv)


# plaintext = b'this is a super important message'
# encrypted = cipher.encrypt(plaintext)
# print('Encrypted:', encrypted)
#
# decrypted = cipher.decrypt(encrypted)
# print('Decrypted:', decrypted)
