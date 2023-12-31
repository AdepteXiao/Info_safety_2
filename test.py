def split_into_blocks(data, block_size):
    num_blocks, remainder = divmod(len(data), block_size)
    blocks = [data[i * block_size: (i + 1) * block_size] for i in range(num_blocks)]
    if remainder > 0:
        last_block = data[num_blocks * block_size:]
        last_block += bytes([0] * (block_size - remainder))
        blocks.append(last_block)

    return blocks


data = b'\x01\x02\x03\x04\x05\x06\x07'
print(data[:-3])
