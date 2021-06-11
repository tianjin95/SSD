import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

life_time = 1000

class page:

    def __init__(self, id):
        self.id = id
        self.meta_pa = int(0xffffffff)
        self.meta_la = int(0xffffffff)
        self.meta_ts = int(0xffffffff)
        self.usr = [0xffffffff for i in range(1024)]
        self.ec = 0
        self.rc = 0

    def erase(self):
        self.meta_pa = 0xffffffff
        self.meta_la = 0xffffffff
        self.meta_ts = 0xffffffff
        for i in range(1024):
            self.usr[i] = 0xffffffff
        self.ec += 1
        self.rc = 0

    def program(self, data):
        self.meta_pa = data[0]
        self.meta_la = data[1]
        self.meta_ts = data[2]
        for i in range(1024):
            self.usr[i] = data[3][i]

    def read(self):
        self.rc += 1
        return [self.meta_pa, self.meta_la, self.meta_ts, self.usr]

class block:

    def __init__(self, id, size_block):
        self.id = id
        self.size_block = size_block
        self.pages = []
        for i in range(size_block):
            self.pages.append(page([id[0], id[1], i]))

    def erase(self):
        for i in range(self.size_block):
            self.pages[i].erase()

class die:
    
    def __init__(self, id, size_die, size_block):
        self.id = id
        self.blocks = []
        for i in range(size_die):
            self.blocks.append(block([id, i], size_block))
        
class ssd:

    def __init__(self, size_ssd, size_die, size_block):
        self.dies = []
        self.size_block = size_block
        self.size_die = size_die
        self.size_ssd = size_ssd
        for i in range(size_ssd):
            self.dies.append(die(i, size_die, size_block))

    def read(self, id_die, id_block, id_page):
        return self.dies[id_die].blocks[id_block].pages[id_page].read()

    def read_multi_plane(self, plane, id_block, id_page):
        result = []
        for i in range(self.size_ssd):
            if(plane[i] == 1):
                result.append(self.dies[i].blocks[id_block].pages[id_page].read())
        return result

    def block_erase(self, id_die, id_block):
        self.dies[id_die].blocks[id_block].erase()

    def block_erase_multi_plane(self, plane, id_block):
        for i in range(self.size_ssd):
            if(plane[i] == 1):
                self.dies[i].blocks[id_block].erase()

    def page_program(self, id_die, id_block, id_page, data):
        self.dies[id_die].blocks[id_block].pages[id_page].program(data)

    def page_program_multi_plane(self, plane, id_block, id_page, data):
        for i in range(self.size_ssd):
            if(plane[i] == 1):
                self.dies[i].blocks[id_block].pages[id_page].program(data[i])

    def report_wear_level_map(self):
        for d in range(self.size_ssd):
            for b in range(self.size_die):
                submap = np.zeros((32,32))
                for x in range(32):
                    for y in range(32):
                        submap[x][y] = self.dies[d].blocks[b].pages[x*32+y].ec / life_time
                if(b == 0):
                    blockmap = submap
                else:
                    blockmap = np.vstack((blockmap, submap))
            if(d == 0):
                diemap = blockmap
            else:
                diemap = np.hstack((diemap, blockmap))
        sns.heatmap(diemap)
        plt.show()