"""加密模块"""
import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoManager:
    """
    加盐加密方案：
    1. 生成随机盐 salt（16 字节）
    2. PBKDF2(salt + master_password, iterations=100000, sha256) → 256位密钥
    3. AES-256-GCM 加密
    4. 存储：base64(salt + nonce + ciphertext + tag)
    """

    def encrypt(self, plaintext, master_password):
        """加盐加密"""
        salt = os.urandom(16)
        key = self._derive_key(salt, master_password)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        # salt(16) + nonce(12) + ciphertext+tag
        return base64.b64encode(salt + nonce + ciphertext).decode('ascii')

    def decrypt(self, ciphertext_b64, master_password):
        """解密"""
        raw = base64.b64decode(ciphertext_b64)
        salt = raw[:16]
        nonce = raw[16:28]
        ciphertext = raw[28:]
        key = self._derive_key(salt, master_password)
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

    def hash_master_password(self, master_password):
        """生成主密码验证哈希"""
        salt = os.urandom(16)
        key = self._derive_key(salt, master_password)
        return base64.b64encode(salt + key).decode('ascii')

    def verify_master_password(self, password, hash_value):
        """验证主密码"""
        raw = base64.b64decode(hash_value)
        salt = raw[:16]
        stored_key = raw[16:]
        key = self._derive_key(salt, password)
        return key == stored_key

    def _derive_key(self, salt, password):
        """PBKDF2 派生密钥"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode('utf-8'))
