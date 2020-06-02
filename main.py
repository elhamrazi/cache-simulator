import math


def get_address(address):
    total = 0
    t = len(address) - 1
    for i in address:
        total += int(i, 16) * math.pow(16, t)
        t = t - 1
    return int(total)


def output1(a, size, asc, bs, wp, ap):
    print("***CACHE SETTINGS***")
    if a == '0':
        print("Unified I- D-cache")
        print("Size:", size)

    else:
        print("Split I- D-cache")
        print("I-cache size:", int(size[0]))
        print("D-cache size:", int(size[2]))
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


def output2(acs, miss, replace, iacs, imiss, ireplace, word, copies):
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
    print("demand fetch:", int((imiss+miss) * word), "\ncopies back:", int(word * copies))


def creating_cache(w, h):
    c = [['x' for x in range(w)] for y in range(h)]
    return c


def check_lru(lru, tag):
    for i in lru:
        if tag in i:
            return True
    return False


def unified_cache(info, c_size, associativity_no):
    i_miss = 0
    i_hit = 0
    d_hit = 0
    d_miss = 0
    i_replace = 0
    d_replace = 0
    copy_back = 0
    blocksize = int(info[0])
    words = blocksize / 4
    set_no = int(c_size / (blocksize * associativity_no))
    cache = creating_cache(associativity_no, set_no)
    # print(*cache)
    lru = []
    for k in range(set_no):
        temp = []
        lru.append(temp)
    inp = input()
    while inp != "":
        request = inp.split()
        tag = int(get_address(request[1]) / block_size)
        set_address = int(tag % set_no)
        d = 'x'
        if check_lru(lru[set_address], str(tag)):
            for i in lru[set_address][:]:
                for i in lru[set_address][:]:
                    if str(tag) in i:
                        d = i.get(str(tag))
                        lru[set_address].remove(i)
                        if request[0] == '1':
                            d = 'd'
            lru[set_address].append({str(tag): d})
            # print("hit")
            if request[0] == '0' or request[0] == '1':
                d_hit += 1
            elif request[0] == '2':
                i_hit += 1
            # print(lru)
        else:
            cell = {str(tag): 'c'}
            if len(lru[set_address]) < associativity_no:
                if request[0] == '1':
                    lru[set_address].append({str(tag): 'd'})
                else:
                    lru[set_address].append(cell)
                # print("miss")
                if request[0] == '0' or request[0] == '1':
                    d_miss += 1
                elif request[0] == '2':
                    i_miss += 1
                # print(lru)
            else:
                t = lru[set_address].pop(0)
                li = list(t.values())
                if li[0] == 'd':
                    copy_back += 1
                if request[0] == '1':
                    lru[set_address].append({str(tag): 'd'})
                else:
                    lru[set_address].append(cell)
                # print("miss")
                if request[0] == '0' or request[0] == '1':
                    d_miss += 1
                    d_replace += 1
                elif request[0] == '2':
                    i_miss += 1
                    i_replace += 1
                # print(lru)
        inp = input()
    # print(*lru)
    for i in lru:
        for j in i:
            l = list(j.values())
            copy_back += l.count('d')
    output1(cache_info[2], cache_size, int(cache_info[4]), block_size, cache_info[6], cache_info[8])
    output2(d_hit + d_miss, d_miss, d_replace, i_miss + i_hit, i_miss, i_replace, words, copy_back)


