import numpy as np

fn=input()

finput = open(fn +".asm", "r")
foutput = open(fn +".ir", "w")
ST={'R0':0,
'R1':1,
'R2':2,
'R3':3,
'R4':4,
'R5':5,
'R6':6,
'R7':7,
'R8':8,
'R9':9,
'R10':10,
'R11':11,
'R12':12,
'R13':13,
'R14':14,
'R15':15,
'SP':0,
'LCL':1,
'ARG':2,
'THIS':3,
'THAT':4,
'SCREEN':16384,
'KBD':24576}
count=0
for line in finput:
    l = line.split("//")
    l[0] = l[0].replace(" ", "")
    if len(l) > 1:
        l[0] += "\n"
    if l[0].rstrip():
        foutput.write(l[0])
        count+=1
    l1=l[0]
    if l1[0]=='@' and l1[1:-1] not in ST:
        if l1[1:-1].isnumeric():
            ST[l1[1:-1]]=int(l1[1:-1])
        else:
            ST[l1[1:-1]]=-1
    if l1[0]=='(':
        count-=1
        ST[l1[1:-2]]=count
    
q=16
for label in ST:
    if ST[label]==-1:
        ST[label]=q
        q+=1

foutput.close()
finput.close()

fi=open(fn+".ir", "r")
fo=open(fn+".hack", "w")
INST = {
        '0'    : '0101010',
        '1'    : '0111111',
        '-1'   : '0111010',
        'D'    : '0001100',
        'A'    : '0110000',
        '!D'   : '0001101',
        '!A'   : '0110001',
        '-D'   : '0001111',
        '-A'   : '0110011',
        'D+1'  : '0011111',
        'A+1'  : '0110111',
        'D-1'  : '0001110',
        'A-1'  : '0110010',
        'D+A'  : '0000010','A+D'  : '0000010',
        'D-A'  : '0010011',
        'A-D'  : '0000111',
        'D&A'  : '0000000', 'A&D'  : '0000000',
        'D|A'  : '0010101', 'A|D'  : '0010101',
        'M'    : '1110000',
        '!M'   : '1110001',
        '-M'   : '1110011',
        'M+1'  : '1110111',
        'M-1'  : '1110010',
        'D+M'  : '1000010', 'M+D'  : '1000010',
        'D-M'  : '1010011',
        'M-D'  : '1000111',
        'D&M'  : '1000000', 'M&D'  : '1000000',
        'D|M'  : '1010101', 'M|D'  : '1010101',
    }
    
DEST = {
        '0'   : '000',
        'M'   : '001',
        'D'   : '010',
        'MD'  : '011', 'DM'  : '011',
        'A'   : '100',
        'AM'  : '101', 'MA'  : '101',
        'AD'  : '110', 'DA'  : '110',
        'ADM' : '111', 'AMD' : '111',
    }
    
JUMP = {
        '0'   : '000',
        'JGT' : '001',
        'JEQ' : '010',
        'JGE' : '011',
        'JLT' : '100',
        'JNE' : '101',
        'JLE' : '110',
        'JMP' : '111'
    }

for line in fi:
    line=line[:-1]
    if '@' in line:
        wr= '0' + str(np.binary_repr(ST[line[1:]], width=15))+'\n'
    elif '=' in line:
        le=line.split('=')
        wr= '111' + INST[le[1]]+ DEST[le[0]]+ JUMP['0']+'\n'
    elif ';' in line:
        lj=line.split(';')
        wr = '111'+ INST[lj[0]] + DEST['0'] + JUMP[lj[1]]+'\n'
    else:
        wr=""
    fo.write(wr)

fi.close()
fo.close()