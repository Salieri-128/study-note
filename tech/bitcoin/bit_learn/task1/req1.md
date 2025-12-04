太棒了！看完前 5 节，意味着你对哈希函数、时间戳服务器、工作量证明（PoW）以及最长链原则已经在理论上闭环了。

现在，我们把这些理论变成代码。

这是你的第一个编程作业 Project Genesis。我不只要你写出来，我要求你按照 OJ (Online Judge) 的标准格式来完成。这意味着你的输出必须严格符合要求，逻辑必须通过特定的测试用例。

🏛️ Assignment 01: Build a Minimal PoW Blockchain
难度： ⭐⭐ 涉及知识点： SHA-256 哈希、链式结构、Nonce 爆破（挖矿） 语言限制： Python (仅允许使用标准库 hashlib, datetime, json)

📝 题目描述 (Problem Description)
你需要构建一个最简化的区块链系统。这个系统包含两个核心类：Block (区块) 和 Blockchain (区块链)。 每一块区块必须包含：

索引 (Index): 区块在链中的位置（创世块为 0）。

时间戳 (Timestamp): 区块生成的时间（Unix 时间戳）。

数据 (Data): 字符串形式的交易数据。

前哈希 (Previous Hash): 前一个区块的哈希值。

Nonce: 用于工作量证明的随机数。

哈希 (Hash): 当前区块的哈希值。

核心挑战 (Mining)： 在将区块加入链之前，你必须进行工作量证明。给定一个难度值 difficulty（整数 n），你必须找到一个 Nonce，使得该区块的 SHA-256 哈希值以 n 个 0 开头。

📥 输入格式 (Input)
你的程序不需要从控制台读取输入，但在测试时，我会给你一组数据。你需要手动将这些数据“喂”给你的代码。 测试数据包含：

难度值 (difficulty): 例如 4 (哈希必须以 0000 开头)。

交易数据列表: 例如 ["Alice pays Bob 10 BTC", "Bob pays Charlie 5 BTC"]。

📤 输出格式 (Output)
对于每一个成功挖出的区块，打印 JSON 格式的区块详情。 最后，打印验证结果：Chain Valid: True/False。

期望输出样例：

Plaintext

Mining block 1...
Block mined: 0000a1b2... (Nonce: 12345)
{
  "index": 1,
  "timestamp": 1678888888,
  "data": "Alice pays Bob 10 BTC",
  "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "nonce": 12345,
  "hash": "0000a1b2c3..."
}
...
Chain Valid: True
💻 代码框架 (Starter Code)
我已经为你写好了骨架，你需要填补标有 TODO 的部分。不要修改类结构，只填写逻辑。

Python

import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        TODO: 1. 将区块的属性 (index, timestamp, data, previous_hash, nonce) 拼接成一个字符串。
              2. 为了保证一致性，建议直接转换成字符串拼接，例如:
                 str(self.index) + str(self.timestamp) + self.data + self.previous_hash + str(self.nonce)
              3. 返回该字符串的 SHA-256 哈希值 (十六进制字符串)。
        """
        # Your code here
        pass

    def mine_block(self, difficulty):
        """
        TODO: 实现工作量证明 (PoW)。
              1. 不断增加 self.nonce 的值。
              2. 每次增加后重新计算 self.hash。
              3. 直到 self.hash 的前缀包含 'difficulty' 个 '0'。
              4. 打印挖矿成功信息。
        """
        target = '0' * difficulty
        # Your code here
        pass

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # 默认难度 4

    def create_genesis_block(self):
        # 创世区块：Index=0, PreHash="0"*64
        return Block(0, time.time(), "Genesis Block", "0"*64)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        # 链接到前一个区块
        new_block.previous_hash = self.get_latest_block().hash
        # 挖矿
        new_block.mine_block(self.difficulty)
        # 加入链
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        TODO: 验证整条链的完整性。
              1. 遍历链中除了创世块以外的所有区块。
              2. 检查 block.hash 是否等于 calculate_hash() (防止数据被篡改)。
              3. 检查 block.previous_hash 是否等于前一个区块的 hash (防止断链)。
              4. 如果有问题返回 False，没问题返回 True。
        """
        # Your code here
        return True

# --- 测试用例 (Test Runner) ---
# 不要修改下面的运行逻辑，你可以修改 my_blockchain.difficulty 来体验挖矿速度的变化

if __name__ == "__main__":
    my_blockchain = Blockchain()
    my_blockchain.difficulty = 4 # 试着改成 5 或 6，看看速度会慢多少

    print("--- Starting Mining ---")
    
    # 模拟添加两个区块
    print("Mining block 1...")
    my_blockchain.add_block(Block(1, time.time(), "Alice pays Bob 10 BTC", ""))
    
    print("Mining block 2...")
    my_blockchain.add_block(Block(2, time.time(), "Bob pays Charlie 5 BTC", ""))

    # 打印结果
    for block in my_blockchain.chain:
        print(json.dumps(block.__dict__, indent=2))

    # 验证链
    print(f"Is blockchain valid? {my_blockchain.is_chain_valid()}")

    # 尝试篡改数据测试 (Optional Challenge)
    # print("Tampering with blockchain...")
    # my_blockchain.chain[1].data = "Alice pays Bob 10000 BTC"
    # print(f"Is blockchain valid after tamper? {my_blockchain.is_chain_valid()}")
🧑‍🏫 老师的批改标准 (Checklist)
当你完成后，请把代码发给我（或者你自己运行），你需要检查：

哈希一致性： 你的 calculate_hash 必须包含 nonce。如果不包含，挖矿时哈希值永远不会变，你的循环会死锁。

挖矿逻辑： 当难度设为 4 时，输出的 Hash 真的以 0000 开头吗？

链的链接： 第二个区块的 previous_hash 真的等于第一个区块的 hash 吗？

防篡改验证： 如果你取消注释最后那段“篡改代码”，is_chain_valid 应该返回 False。

现在，打开你的 IDE (VS Code / PyCharm)，开始你的 Genesis 之旅吧！遇到 hashlib 报错或者死循环随时问我。