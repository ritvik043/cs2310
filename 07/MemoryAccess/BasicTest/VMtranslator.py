"""
Created on Thu Oct  3 11:05:53 2019

@author: Ritvik
"""

fn="BasicTest"

fi=open(fn+".vm", "r")
fo=open(fn+".ir", "w")
for line in fi:
    l = line.split("//")
    """if len(l[0].replace(" ","")) > 1:
        l[0]+="\n"
        """
    if l[0].rstrip():
        fo.write(l[0])
fi.close()
fo.close()

fi=open(fn+".ir", "r")
fo=open(fn+".asm", "w")

vm_cmd={
                     'push constant' :  '@X' + '\n'
                                        'D=A' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n',
                     'push argument' :  '@X' + '\n'
                                        'D=A' + '\n'
                                        '@ARG' + '\n'
                                        'A=D+M' + '\n'
                                        'D=M' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n',
                     'push local' :     '@X' + '\n'
                                        'D=A' + '\n'
                                        '@LCL' + '\n'
                                        'A=D+M' + '\n'
                                        'D=M' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n',
                     'push static' :    '@X' + '\n'
                                        'D=A' + '\n'
                                        '@16' + '\n'
                                        'A=D+A' + '\n'
                                        'D=M' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n',
                     'push this' :      '@X' + '\n'
                                        'D=A' + '\n'
                                        '@THIS' + '\n'
                                        'A=D+M' + '\n'
                                        'D=M' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n',
                     'push that' :      '@X' + '\n'
                                        'D=A' + '\n'
                                        '@THAT' + '\n'
                                        'A=D+M' + '\n'
                                        'D=M' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n',
                     'push pointer' :   '@X' + '\n'
                                        'D=A' + '\n'
                                        '@3' + '\n' 
                                        'A=D+A' + '\n'
                                        'D=M' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n', 
                     'push temp' :      '@X' + '\n'
                                        'D=A' + '\n'
                                        '@5' + '\n'
                                        'A=D+A' + '\n'
                                        'D=M' + '\n'
                                        '@SP' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'M=M+1' + '\n',
                     'pop argument' :   '@X' + '\n'
                                        'D=A' + '\n'
                                        '@ARG' + '\n'
                                        'D=D+M' + '\n'
                                        '@R5' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'AM=M-1' + '\n'
                                        'D=M' + '\n'
                                        '@R5' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n',
                     'pop local' :      '@X' + '\n'
                                        'D=A' + '\n'
                                        '@LCL' + '\n'
                                        'D=D+M' + '\n'
                                        '@R5' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'AM=M-1' + '\n'
                                        'D=M' + '\n'
                                        '@R5' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n',
                     'pop static' :     '@X' + '\n'
                                        'D=A' + '\n'
                                        '@16' + '\n'
                                        'D=D+A' + '\n'
                                        '@R5' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'AM=M-1' + '\n'
                                        'D=M' + '\n'
                                        '@R5' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n',
                     'pop this' :       '@X' + '\n'
                                        'D=A' + '\n'
                                        '@R3' + '\n'
                                        'D=D+M' + '\n'
                                        '@R5' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'AM=M-1' + '\n'
                                        'D=M' + '\n'
                                        '@R5' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n',
                     'pop that' :       '@X' + '\n'
                                        'D=A' + '\n'
                                        '@R4' + '\n'
                                        'D=D+M' + '\n'
                                        '@R5' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'AM=M-1' + '\n'
                                        'D=M' + '\n'
                                        '@R5' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n',
                     'pop pointer' :    '@X' + '\n'
                                        'D=A' + '\n'
                                        '@3' + '\n'
                                        'D=D+A' + '\n'
                                        '@R5' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'AM=M-1' + '\n'
                                        'D=M' + '\n'
                                        '@R5' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n',
                    'pop temp' :        '@X' + '\n'
                                        'D=A' + '\n'
                                        '@5' + '\n'
                                        'D=D+A' + '\n'
                                        '@R5' + '\n'
                                        'M=D' + '\n'
                                        '@SP' + '\n'
                                        'AM=M-1' + '\n'
                                        'D=M' + '\n'
                                        '@R5' + '\n'
                                        'A=M' + '\n'
                                        'M=D' + '\n',
                    'add' :     '@SP' + '\n'
                                'AM=M-1' + '\n'
                                'D=M' + '\n'
                                'M=0' + '\n'
                                '@SP' + '\n'
                                'A=M-1' + '\n'
                                'M=D+M' + '\n',                                    
                     'sub' :    '@SP' + '\n'
                                'AM=M-1' + '\n'
                                'D=M' + '\n'
                                'M=0' + '\n'
                                '@SP' + '\n'
                                'A=M-1' + '\n'
                                'M=M-D' + '\n',
                     'neg' :    '@SP' + '\n'
                                'A=M-1' + '\n'
                                'M=-M' + '\n',
                     'eq' :     '@SP' + '\n'
                                'AM=M-1' + '\n'
                                'D=M' + '\n'
                                'M=0' + '\n'
                                'A=A-1' + '\n'
                                'D=M-D' + '\n'
                                'M=-1' + '\n'
                                '@JJ' + '\n'
                                'D;JEQ' + '\n'
                                '@SP' + '\n'
                                'A=M-1'+  '\n'
                                'M=0' + '\n'
                                '(JJ)' + '\n',
                     'gt' :     '@SP' + '\n'
                                'AM=M-1' + '\n'
                                'D=M' + '\n'
                                'M=0' + '\n'
                                'A=A-1' + '\n'
                                'D=M-D' + '\n'
                                'M=-1' + '\n'
                                '@JJ' + '\n'
                                'D;JGT' + '\n'
                                '@SP' + '\n'
                                'A=M-1'+  '\n'
                                'M=0' + '\n'
                                '(JJ)' + '\n',
                     'lt' :     '@SP' + '\n'
                                'AM=M-1' + '\n'
                                'D=M' + '\n'
                                'M=0' + '\n'
                                'A=A-1' + '\n'
                                'D=M-D' + '\n'
                                'M=-1' + '\n'
                                '@JJ' + '\n'
                                'D;JLT' + '\n'
                                '@SP' + '\n'
                                'A=M-1'+  '\n'
                                'M=0' + '\n'
                                '(JJ)' + '\n',
                     'and' :    '@SP' + '\n'
                                'AM=M-1' + '\n'
                                'D=M' + '\n'
                                'M=0' + '\n'
                                '@SP' + '\n'
                                'A=M-1' + '\n'
                                'M=D&M' + '\n',
                     'or' :     '@SP' + '\n'
                                'AM=M-1' + '\n'
                                'D=M' + '\n'
                                'M=0' + '\n'
                                '@SP' + '\n'
                                'A=M-1' + '\n'
                                'M=D|M' + '\n',
                     'not' :    '@SP' + '\n'
                                'A=M-1' + '\n'
                                'M=!M' + '\n'
         }
count=0
for line in fi:
    l=line.split()
    if len(l)<2:
        if l[0] in ['add', 'and', 'or', 'not', 'sub', 'neg']:
            fo.write(vm_cmd[l[0]])
        else:
            l1=vm_cmd[l[0]].replace('JJ', 'J'+str(count))
            fo.write(l1)
            count+=1
    elif len(l)>2:
        code = vm_cmd[l[0]+" "+l[1]]
        code = code.replace('X', l[2])
        fo.write(code)
        
fo.write('(END)\n' +\
         '@END\n' +\
         '0;JMP')
fi.close()
fo.close()