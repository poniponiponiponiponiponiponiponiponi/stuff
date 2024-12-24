num_kb = { (0, 0): '7', (1, 0): '8', (2, 0): '9', (0, 1): '4', (1, 1): '5',
           (2, 1): '6', (0, 2): '1', (1, 2): '2', (2, 2): '3', (1, 3): '0',
           (2, 3): 'A' }
dir_kb = { (1, 0): 'w', (2, 0): 'A', (0, 1): 'a', (1, 1): 's', (2, 1): 'd' }

def get_cands(kb, from_b, to_b):
    from_coord, to_coord = None, None
    for k, v in kb.items():
        if v == from_b:
            from_coord = k
        if v == to_b:
            to_coord = k
    diff = (to_coord[0] - from_coord[0], to_coord[1] - from_coord[1])
    cands = []
    vertical = ('s' if diff[1] >= 0 else 'w') * abs(diff[1])
    horizontal = ('d' if diff[0] >= 0 else 'a') * abs(diff[0])
    if kb is num_kb:
        if not (from_coord[1] == 3 and to_coord[0] == 0):
            cands.append(horizontal + vertical + 'A')
        if not (from_coord[0] == 0 and to_coord[1] == 3):
            cands.append(vertical + horizontal + 'A')
    if kb is dir_kb:
        if not (from_coord[0] == 0 and to_coord[1] == 0):
            cands.append(vertical + horizontal + 'A')
        if not (from_coord[1] == 0 and to_coord[0] == 0):
            cands.append(horizontal + vertical + 'A')
    if len(cands) == 2 and cands[0] == cands[1]:
        cands.pop()
    return cands


def robots(path, buttons):
    if len(path) <= 1:
        return [buttons]
    from_b = path[0]
    to_b = path[1]
    cands = get_cands(dir_kb, from_b, to_b)
    ret = []
    for cand in cands:
        ret.extend(robots(path[1:], buttons + cand))
    return ret


def get_ans(maybes, code):
    mini = min(map(lambda s: (len(s), s), maybes))
    code_val = int(code[:-1])
    return mini[1], code_val


ans1 = 0
for line in open('input').readlines():
    line = line.strip()
    from_b = 'A'
    to_b = line[0]
    possible_paths = ['']
    for from_b, to_b in zip('A'+line, line):
        cands = get_cands(num_kb, from_b, to_b)
        possible_paths_tmp = []
        for cand in cands:
            for possible_path in possible_paths:
                possible_paths_tmp.append(possible_path + cand)
        possible_paths = possible_paths_tmp
    mini = None
    print(possible_paths)
    for possible_path in possible_paths:
        maybe = robots('A' + possible_path, '')
        for a in maybe:
            maybe2 = robots('A' + a, '')
            mini_cand = get_ans(maybe2, line)
            if mini == None or mini_cand < mini:
                mini = mini_cand
    print(mini, len(mini[0]))
    ans1 += len(mini[0]) * mini[1]
print(ans1)
