instructions: dict = dict({
    "=" : "LDA",
    "+" : "ADD",
    "-" : "SUB"
})
binary: dict = dict({
    "LDA" : "0000",
    "ADD" : "0001",
    "SUB" : "0010",
    "OUT" : "1110",
    "HLT" : "1111"
})

def get_hex(n: int, pad: bool = True) -> str:
    res = str(hex(n).split('x')[-1])
    return '0' * pad * (2 - len(res)) + res

def get_bin(n: int) -> str:
    res = str(bin(n).split('b')[-1])
    return '0' * (4 - len(res)) + res


def parse_exp(exp: str, start_loc: int):
    exp = exp.replace(' ', '')
    exp = '=' + exp
    sign: str = ''
    num:str = ''
    ret: dict = dict({
        'inst': [],
        'nums': []
    })
    for idx, i in enumerate(exp):
        if i >= '0' and i <= '9':
            num += i
        else:
            if sign == '':
                sign = i
            else:
                ret['inst'].append(f'{instructions[sign]} {get_hex(start_loc)}')
                ret['nums'].append(int(num))
                start_loc += 1
                num = ''
                sign = i
    if idx == len(exp) - 1:
        ret['inst'].append(f'{instructions[sign]} {get_hex(start_loc)}')
        ret['nums'].append(int(num))
        start_loc += 1
    ret['inst'].append("OUT 0")
    ret['inst'].append("HLT 0")
    return ret





def parse_args():
    import sys
    flag: str = ''
    args = dict()
    for i in sys.argv[1:]:
        if i[:1] == '-':
            flag = i
            pass
        else:
            args[flag] = i
    return args



args = parse_args()


exp: str = args['--exp']
start_loc = int(args['--mem']) if '--mem' in args else 8

print()
print(f'Expression \t: {exp}')
print(f'Start Location \t: {get_hex(start_loc, pad=False).upper()}H')
print(f'Output\t\t: {get_hex(eval(exp)).upper()}')
print()


parsed = parse_exp(exp, start_loc)
inst = parse_exp(exp, start_loc)['inst']
nums = parse_exp(exp, start_loc)['nums']
print('Commands')
for i in inst:
    print(i)



hex_commands = []
for i in inst:
    cccc = i.split(' ')[0]
    vvvv = i.split(' ')[1]
    bstr = binary[cccc] + get_bin(int(vvvv, 16))
    hex_commands.append(get_hex(int(bstr, 2)))



print()
print('Logisim input file')
output = 'v2.0 raw\n'


for i in range(0, start_loc):
    if i < len(hex_commands):
        output += hex_commands[i] + ' '
    else:
        output += '0' + ' '




for num in nums:
    hex_num = get_hex(num)
    output += hex_num + ' '

print(output)
print()


out = open("in.txt", "w") 
out.write(output)
out.close()
