from utils import miller_rabin, ferma, nod, mod_inverse
import random
from gmpy2 import powmod


class RSA:

    def __init__(self, num: int = 32):
        self.s, self.N, self.e = self.get_public_key()
        self.num = num

    @staticmethod
    def find_prime(lb: int, rb: int, tests_k: int) -> int:
        while True:
            num = random.randint(lb, rb)
            miller_rabin_verdict = miller_rabin(num, tests_k)
            ferma_verdict = ferma(num, tests_k)
            if miller_rabin_verdict and ferma_verdict:
                return num

    @staticmethod
    def get_public_key():
        while True:
            P = RSA.find_prime(10 ** 9, 10 ** 10, 10)
            Q = RSA.find_prime(10 ** 17, 10 ** 18, 10)
            if P != Q and 10 ** 27 <= (N := P * Q) < 10 ** 28:
                d = (P - 1) * (Q - 1)
                break
        while True:
            s = random.randint(2, d)
            if nod(s, d) == 1:
                break
        e = mod_inverse(s, d)
        return s, N, e


class Encrypt:
    def __init__(self, s, N):
        self.s = s
        self.N = N
        self.block_len = (len(format(self.N, 'b'))) // 8 - 1

    def split_into_blocks(self, data):
        num_blocks, remainder = divmod(len(data), self.block_len)
        blocks = [data[i * self.block_len: (i + 1) * self.block_len] for i in
                  range(num_blocks)]
        zero_num = self.block_len - remainder
        if remainder > 0:
            last_block = data[num_blocks * self.block_len:]
            last_block += bytes([0] * zero_num)
            blocks.append(last_block)
        return blocks, zero_num

    def transformation(self, data):
        res = []
        nums = []
        in_bytes = data.to_bytes(11, byteorder="big")
        print(in_bytes)
        blocks, zero_num = self.split_into_blocks(in_bytes)
        for block in blocks:
            block = int.from_bytes(block, byteorder="big")
            nums.append(int(powmod(block, self.s, self.N)))
        block_len = (len(format(max(nums), 'b'))) // 8 + 1
        for num in nums:
            res.append(num.to_bytes(block_len, byteorder="big"))
        res.insert(0, block_len.to_bytes(1, byteorder="big"))
        res.insert(1, zero_num.to_bytes(1, byteorder="big"))
        return b''.join(res)


class Decrypt:
    def __init__(self, e, N):
        self.e = e
        self.N = N
        self.block_len = 1
        self.zero_num = 0

    def decrypt(self, data):
        res = []
        self.block_len = int.from_bytes(data[0].to_bytes(1, byteorder='big'), byteorder="big")
        self.zero_num = int.from_bytes(data[1].to_bytes(1, byteorder='big'), byteorder="big")
        data = data[2:]
        print(data)
        blocks = [data[i * self.block_len: (i + 1) * self.block_len] for i in
                  range(len(data) // self.block_len)]
        print(blocks)
        for block in blocks:
            block = int.from_bytes(block, byteorder="big")
            res.append(int(powmod(block, self.e, self.N))
                       .to_bytes(self.block_len, byteorder="big"))
        res = b''.join(res)
        print(res)
        res = res[:-self.zero_num]
        # return int.from_bytes(res, byteorder="big")
        return res

if __name__ == '__main__':
    rsa = RSA()
    encr = Encrypt(rsa.s, rsa.N)
    res = encr.transformation(1298476)
    print(res)
    decr = Decrypt(rsa.e, rsa.N)
    print(decr.decrypt(res))