def split_cache(info, c_size, associativity_no):
    i_miss = 0
    i_hit = 0
    d_hit = 0
    d_miss = 0
    i_replace = 0
    d_replace = 0
    copy_back = 0
    blocksize = int(info[0])
    words = blocksize / 4
    set_no1 = int(int(c_size[2]) / (blocksize * associativity_no))
    set_no2 = int(int(c_size[0]) / (blocksize * associativity_no))
    lru1 = []
    lru2 = []
    for k in range(set_no1):
        temp = []
        lru1.append(temp)
    for k in range(set_no2):
        temp = []
        lru2.append(temp)
    inp = input()
    while inp != "":
        request = inp.split()
        if request[0] == '0' or request[0] == '1':
            tag = int(get_address(request[1]) / block_size)
            set_address = int(tag % set_no1)
            # if str(tag) in lru1[set_address]:
            #     for i in lru1[set_address][:]:
            #         for i in lru1[set_address][:]:
            #             if i == str(tag):
            #                 lru1[set_address].remove(i)
            #     # lru[set_address].remove(str(tag))
            #     lru1[set_address].append(str(tag))
            #     # print("hit")
            #     d_hit += 1
            #     # print(lru1[set_address])
            # else:
            #     if len(lru1[set_address]) < associativity_no:
            #         lru1[set_address].append(str(tag))
            #         # print("miss1")
            #         d_miss += 1
            #         # print(lru1[set_address])
            #     else:
            #         lru1[set_address].pop(0)
            #         lru1[set_address].append(str(tag))
            #         # print("miss2")
            #         d_miss += 1
            #         d_replace += 1
            #         # print(lru1[set_address])
            d = 'x'
            if check_lru(lru1[set_address], str(tag)):
                for i in lru1[set_address][:]:
                    for i in lru1[set_address][:]:
                        if str(tag) in i:
                            d = i.get(str(tag))
                            lru1[set_address].remove(i)
                            if request[0] == '1':
                                d = 'd'
                lru1[set_address].append({str(tag): d})
                # print("hit")
                if request[0] == '0' or request[0] == '1':
                    d_hit += 1
                # print(lru)
            else:
                cell = {str(tag): 'c'}
                if len(lru1[set_address]) < associativity_no:
                    if request[0] == '1':
                        lru1[set_address].append({str(tag): 'd'})
                    else:
                        lru1[set_address].append(cell)
                    # print("miss")
                    if request[0] == '0' or request[0] == '1':
                        d_miss += 1
                    # print(lru)
                else:
                    t = lru1[set_address].pop(0)
                    li = list(t.values())
                    if li[0] == 'd':
                        copy_back += 1
                    if request[0] == '1':
                        lru1[set_address].append({str(tag): 'd'})
                    else:
                        lru1[set_address].append(cell)
                    # print("miss")
                    if request[0] == '0' or request[0] == '1':
                        d_miss += 1
                        d_replace += 1
                    # print(lru)
        elif request[0] == '2':
            tag = int(get_address(request[1]) / block_size)
            set_address = int(tag % set_no2)
            if str(tag) in lru2[set_address]:
                for i in lru2[set_address][:]:
                    for i in lru2[set_address][:]:
                        if i == str(tag):
                            lru2[set_address].remove(i)
                # lru[set_address].remove(str(tag))
                lru2[set_address].append(str(tag))
                # print("hit")
                i_hit += 1
            else:
                if len(lru2[set_address]) < associativity_no:
                    lru2[set_address].append(str(tag))
                    # print("miss1")
                    i_miss += 1
                    # print(lru[set_address])
                else:
                    lru2[set_address].pop(0)
                    lru2[set_address].append(str(tag))
                    # print("miss2")
                    i_miss += 1
                    i_replace += 1
                    # print(lru[set_address])
        inp = input()
    for i in lru1:
        for j in i:
            l = list(j.values())
            copy_back += l.count('d')
    output1(cache_info[2], c_size, int(cache_info[4]), block_size, cache_info[6], cache_info[8])
    output2(d_hit + d_miss, d_miss, d_replace, i_miss + i_hit, i_miss, i_replace, words, copy_back)


input1 = input()
cache_size = input()
cache_split = cache_size.split()
cache_info = input1.split()
block_size = int(cache_info[0])
associativity = int(cache_info[4])
split = int(cache_info[2])
# if associativity == 1:
#     direct_mapped(cache_info, cache_size)
# else:
if len(cache_split) == 1:
    unified_cache(cache_info, int(cache_split[0]), associativity)
else:
    split_cache(cache_info, cache_split, associativity)





