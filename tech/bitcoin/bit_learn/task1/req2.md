🔐 Assignment 02: The Digital Signature & Wallet
难度： ⭐⭐⭐ 涉及知识点： 非对称加密 (ECC - 椭圆曲线加密), 数字签名 (ECDSA), 公钥/私钥, 交易结构。 前置准备： 你需要安装 Python 的 ECDSA 库（比特币用的就是 SECP256k1 曲线）。

Bash

pip install ecdsa
📝 题目描述 (Problem Description)
在 Assignment 01 的基础上，扩充你的区块链系统。你需要实现两个新的组件：

Wallet (钱包): 负责生成公私钥对，并对数据进行签名。

Transaction (交易): 定义交易的数据结构，并包含验证逻辑。

核心逻辑：

私钥 (Private Key): 用于签名 (Sign)。只有你自己知道，绝不示人。

公钥 (Public Key): 用于验证 (Verify)。也是你的钱包地址，公开给全网。

验证规则： 节点收到一笔交易时，会用交易里的公钥去解密签名，如果解出来的哈希值和交易内容的哈希值一致，说明这笔交易确实是私钥持有者发出的。

👨‍🏫 老师的“通关”标准
签名生成 (Sign): 你的代码能生成一串看不懂的十六进制字符串（Signature）。

验签逻辑 (Verify): * 正常签名的交易，is_valid() 返回 True。

篡改测试： 如果你在签名后，手动修改了 tx1.amount 或者 tx1.recipient，is_valid() 必须返回 False。这点最关键！ 这证明了没人能篡改已签名的交易。

异常处理： 你的 is_valid 应该包含 try...except 块，因为 ecdsa 库验证失败时喜欢直接报错（Crash），我们要捕获它并优雅地返回 False。

等你写完这个，我们就把 Transaction 类塞进之前的 Block.data 里（把 data 从字符串变成列表 [tx1, tx2]），那样你就拥有了一个真正的加密货币原型了！