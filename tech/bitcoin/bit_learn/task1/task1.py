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
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

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
        while self.hash[:difficulty] != target or self.hash[difficulty]==0 :##要求一定是只有前四位是0，如果有超过四位是0也不算
            self.nonce += 1
            self.hash = self.calculate_hash()
        if self.index!= 0:
            print(f"Block mined: {self.hash}")
        return self.hash

        

class Blockchain:
    def __init__(self):
        self.difficulty = 4  # 默认难度 4
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # 创世区块：Index=0, PreHash="0"*64
        genesis_block = Block(0, time.time(), "Genesis Block", "0"*64)
        genesis_block.mine_block(self.difficulty)  # 挖创世区块
        return genesis_block

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
              1. 遍历链中所有区块。
              2. 检查 block.hash 是否等于 calculate_hash() (防止数据被篡改)。
              3. 检查 block.previous_hash 是否等于前一个区块的 hash (防止断链)。
              4. 如果有问题返回 False，没问题返回 True。
        """
        # Your code here
        for i in range(0, len(self.chain)):
            if i == 0:
                continue
            block = self.chain[i]
            if block.hash != block.calculate_hash():
                return False
            if block.previous_hash != self.chain[i-1].hash:
                return False
        return True

# --- 测试用例 (Test Runner) ---
# 不要修改下面的运行逻辑，你可以修改 my_blockchain.difficulty 来体验挖矿速度的变化

def operation_mining(Blockchain,data):
    if my_blockchain.is_chain_valid():
            new_block = Block(len(my_blockchain.chain),time.time(),data,my_blockchain.get_latest_block().hash)
            my_blockchain.add_block(new_block)
            return True
    else:
        print("this blockchain has been tamperred")##因为是单人，其实不会人改你东西
        return False


if __name__ == "__main__":
    my_blockchain = Blockchain()
    my_blockchain.difficulty = 4 # 试着改成 5 或 6，看看速度会慢多少
    print("--- 交互式区块链挖矿程序 ---")
    
    while True:
        operation=input("请输入你想要进行的操作:\n'1:进入挖矿'\n'2:查看特定区块内容\n'3:退出'")
        ##挖矿区块
        if operation == '1':
            while True:
                data=input("请输入你想要储存的数据('输入exit退出')")
                if data == 'exit':
                    break
                else:
                    operation_mining(my_blockchain,data)
        
        ##查看区块
        if operation == '2':
            while True:
                print("当前区块链长度为:",len(my_blockchain.chain),"(从0开始计数)")
                number_check=input("请输入你想要查看的区块链数字('输入exit退出')")
                if number_check == 'exit':
                    break
                number_check=int(number_check)
                if number_check < len(my_blockchain.chain):
                    print(json.dumps(my_blockchain.chain[number_check].__dict__,indent=1))
                else:
                    print("输入有误，请重新输入")
                    continue

        ##退出        
        if operation == '3':
            print("退出成功，所有数据消失了，因为我没做存储功能")
            break
        else:
            print("输入有误，请重新输入")
            continue