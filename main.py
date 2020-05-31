import math


def get_address(address):
    total = 0
    t = 4
    for i in address:
        total += int(i, 16) * math.pow(16, t)
        t = t - 1
    return int(total)


def output1(a, size, asc, bs, wp, ap):
    print("***CACHE SETTINGS***")
    if a == '0':
        print("Unified I- D-cache")
    else:
        print("Split I- D-cache")
    print("Size:", size)
    print("Associativity:", asc)
    print("Block size:", bs)
    if wp == 'wb':
        print("Write policy: WRITE BACK")
    else:
        print("Write policy: WRITE THOROUGH")
    if ap == "wa":
        print("Allocation policy: WRITE ALLOCATE")
    else:
        print("Allocation policy: NO WRITE ALLOCATE")
    print()


def output2(acs, miss, replace, iacs, imiss, ireplace, word):
    print("***CACHE STATISTICS***")
    print("INSTRUCTIONS")
    print("accesses:", iacs)
    print("misses:", imiss)
    if iacs != 0:
        i_miss_rate = round((imiss/iacs), 4)
        print("miss rate: %.4f" % i_miss_rate, "(hit rate %.4f)" % (1 - i_miss_rate))
    if iacs == 0:
        print("miss rate: 0.0000 (hit rate 0.0000)")
    print("replace:", ireplace)
    print("DATA")
    print("accesses:", acs)
    print("misses:", miss)
    if acs != 0:
        d_miss_rate = round((miss/acs), 4)
        print("miss rate: %.4f" % d_miss_rate, "(hit rate %.4f)" % (1 - d_miss_rate))
    else:
        print("miss rate:", 0.0000, "(hit rate 0.0000)")
    # print("miss rate: %.4f" % d_miss_rate, "(hit rate %.4f)" % (1 - d_miss_rate))
    print("replace:", replace)
    print("TRAFFIC (in words)")
    print("demand fetch:", int((imiss+miss) * word), "\ncopies back: 0")


def creating_cache(w, h):
    c = [['x' for x in range(w)] for y in range(h)]
    return c


def direct_mapped(info, csize):
    i_miss = 0
    i_hit = 0
    d_hit = 0
    d_miss = 0
    i_replace = 0
    i_access = 0
    d_access = 0
    d_replace = 0
    block_size = int(info[0])
    words = block_size / 4
    cache_rows = int(csize / block_size)
    cache = creating_cache(2, cache_rows)
    inp = input()
    while inp != "":
        request = inp.split()
        tag = int(get_address(request[1]) / 16)
        # print(tag)
        block = int(tag % 16)
        if cache[block][0] == tag:
            # print("hit")
            if request[0] == '0':
                d_hit += 1
                d_access += 1
            elif request[0] == '2':
                i_hit += 1
                i_access += 1
        else:
            if cache[block][0] != 'x':
                if request[0] == '0':
                    d_replace += 1
                    # d_access += 1
                elif request[0] == '2':
                    i_replace += 1
                    # i_access += 1
            cache[block][0] = tag
            cache[block][1] = 'a'
            # print("miss")
            if request[0] == '0':
                d_miss += 1
                # d_access += 1
            elif request[0] == '2':
                i_miss += 1
                # i_access += 1
        # if request[0] == '0':
        #     # d_access += 1
        # elif request[0] == '2':
        #     i_access += 1
        inp = input()
        if inp == "":
            break
    output1(cache_info[2], cache_size, int(cache_info[4]), block_size, cache_info[6], cache_info[8])
    output2(d_hit + d_miss, d_miss, d_replace, i_miss + i_hit, i_miss, i_replace, words)
    # print(*cache)


def associative_cache(info, c_size, associativity_no):
    i_miss = 0
    i_hit = 0
    d_hit = 0
    d_miss = 0
    i_replace = 0
    i_access = 0
    d_access = 0
    d_replace = 0
    blocksize = int(info[0])
    words = blocksize / 4
    set_no = int(c_size / (blocksize * associativity_no))
    cache = creating_cache(associativity_no, set_no)
    # print(*cache)
    lru = []
    for i in range(set_no):
        temp = []
        lru.append(temp)
    inp = input()
    while inp != "":
        request = inp.split()
        tag = int(get_address(request[1]) / block_size)
        set_address = int(tag % set_no)
        if str(tag) in cache[set_address]:
            for i in lru[set_address][:]:
                for i in lru[set_address][:]:
                    if i == str(tag):
                        lru[set_address].remove(i)
        # lru[set_address].remove(str(tag))
            lru.append(str(tag))
            # print("hit")
            if request[0] == '0':
                d_hit += 1
            elif request[0] == '2':
                i_hit += 1
            # print(*lru[set_address])
        else:
            if len(lru[set_address]) < associativity_no:
                lru[set_address].append(str(tag))
                y = cache[set_address].index('x')
                cache[set_address][y] = str(tag)
                # print("miss")
                if request[0] == '0':
                    d_miss += 1
                elif request[0] == '2':
                    i_miss += 1
            else:
                lru[set_address].pop(0)
                lru[set_address].append(str(tag))
                # print("miss")
                if request[0] == '0':
                    d_miss += 1
                    d_replace += 1
                elif request[0] == '2':
                    i_miss += 1
                    i_replace += 1
        inp = input()
    output1(cache_info[2], cache_size, int(cache_info[4]), block_size, cache_info[6], cache_info[8])
    output2(d_hit + d_miss, d_miss, d_replace, i_miss + i_hit, i_miss, i_replace, words)


input1 = input()
cache_size = int(input())
cache_info = input1.split()
block_size = int(cache_info[0])
associativity = int(cache_info[4])
split = int(cache_info[2])
if associativity == 1:
    direct_mapped(cache_info, cache_size)
else:
    associative_cache(cache_info, cache_size, associativity)



# output1(cache_info[2], cache_size, int(cache_info[4]), block_size, cache_info[6], cache_info[8])
# output2(D_access-1, D_miss, D_hit, D_replace)



