from copy import deepcopy
from ipdb import launch_ipdb_on_exception

inp = open('input').read().strip()
init, eqs = inp.split('\n\n')

vals_orig = {}
for l in init.split('\n'):
    var, val = l.split(': ')
    vals_orig[var] = int(val)
bits_n = len(vals_orig)

to_process_orig = []
for eq in eqs.split('\n'):
    v1, op, v2, _, res = eq.split()
    op = op.replace('AND', '&').replace('XOR', '^').replace('OR', '|')
    to_process_orig.append([res, v1, op, v2])

def swap_output(to_process, x, y):
    p1 = to_process[x]
    p2 = to_process[y]
    p1[0], p2[0] = to_process[y][0], to_process[x][0]
    return p1[0], p2[0]

to_process = deepcopy(to_process_orig)
swapped = []
vals = deepcopy(vals_orig)

while len(to_process) != 0:
    new_to_process = []
    for res, v1, op, v2 in to_process:
        if v1 not in vals or v2 not in vals:
            new_to_process.append([res, v1, op, v2])
            continue
        vals[res] = eval(f"vals['{v1}'] {op} vals['{v2}']")
        changed = True
    to_process = new_to_process

bits = []
for i in range(100):
    z = f'z{i:02}'
    if z not in vals:
        break
    bits.append(str(vals[z]))
bits.reverse()
z = int(''.join(bits), 2)
bits = []
for i in range(100):
    x = f'x{i:02}'
    if x not in vals:
        break
    bits.append(str(vals[x]))
bits.reverse()
x = int(''.join(bits), 2)
bits = []
for i in range(100):
    y = f'y{i:02}'
    if y not in vals:
        break
    bits.append(str(vals[y]))
bits.reverse()
y = int(''.join(bits), 2)
if x + y == z:
    print("FOUNDDD")
    print(''.join(sorted(swapped)))
print(" " + bin(x))
print(" " + bin(y))
print(bin(x+y))
print(bin(z))
