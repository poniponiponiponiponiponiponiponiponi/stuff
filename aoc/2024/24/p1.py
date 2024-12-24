inp = open('input').read().strip()
init, eqs = inp.split('\n\n')

vals = {}
for l in init.split('\n'):
    var, val = l.split(': ')
    vals[var] = int(val)

to_process = []
for eq in eqs.split('\n'):
    v1, op, v2, _, res = eq.split()
    op = op.replace('AND', '&').replace('XOR', '^').replace('OR', '|')
    to_process.append([res, v1, op, v2])

while len(to_process) != 0:
    new_to_process = []
    for res, v1, op, v2 in to_process:
        if v1 not in vals or v2 not in vals:
            new_to_process.append([res, v1, op, v2])
            continue
        vals[res] = eval(f"vals['{v1}'] {op} vals['{v2}']")
    to_process = new_to_process
    
bits = []
for i in range(100):
    z = f'z{i:02}'
    print(z)
    if z not in vals:
        break
    bits.append(str(vals[z]))
bits.reverse()
print(int(''.join(bits), 2))
