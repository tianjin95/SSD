
from ssd import ssd
from random import randint

num_die = 8
num_block = 8
num_page = 1024

disk0 = ssd(num_die,num_block,num_page)

num_read = randint(0,1000)
num_read_mult = randint(0,1000)
num_erase = randint(0,1000)
num_erase_mult = randint(0,1000)
num_program = randint(0,1000)
num_program_mult = randint(0,1000)

opcnt = [num_read,num_read_mult,num_erase,num_erase_mult,num_program,num_program_mult]
while(1):
    mode = randint(0,5)
    if(opcnt[mode] == 0):
        continue
    if(mode == 0):
        disk0.read(randint(0,num_die-1),randint(0,num_block-1),randint(0,num_page-1))
    elif(mode == 1):
        disk0.read_multi_plane([1 for i in range(num_die)],randint(0,num_block-1),randint(0,num_page-1))
    elif(mode == 2):
        disk0.block_erase(randint(0,num_die-1),randint(0,num_block-1))
    elif(mode == 3):
        disk0.block_erase_multi_plane([1 for i in range(num_die)],randint(0,num_block-1))
    elif(mode == 4):
        data = [0,0,0,[0 for i in range(1024)]]
        disk0.page_program(randint(0,num_die-1),randint(0,num_block-1),randint(0,num_page-1),data)
    else:
        data = [0,0,0,[0 for i in range(1024)]]
        niubi = [data for i in range(num_die)]
        disk0.page_program_multi_plane([1 for i in range(num_die)],randint(0,num_block-1),randint(0,num_page-1),niubi)
    opcnt[mode] -= 1
    flag = 0
    for i in range(6):
        if(opcnt[i] == 0):
            flag += 1
    if(flag == 5):
        break
disk0.report_wear_level_map()