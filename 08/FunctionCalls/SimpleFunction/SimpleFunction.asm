(SimpleFunction.test)
@SP 
A=M 
M=0 
@SP 
M=M+1 
@SP 
A=M 
M=0 
@SP 
M=M+1 
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D+M
@SP
A=M-1
M=!M
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D+M
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=M-D
@LCL
D=M
@FRAME
M=D
@5
A=D-A
D=M
@RETURN
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@FRAME
AM=M-1
D=M
@THAT
M=D
@FRAME
AM=M-1
D=M
@THIS
M=D
@FRAME
AM=M-1
D=M
@ARG
M=D
@FRAME
AM=M-1
D=M
@LCL
M=D
@RETURN
A=M
0;JMP
(END)
@END
0;JMP