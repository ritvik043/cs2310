"""
Created on Thu Oct  3 11:05:53 2019

@author: Ritvik
"""

fn=input()

fi=open(fn+".vm", "r")
fo=open(fn+".ir", "w")
for line in fi:
    l1 = line.split("//")
    """if len(l[0].replace(" ","")) > 1:
        l[0]+="\n"
        """
    if l1[0].rstrip():
        fo.write(l1[0].strip()+"\n")
fi.close()
fo.close()

fi=open(fn+".ir", "r")
fo=open(fn+".asm", "w")

vm_cmd={
                     'push constant' :  '@X\n'
                                        'D=A\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n',
                     'push argument' :  '@X\n'
                                        'D=A\n'
                                        '@ARG\n'
                                        'A=D+M\n'
                                        'D=M\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n',
                     'push local' :     '@X\n'
                                        'D=A\n'
                                        '@LCL\n'
                                        'A=D+M\n'
                                        'D=M\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n',
                     'push static' :    '@X\n'
                                        'D=M\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n',
                     'push this' :      '@X\n'
                                        'D=A\n'
                                        '@THIS\n'
                                        'A=D+M\n'
                                        'D=M\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n',
                     'push that' :      '@X\n'
                                        'D=A\n'
                                        '@THAT\n'
                                        'A=D+M\n'
                                        'D=M\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n',
                     'push pointer' :   '@X\n'
                                        'D=A\n'
                                        '@3\n' 
                                        'A=D+A\n'
                                        'D=M\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n', 
                     'push temp' :      '@X\n'
                                        'D=A\n'
                                        '@5\n'
                                        'A=D+A\n'
                                        'D=M\n'
                                        '@SP\n'
                                        'A=M\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'M=M+1\n',
                     'pop argument' :   '@X\n'
                                        'D=A\n'
                                        '@ARG\n'
                                        'D=D+M\n'
                                        '@R13\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'AM=M-1\n'
                                        'D=M\n'
                                        '@R13\n'
                                        'A=M\n'
                                        'M=D\n',
                     'pop local' :      '@X\n'
                                        'D=A\n'
                                        '@LCL\n'
                                        'D=D+M\n'
                                        '@R13\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'AM=M-1\n'
                                        'D=M\n'
                                        '@R13\n'
                                        'A=M\n'
                                        'M=D\n',
                     'pop static' :     '@X\n'
                                        'D=A\n'
                                        '@R13\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'AM=M-1\n'
                                        'D=M\n'
                                        '@R13\n'
                                        'A=M\n'
                                        'M=D\n',
                     'pop this' :       '@X\n'
                                        'D=A\n'
                                        '@R3\n'
                                        'D=D+M\n'
                                        '@R13\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'AM=M-1\n'
                                        'D=M\n'
                                        '@R13\n'
                                        'A=M\n'
                                        'M=D\n',
                     'pop that' :       '@X\n'
                                        'D=A\n'
                                        '@R4\n'
                                        'D=D+M\n'
                                        '@R13\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'AM=M-1\n'
                                        'D=M\n'
                                        '@R13\n'
                                        'A=M\n'
                                        'M=D\n',
                     'pop pointer' :    '@X\n'
                                        'D=A\n'
                                        '@3\n'
                                        'D=D+A\n'
                                        '@R13\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'AM=M-1\n'
                                        'D=M\n'
                                        '@R13\n'
                                        'A=M\n'
                                        'M=D\n',
                    'pop temp' :        '@X\n'
                                        'D=A\n'
                                        '@5\n'
                                        'D=D+A\n'
                                        '@R13\n'
                                        'M=D\n'
                                        '@SP\n'
                                        'AM=M-1\n'
                                        'D=M\n'
                                        '@R13\n'
                                        'A=M\n'
                                        'M=D\n',
                    'add' :     '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                '@SP\n'
                                'A=M-1\n'
                                'M=D+M\n',                                    
                     'sub' :    '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                '@SP\n'
                                'A=M-1\n'
                                'M=M-D\n',
                     'neg' :    '@SP\n'
                                'A=M-1\n'
                                'M=-M\n',
                     'eq' :     '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                'A=A-1\n'
                                'D=M-D\n'
                                'M=-1\n'
                                '@JJ\n'
                                'D;JEQ\n'
                                '@SP\n'
                                'A=M-1\n'
                                'M=0\n'
                                '(JJ)\n',
                     'gt' :     '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                'A=A-1\n'
                                'D=M-D\n'
                                'M=-1\n'
                                '@JJ\n'
                                'D;JGT\n'
                                '@SP\n'
                                'A=M-1\n'
                                'M=0\n'
                                '(JJ)\n',
                     'lt' :     '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                'A=A-1\n'
                                'D=M-D\n'
                                'M=-1\n'
                                '@JJ\n'
                                'D;JLT\n'
                                '@SP\n'
                                'A=M-1\n'
                                'M=0\n'
                                '(JJ)\n',
                     'and' :    '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                '@SP\n'
                                'A=M-1\n'
                                'M=D&M\n',
                     'or' :     '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                '@SP\n'
                                'A=M-1\n'
                                'M=D|M\n',
                     'not' :    '@SP\n'
                                'A=M-1\n'
                                'M=!M\n',
                                
                                
                    'label':   '(X)\n',
                    'goto' :    '@X\n'
                                '0;JMP\n',
                    'if-goto':  '@SP\n'
                                'AM=M-1\n'
                                'D=M\n'
                                'M=0\n'
                                '@X\n'
                                'D;JNE\n',
                                
                    'function':     '(X)\n',
                    'call':     '@Return_name_X\n'
                                'D=A\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'
                                    
                                '@LCL\n'
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'
                                
                                '@ARG\n'
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'
                                
                                '@THIS\n'
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'
                                
                                '@THAT\n'
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'
                            
                                '@SP\n'
                                'D=M\n'
                                '@NARG\n'
                                'D=D-A\n'
                                '@5\n'
                                'D=D-A\n'
                                '@ARG\n'
                                'M=D\n'
                                
                                '@SP\n'
                                'D=M\n'
                                '@LCL\n'
                                'M=D\n'
                                
                                '@_name\n'
                                '0;JMP\n'
                                '(Return_name_X)\n',
                                
            'return':       '@LCL\n' 
                            'D=M\n' 
                            '@R13\n' 
                            'M=D\n' 
                            '@5\n' 
                            'A=D-A\n' 
                            'D=M\n' 
                            '@R14\n' 
                            'M=D\n' 
                            '@SP\n' 
                            'AM=M-1\n'
                            'D=M\n'
                            '@ARG\n' 
                            'A=M\n' 
                            'M=D\n' 
                            '@ARG\n' 
                            'D=M\n'
                            'D=D+1\n'
                            '@SP\n' 
                            'M=D\n' 
                            '@R13\n' 
                            'AM=M-1\n' 
                            'D=M\n' 
                            '@THAT\n' 
                            'M=D\n' 
                            '@R13\n' 
                            'AM=M-1\n' 
                            'D=M\n' 
                            '@THIS\n' 
                            'M=D\n' 
                            '@R13\n' 
                            'AM=M-1\n' 
                            'D=M\n' 
                            '@ARG\n' 
                            'M=D\n' 
                            '@R13\n' 
                            'AM=M-1\n' 
                            'D=M\n' 
                            '@LCL\n' 
                            'M=D\n' 
                            '@R14\n' 
                            'A=M\n' 
                            '0;JMP\n'                                   
          }
