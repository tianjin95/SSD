import numpy as np

class ftl:

    def __init__(self, size_ssd, size_die, size_block):
        self.size_ssd = size_ssd
        self.size_die = size_die
        self.size_block = size_block
        self.address_map = np.zeros((size_ssd,size_die,size_block))
        self.bit_map = np.zeros((size_ssd,size_die,size_block))
        