import hashlib
import json
import time
import binascii
# 需要安装: pip install ecdsa
from ecdsa import SigningKey, VerifyingKey, SECP256k1 

class Wallet:
    def __init__(self):
        """
        初始化钱包，生成一对公私钥。
        使用 SECP256k1 曲线 (比特币同款)。
        """
        self._private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self._private_key.verifying_key

    def sign_data(self, data_string):
        """
        TODO: 使用私钥对字符串数据进行签名。
        1. 将 data_string 编码为 bytes。
        2. 使用 self._private_key.sign() 生成签名。
        3. 返回 hex 格式的签名字符串 (binascii.hexlify)。
        """
        data_code=data_string.encode()
        signature=self._private_key.sign(data_code)
        return binascii.hexlify(signature).decode()


    def get_public_key_str(self):
        """辅助函数：将公钥对象转换为 hex 字符串，方便传输"""
        return binascii.hexlify(self.public_key.to_string()).decode()


class Transaction:
    def __init__(self, sender_pub_key_str, recipient_pub_key_str, amount):
        self.sender = sender_pub_key_str      # 发送者公钥 (字符串)
        self.recipient = recipient_pub_key_str # 接收者公钥 (字符串)
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None # 签名初始为空，需要调用 sign_transaction 填充

    def calculate_hash(self):
        """
        计算交易内容的哈希（不包含签名本身），用于签名。
        """
        # 注意：这里只包含交易核心数据，不包含 signature
        tx_content = str(self.sender) + str(self.recipient) + str(self.amount) + str(self.timestamp)
        return hashlib.sha256(tx_content.encode()).hexdigest()

    def sign_transaction(self, wallet):
        """
        使用钱包对交易进行签名。
        """
        if wallet.get_public_key_str() != self.sender:
            print("Error: You cannot sign a transaction for another wallet!")
            return False
        
        tx_hash = self.calculate_hash()
        self.signature = wallet.sign_data(tx_hash)
        return True

    def is_valid(self):
        """
        TODO: 验证交易签名的有效性。
        这是矿工节点要做的核心工作。
        
        逻辑步骤:
        1. 如果 sender 是 "System" (挖矿奖励)，直接返回 True。
        2. 如果没有 signature，返回 False。
        3. 重建 VerifyingKey 对象:
           vk = VerifyingKey.from_string(binascii.unhexlify(self.sender), curve=SECP256k1)
        4. 计算交易内容的哈希 (self.calculate_hash())
        5. 使用 vk.verify() 验证签名。
           注意：verify 函数如果验证失败会抛出 BadSignatureError 异常，需要用 try-except 捕获。
           如果验证成功返回 True，抛出异常则返回 False。
        """
        if self.sender == "System": # 挖矿奖励交易
            return True

        if not self.signature:
            return False

        # Your code here (Try-Except block needed)
        try:
            # 1. 还原公钥对象
            vk=VerifyingKey.from_string(binascii.unhexlify(self.sender),curve=SECP256k1)
            # 2. 验证签名
            tx_hash=self.calculate_hash()
            vk.verify(binascii.unhexlify(self.signature),tx_hash.encode())
        except: 
            return False
        return True

# --- 测试脚本 (Test Runner) ---
if __name__ == "__main__":
    # 1. 创建两个钱包：Alice 和 Bob
    alice_wallet = Wallet()
    bob_wallet = Wallet()
    print(f"Alice's Public Key: {alice_wallet.get_public_key_str()[:20]}...")
    print(f"Bob's Public Key: {bob_wallet.get_public_key_str()[:20]}...")

    # 2. Alice 创建一笔转账给 Bob 的交易 (10 BTC)
    tx1 = Transaction(alice_wallet.get_public_key_str(), bob_wallet.get_public_key_str(), 10)
    
    # 3. Alice 用自己的私钥签名
    print("\nSigning transaction...")
    tx1.sign_transaction(alice_wallet)
    print(f"Signature: {tx1.signature[:20]}...")

    # 4. 验证交易是否合法
    print(f"\nIs transaction valid? {tx1.is_valid()}") # 应该输出 True

    # 5. 【黑客攻击测试】
    # Eve 试图篡改交易金额，把 10 改成 100
    print("\n--- Tampering Attack ---")
    tx1.amount = 100 
    print(f"Eve changed amount to 100. Is transaction valid now? {tx1.is_valid()}") # 应该输出 False
    # 为什么？因为数据变了，calculate_hash() 变了，但签名是针对原哈希的，所以对不上。

    # 这里展示的原理是，当交易发生的时候，会先把交易内容先hash出来，然后对这串hash值签名，得到一个签名。
    # 验证的时候，会先从sender的publickey还原出一个中介vk，然后利用vk的函数，将电子签名和当前交易内容的hash进行对比，电子签名里包含有签名时的交易的信息，如果对不上就说明内容被篡改