countfun=0
countbool=0
for line in fi:
    fo.write("\n//"+line)
    l=line.split()
    if len(l)<2:
        if l[0] in ['add', 'and', 'or', 'not', 'sub', 'neg','return']:
            fo.write(vm_cmd[l[0]])
        elif l[0] in ['eq', 'lt', 'gt']:
            l1=vm_cmd[l[0]].replace('JJ', 'J'+str(countbool)+'_'+fn)
            fo.write(l1)
            countbool+=1
    elif len(l) == 2:
        if l[0] in ['label', 'goto', 'if-goto']:
            code = vm_cmd[l[0]]
            code = code.replace('X', fn+'_'+l[1])
            fo.write(code)
    elif len(l)>2:
        if l[0] in ['push', 'pop']:
            if l[1] in ['static']:
                code = vm_cmd[l[0]+" "+l[1]]
                code = code.replace('X', fn+'_'+l[2])
            else:
                code = vm_cmd[l[0]+" "+l[1]]
                code = code.replace('X', l[2])
            fo.write(code)
        elif l[0] in ['function']:
            code=vm_cmd[l[0]]
            code=code.replace('X', l[1])
            for i in range(int(l[2])):
                code=code + '@SP \nA=M \nM=0 \n@SP \nM=M+1 \n'
            fo.write(code)
        elif l[0] in ['call']:
            code=vm_cmd[l[0]]
            code=code.replace('_name', l[1])
            code=code.replace('_X', '_'+str(countfun)+"_"+fn)
            code=code.replace('NARG', l[2])
            countfun+=1
            fo.write(code)
            
        
        
fo.write('(END)\n'
         '@END\n'
         '0;JMP')
fi.close()
fo.close()