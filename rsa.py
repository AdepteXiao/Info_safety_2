import json
import os

from utils import miller_rabin, ferma, nod, mod_inverse
import random
from gmpy2 import powmod

FILES_FOLDER = "files\\"
KEYS_FOLDER = FILES_FOLDER + "keys\\"
ENC_FOLDER = FILES_FOLDER + "encrypted\\"
DEC_FOLDER = FILES_FOLDER + "decrypted\\"


class RSA:
    def __init__(self, num: int = 28):
        self.s, self.N, self.e = self.get_keys()
        self.num = num
        self.make_folders(
            FILES_FOLDER,
            KEYS_FOLDER,
            ENC_FOLDER,
            DEC_FOLDER
        )

    @staticmethod
    def make_folders(*folders):
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

    @staticmethod
    def find_prime(lb: int, rb: int, tests_k: int) -> int:
        while True:
            num = random.randint(lb, rb)
            miller_rabin_verdict = miller_rabin(num, tests_k)
            ferma_verdict = ferma(num, tests_k)
            if miller_rabin_verdict and ferma_verdict:
                return num

    @staticmethod
    def get_keys():
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

    def save_keys(self, filename: str) -> None:
        key_data = {
            "N": self.N,
            "e": self.e,
            "s": self.s
        }

        with open(filename, 'w') as key_file:
            json.dump(key_data, key_file, indent=4)

    def load_keys(self, filename: str) -> None:
        with open(filename, 'r') as key_file:
            key_data = json.load(key_file)
        self.N = key_data["N"]
        self.e = key_data["e"]
        self.s = key_data["s"]

    def enc_dec_factory(self):
        return Encrypter(self.s, self.N), Decrypter(self.e, self.N)


class Encrypter:
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
            last_block = data[num_blocks * self.block_len:] + bytes([0] * zero_num)
            blocks.append(last_block)
        return blocks, zero_num

    def encrypt(self, data):
        res = []
        nums = []
        blocks, zero_num = self.split_into_blocks(data)
        for block in blocks:
            block = int.from_bytes(block, byteorder="big")
            nums.append(int(powmod(block, self.s, self.N)))
        block_len = (len(format(max(nums), 'b'))) // 8 + 1
        for num in nums:
            res.append(num.to_bytes(block_len, byteorder="big"))
        res.insert(0, block_len.to_bytes(1, byteorder="big"))
        res.insert(1, zero_num.to_bytes(1, byteorder="big"))
        return b''.join(res)
        # return res


class Decrypter:
    def __init__(self, e, N):
        self.e = e
        self.N = N
        self.block_len = 1
        self.zero_num = 0
        self.n_len = (len(format(self.N, 'b'))) // 8 - 1

    def decrypt(self, data):
        res = []
        self.block_len = data[0]
        self.zero_num = data[1]
        data = data[2:]
        blocks = [data[i * self.block_len: (i + 1) * self.block_len] for i in
                  range(len(data) // self.block_len)]
        for block in blocks:
            block = int.from_bytes(block, byteorder="big")
            res.append(int(powmod(block, self.e, self.N))
                       .to_bytes(self.n_len, byteorder="big"))
        res = b''.join(res)
        res = res[:-self.zero_num]
        return res


if __name__ == '__main__':
    rsa = RSA()
    rsa.load_keys(KEYS_FOLDER + "keys.json")
    encr, decr = rsa.enc_dec_factory()

    with open(FILES_FOLDER + "test.txt", "rb") as file:
        file_bytes = file.read()

    enc = encr.encrypt(file_bytes)
    print(enc)
    dec = decr.decrypt(enc)
    with open(FILES_FOLDER + "res.txt", "wb") as file:
        file.write(dec)
