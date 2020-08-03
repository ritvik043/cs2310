# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 17:01:24 2019

@author: Ritvik (Roll No: CS18B057)

"""

"""
TOKENISATION START:
"""
import re 
import sys
   
regex = '^[A-Za-z_][A-Za-z0-9_]*'

fn = sys.argv[1]
flagerror=False

fn=fn.split(".")[0]
fi = open(fn+".jack", "r")
fo = open(fn+".tok", "w")
err = open(fn+".err", "w")

keyword = ['class', 'constructor','function','method', 'field', 'static', 
           'var', 'int', 'char','boolean', 'void', 'true', 'false','null',
           'this', 'let', 'do','if', 'else', 'while', 'return']
symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
          '&', '|', '<', '>', '=', '~']

def check(string):  
     if(re.search(regex, string)):  
        return True  
     else:  
        return False  

fo.write("<tokens>\n")

iscomment = False
isstring = False
lno = 0

for line in fi:
    lno+=1
    l1=line
    if not iscomment:
        l1s=l1.split("//")
        l1=l1s[0]
        lcs=l1s[0].split("/*")
        l1=lcs[0]
        if len(lcs)>1:
            if "*/" not in lcs[1]:
                iscomment = True
            else:
                lcs1=lcs[1].split("*/")
                l1=l1+" "+lcs1[1]
    elif iscomment:
         if "*/" not in l1:
            iscomment = True
            continue
         else:
            ls = l1.split("*/")
            l1 = ls[1]
            iscomment=False
    for key in symbol:
        l1=l1.replace(key, " "+key+" ")
    ls=l1.split()
    for token in ls:
        if isstring:
            if token[-1] in ['"']:
                fo.write(" "+token[:-1]+" </stringConstant>\n")
                isstring=False
            else:
                fo.write(" "+token)
        elif token in keyword:
            fo.write("<keyword> "+token+" </keyword>\n")
        elif token in symbol:
            token=token.replace("&","&amp;")
            token=token.replace("<","&lt;")
            token=token.replace(">","&gt;")
            fo.write("<symbol> "+token+" </symbol>\n")
        elif token.isdigit():
            fo.write("<integerConstant> "+token+" </integerConstant>\n")
        elif token[0] in ['"']:
            fo.write("<stringConstant> "+token[1:])
            if token[-1] in ['"']:
                fo.write("\b </stringConstant>\n")
            else: 
                isstring=True
        elif check(token):
            fo.write("<identifier> "+token+" </identifier>\n")
        else:
            if flagerror is False:
                err.write("Invalid token : "+token+"\n")
                flagerror=True
            else:
                continue

            
fo.write("</tokens>\n")

fi.close()
fo.close()
 
"""
Tokenisation done
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:39:43 2019

@author: Ritvik
"""
import sys


fi=open(fn+".tok","r")
fo=open(fn+".anz","w")
fv=open(fn+".vm","w")

class symbolTable:
    def __init__(self, name=None, kind=None, type =None, index=None):
        self.name=name
        self.kind=kind
        self.type=type
        self.index=index
        

l=fi.readline()
s=0
lno=0
labelno=0
ccn=""  #currentClassName
csn=""  #cuurentsubname
cst=""   #currentSubType
static_count=0
field_count=0
total_count=0
argument_count=0
local_count=0
total_counts=0

def errortype(typet):       #Used when verifyng type only
    global flagerror
    if typet not in l.split() and flagerror is False:
        err.write("ERROR: Expecting "+typet+" but "+l.split()[1]+"\n")
        flagerror=True

def errortt(typet, token):        #used when verifynig a token
    global flagerror
    if typet not in l.split() and flagerror is False:
        err.write("ERROR: Expecting "+typet+" but "+l.split()[1]+"\n")
        flagerror=True
    if token not in l.split() and flagerror is False:
        err.write("ERROR: "+l.split()[1]+"\n")
        flagerror=True
    return


def compileClass():
    global s, lno, static_count,field_count, total_count
    global l,ccn
    fo.write(" "*s+"<class>\n")
    s += 2
    fo.write(" "*s+l)  #class
    classST=[]
    static_count=0
    field_count=0
    total_count=0
    l=fi.readline()
    lno+=1
    errortype("<identifier>")
    fo.write(" "*s+l)  #className
    ccn=l.split()[1]
    l=fi.readline()
    lno+=1
    errortt("<symbol>","{")
    fo.write(" "*s+l)  #{
    l=fi.readline()
    lno+=1
    compileClassVarDec(classST)
    compileSubroutineDec(classST)
    errortt("<symbol>","}")
    fo.write(" "*s+l)  #}
    s-=2
    l=fi.readline()
    lno+=1
    fo.write(" "*s+"</class>\n")
    return

def compileClassVarDec(classST):
    global s,lno, static_count, field_count, total_count
    global l
    while "static" in l.split() or "field" in l.split():
        fo.write(" "*s+"<classVarDec>\n")
        #l=fi.readline()
        s+=2
        while "static" in l.split() or "field" in l.split():
            fo.write(" "*s+l)   #static|field
            kindv = l.split()[1]
            l=fi.readline()
            lno+=1
            fo.write(" "*s+l)   #type
            typev = l.split()[1]
            l=fi.readline()
            lno+=1
            while "<identifier>" in l.split():
                fo.write(" "*s+l)    #name
                namev=l.split()[1]
                if kindv in ["static"]:
                    index=static_count
                    static_count+=1
                    classST.append(symbolTable(namev, kindv, typev, index))
                else:
                    index=field_count
                    field_count+=1
                    classST.append(symbolTable(namev, "this", typev, index))
                total_count+=1
                l=fi.readline()
                lno+=1
                if l.split()[1] in [","] :
                    fo.write(" "*s+l)
                    l=fi.readline()
                    lno+=1
        errortt("<symbol>",";")
        fo.write(" "*s+l)
        l=fi.readline()
        lno+=1
        s-=2
        fo.write(" "*s+"</classVarDec>\n")
    return

def compileSubroutineDec(classST):
    global s,lno,ccn,cst,csn, argument_count,local_count,total_counts
    global l
    while l.split()[1] in ["constructor", "function", "method"]:
        fo.write(" "*s+"<subroutineDec>\n")
        s+=2
        fo.write(" "*s+l)    #constructor,function,method...etc.
        cst=l.split()[1]
        l=fi.readline()
        lno+=1
        fo.write(" "*s+l)    #void | type
        l=fi.readline()
        lno+=1
        errortype("<identifier>")
        fo.write(" "*s+l)   #subroutine name
        csn=l.split()[1]
        l=fi.readline()
        lno+=1
        subST=[]
        argument_count=0
        local_count=0
        total_counts=0
        if cst in ["method"]:
            subST.append(symbolTable("this", "argument", ccn,0))
            argument_count+=1
            total_counts+=1
        errortt("<symbol>","(")
        fo.write(" "*s+l)  #(
        l=fi.readline()
        lno+=1
        compileParameterList(subST)
        errortt("<symbol>",")")
        fo.write(" "*s+l)  #)
        l=fi.readline()
        lno+=1
        compileSubroutineBody(subST,classST)
        s-=2
        fo.write(" "*s+"</subroutineDec>\n")
    return

def compileParameterList(subST):
    global s,lno,csn,cst,argument_count, total_counts
    global l
    fo.write(" "*s+"<parameterList>\n")
    s+=2
    while l.split()[0] in ["<keyword>","<identifier>"]:
        fo.write(" "*s+l)    #int,..
        typev=l.split()[1]
        l=fi.readline()
        lno+=1
        errortype("<identifier>")
        fo.write(" "*s+l)     #varname
        namev=l.split()[1]
        subST.append(symbolTable(namev,"argument",typev,argument_count))
        argument_count+=1
        total_counts+=1
        l=fi.readline()
        lno+=1
        if l.split()[1] in [","]:
            fo.write(" "*s+l)
            l=fi.readline()
            lno+=1
    s-=2
    fo.write(" "*s+"</parameterList>\n")
    return

def compileSubroutineBody(subST,classST):
    global s,lno, local_count,total_counts
    global l
    fo.write(" "*s+"<subroutineBody>\n")
    s+=2
    errortt("<symbol>","{")
    fo.write(" "*s+l)
    l=fi.readline()
    lno+=1
    compileVarDec(subST)
    fv.write("function "+ccn+"."+csn+" "+str(local_count)+"\n")
    if cst in ["constructor"]:
        fv.write("push constant "+str(field_count)+"\n")
        fv.write("call Memory.alloc 1 \n")
        fv.write("pop pointer 0 \n")
    if cst in ["method"]:
        fv.write("push argument 0 \npop pointer 0 \n")                
    compileStatements(subST,classST)
    errortt("<symbol>","}")
    fo.write(" "*s+l)
    s-=2
    l=fi.readline()
    lno+=1
    fo.write(" "*s+"</subroutineBody>\n")
    return

def compileVarDec(subST):
    global s, local_count, total_counts
    global l,lno
    while "var" in l.split():
        fo.write(" "*s+"<varDec>\n")
        #l=fi.readline()
        s+=2
        while "var" in l.split():
            fo.write(" "*s+l)   #var
            l=fi.readline()
            lno+=1
            fo.write(" "*s+l)   #type
            typev=l.split()[1]
            l=fi.readline()
            lno+=1
            while "<identifier>" in l.split():
                fo.write(" "*s+l)    #name
                namev=l.split()[1]
                subST.append(symbolTable(namev,"local",typev,local_count))
                local_count+=1
                total_counts+=1
                l=fi.readline()
                lno+=1
                if l.split()[1] in [","] :
                    fo.write(" "*s+l)
                    l=fi.readline()
                    lno+=1
        errortt("<symbol>",";")
        fo.write(" "*s+l)
        l=fi.readline()
        lno+=1
        s-=2
        fo.write(" "*s+"</varDec>\n")
    return

def compileStatements(subST,classST):
    global s
    global l
    fo.write(" "*s+"<statements>\n")
    s+=2
    while l.split()[1] in ["let", "if", "while","do", "return"]:
        if l.split()[1] in ["let"]:
            compileLetStatement(subST,classST)
        elif l.split()[1] in ["if"]:
            compileIfStatement(subST,classST)
        elif l.split()[1] in ["while"]:
            compileWhileStatement(subST,classST)
        elif l.split()[1] in ["do"]:
            compileDoStatement(subST,classST)
        elif l.split()[1] in ["return"]:
            compileReturnStatement(subST,classST)
    s-=2
    fo.write(" "*s+"</statements>\n")
    return

def getkind(name,classST,subST):
    for i in classST:
        if i.name == name:
            return i.kind
    for i in subST:
        if i.name == name:
            return i.kind
    return False
        
def getindex(name,classST,subST):
    for i in classST:
        if i.name == name:
            return str(i.index)
    for i in subST:
        if i.name == name:
            return str(i.index)

def gettype(name,classST,subST):
    for i in classST:
        if i.name == name:
            return i.type
    for i in subST:
        if i.name == name:
            return i.type

def errvar(varname, classST, subST):
    global flagerror
    if getkind(varname,classST, subST) is False and flagerror is False:
        err.write("Declaration error: "+varname+" undeclared\n")
        flagerror=True

def compileLetStatement(subST,classST):
    global s
    global l,lno
    fo.write(" "*s+"<letStatement>\n")
    s+=2
    fo.write(" "*s+l)  #let
    l=fi.readline()
    lno+=1
    errortype("<identifier>")
    fo.write(" "*s+l)  # varName
    varname=l.split()[1]
    errvar(varname,classST,subST)
    l=fi.readline()
    lno+=1
    f=False
    if l.split()[1] in ["["]:
        fo.write(" "*s+l)  #[
        l=fi.readline()
        lno+=1
        compileExpression(classST,subST)
        errortt("<symbol>","]")
        fo.write(" "*s+l)  #]
        fv.write("push "+getkind(varname,classST,subST)+" "+getindex(varname,classST,subST)+"\nadd \n")
        l=fi.readline()
        lno+=1
        f=True
    errortt("<symbol>","=")
    fo.write(" "*s+l)  #=
    l=fi.readline()
    lno+=1
    compileExpression(classST,subST)   #expression
    if f:
        fv.write("pop temp 0\npop pointer 1\npush temp 0\npop that 0\n")
    else:
        fv.write("pop "+getkind(varname,classST,subST)+" "+getindex(varname,classST,subST)+"\n")
    errortt("<symbol>",";")
    fo.write(" "*s+l)   #;
    l=fi.readline()
    lno+=1
    s-=2
    fo.write(" "*s+"</letStatement>\n")
    return

def compileIfStatement(classST,subST):
    global s,lno,labelno
    global l
    fo.write(" "*s+"<ifStatement>\n")
    s+=2
    fo.write(" "*s+l)  #if
    l=fi.readline()
    tlabn=labelno
    labelno+=2
    lno+=1
    errortt("<symbol>","(")
    fo.write(" "*s+l)  #(
    l=fi.readline()
    lno+=1
    compileExpression(classST,subST)   #expression
    errortt("<symbol>",")")
    fo.write(" "*s+l)  #)
    l=fi.readline()
    lno+=1
    errortt("<symbol>","{")
    fo.write(" "*s+l)  #{
    l=fi.readline()
    fv.write("not \nif-goto "+ccn+"."+str(tlabn)+"\n")
    lno+=1
    compileStatements(classST,subST)  #statements
    errortt("<symbol>","}")
    fo.write(" "*s+l)   #}
    l=fi.readline()
    fv.write("goto "+ccn+"."+str(tlabn+1)+"\nlabel "+ccn+"."+str(tlabn)+"\n")
    lno+=1
    if l.split()[1] in ["else"]:
        fo.write(" "*s+l)   #else
        l=fi.readline()
        lno+=1
        errortt("<symbol>","{")
        fo.write(" "*s+l)  #{
        l=fi.readline()
        lno+=1
        compileStatements(classST,subST)  #statements
        errortt("<symbol>","}")
        fo.write(" "*s+l)   #}
        l=fi.readline()
        lno+=1
    s-=2
    fv.write("label "+ccn+"."+str(tlabn+1)+"\n")
    fo.write(" "*s+"</ifStatement>\n")
    return

def compileWhileStatement(classST,subST):
    global s,lno,labelno
    global l
    fo.write(" "*s+"<whileStatement>\n")
    s+=2
    fo.write(" "*s+l)  #while
    l=fi.readline()
    tlabn=labelno
    labelno+=2
    lno+=1
    fv.write("label "+ccn+"."+str(tlabn)+"\n")
    errortt("<symbol>","(")
    fo.write(" "*s+l)  #(
    l=fi.readline()
    lno+=1
    compileExpression(classST,subST)   #expression
    errortt("<symbol>",")")
    fo.write(" "*s+l)  #)
    l=fi.readline()
    fv.write("not \nif-goto "+ccn+"."+str(tlabn+1)+"\n")
    lno+=1
    errortt("<symbol>","{")
    fo.write(" "*s+l)  #{
    l=fi.readline()
    lno+=1
    compileStatements(classST,subST)  #statements
    errortt("<symbol>","}")
    fo.write(" "*s+l)   #}
    fv.write("goto "+ccn+"."+str(tlabn)+"\nlabel "+ccn+"."+str(tlabn+1)+"\n")
    l=fi.readline()
    lno+=1
    s-=2
    fo.write(" "*s+"</whileStatement>\n")
    return

def compileDoStatement(classST,subST):
    global s,lno
    global l
    fo.write(" "*s+"<doStatement>\n")
    s+=2
    fo.write(" "*s+l)  #do
    l=fi.readline()
    lno+=1
    errortype("<identifier>")
    fo.write(" "*s+l)  #id1
    id1=l.split()[1]
    l=fi.readline()
    lno+=1
    if l.split()[1] in ["."]:
        fo.write(" "*s+l)  #.
        l=fi.readline()
        lno+=1
        errortype("<identifier>")
        fo.write(" "*s+l)  #id2
        id2=l.split()[1]
        if getkind(id1,classST,subST) is not False:
            fv.write("push "+getkind(id1,classST,subST)+" "+str(getindex(id1,classST,subST))+"\n")
        l=fi.readline()
        lno+=1
        errortt("<symbol>","(")
        fo.write(" "*s+l)  #(
        l=fi.readline()
        lno+=1
        nP=compileExpressionList(classST, subST)   #expressionlist
        errortt("<symbol>",")")
        fo.write(" "*s+l)  #)
        if getkind(id1,classST,subST) is not False:
            fv.write("call "+gettype(id1,classST,subST)+"."+id2+" "+str(nP+1)+"\npop temp 0\n")
        else:
            fv.write("call "+id1+"."+id2+" "+str(nP)+"\npop temp 0\n")
        l=fi.readline()
        lno+=1
    else:
        errortt("<symbol>","(")
        fo.write(" "*s+l)  #(
        l=fi.readline()
        fv.write("push pointer 0\n")
        lno+=1
        nP=compileExpressionList(classST,subST)   #expressionlist
        errortt("<symbol>",")")
        fo.write(" "*s+l)  #)
        fv.write("call "+ccn+"."+id1+" "+str(nP+1)+"\npop temp 0\n")
        l=fi.readline()
        lno+=1
    errortt("<symbol>",";")
    fo.write(" "*s+l)   #;
    l=fi.readline()
    lno+=1
    s-=2
    fo.write(" "*s+"</doStatement>\n")
    return

def compileReturnStatement(classST,subST):
    global s,lno
    global l
    fo.write(" "*s+"<returnStatement>\n")
    s+=2
    fo.write(" "*s+l)  #return
    l=fi.readline()
    lno+=1
    f=True
    if l.split()[1] not in [";"]:
        compileExpression(classST,subST)
        fv.write("return\n")
        f=False
    errortt("<symbol>",";")
    fo.write(" "*s+l)
    if f:
        fv.write("push constant 0\nreturn\n")
    l=fi.readline()
    lno+=1    #;
    s-=2
    fo.write(" "*s+"</returnStatement>\n")
    return

op=["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]
op_code={'+':'add\n','-':'sub\n', '*':'call Math.multiply 2\n','/':'call Math.divide 2\n',
         '&amp;':'and\n', '|':'or\n', '&lt;':'lt\n', '&gt;':'gt\n', '=':'eq\n'}
unary={'-':'neg\n','~':'not\n'}

def compileExpression(classST,subST):
    global s,lno
    global l
    fo.write(" "*s+"<expression>\n")
    s+=2
    compileTerm(classST,subST)   #term
    while l.split()[1] in op:
        fo.write(" "*s+l)  #op
        opc=op_code[l.split()[1]]
        l=fi.readline()
        lno+=1
        compileTerm(classST,subST)     #term
        fv.write(opc)
    s-=2
    fo.write(" "*s+"</expression>\n")
    return

def compileExpressionList(classST,subST):
    global s
    global l,lno
    fo.write(" "*s+"<expressionList>\n")
    nP=0
    s+=2
    while l.split()[1] not in [")"]:
        compileExpression(classST,subST)   #expression
        nP+=1
        if l.split()[1] not in [","]:
            break
        fo.write(" "*s+l)  #,
        l=fi.readline()
        lno+=1
    s-=2
    fo.write(" "*s+"</expressionList>\n")
    return nP

def compileTerm(classST,subST):
    global s
    global l,lno
    fo.write(" "*s+"<term>\n")
    s+=2
    if l.split()[0] in ["<integerConstant>","<stringConstant>","<keyword>"]:
        fo.write(" "*s+l)  
        if l.split()[0] in ["<integerConstant>"]:
            fv.write("push constant "+l.split()[1]+"\n")
        elif l.split()[1] in ["true"]:
            fv.write("push constant 0\nnot\n")
        elif l.split()[1] in ["false","null"]:
            fv.write("push constant 0\n")
        elif l.split()[1] in ["this"]:
            fv.write("push pointer 0\n")
        elif l.split()[0] in ["<stringConstant>"]:
            string=" ".join(l.split()[1:-1])
            strlen=len(string)
            fv.write("push constant "+str(strlen)+"\ncall String.new 1\n")
            for i in string:
                fv.write(f"push constant {ord(i)}\ncall String.appendChar 2\n")
        l=fi.readline()
        lno+=1
    elif l.split()[0] in ["<identifier>"]:
        fo.write(" "*s+l) 
        id1=l.split()[1]
        l=fi.readline()
        lno+=1
        if l.split()[1] in ["["]:
            errvar(id1,classST,subST)
            fo.write(" "*s+l)  #[
            l=fi.readline()
            lno+=1
            compileExpression(classST,subST)
            errortt("<symbol>","]")
            fo.write(" "*s+l)  #]
            fv.write("push "+getkind(id1,classST,subST)+" "+str(getindex(id1,classST,subST))+"\n")
            fv.write("add\npop pointer 1\npush that 0\n")
            l=fi.readline()
            lno+=1
        elif l.split()[1] in ["."]:   
            fo.write(" "*s+l)  #.
            l=fi.readline()
            lno+=1
            errortype("<identifier>")
            fo.write(" "*s+l)  #id2
            id2=l.split()[1]
            if getkind(id1,classST,subST) is not False:
                fv.write("push "+getkind(id1,classST,subST)+" "+str(getindex(id1,classST,subST))+"\n")
            l=fi.readline()
            lno+=1
            errortt("<symbol>","(")
            fo.write(" "*s+l)  #(
            l=fi.readline()
            lno+=1
            nP=compileExpressionList(classST, subST)   #expressionlist
            errortt("<symbol>",")")
            fo.write(" "*s+l)  #)
            if getkind(id1,classST,subST) is not False:
                fv.write("call "+gettype(id1,classST,subST)+"."+id2+" "+str(nP+1)+"\n")
            else:
                fv.write("call "+id1+"."+id2+" "+str(nP)+"\n")
            l=fi.readline()
            lno+=1
        elif l.split()[1] in ["("]:
            fo.write(" "*s+l)  #(
            l=fi.readline()
            fv.write("push pointer 0\n")
            lno+=1
            nP=compileExpressionList(classST,subST)   #expressionlist
            errortt("<symbol>",")")
            fo.write(" "*s+l)  #)
            fv.write("call "+ccn+"."+id1+" "+str(nP+1)+"\n")
            l=fi.readline()
            lno+=1
        else:
            errvar(id1,classST,subST)
            fv.write("push "+getkind(id1,classST,subST)+" "+str(getindex(id1,classST,subST))+"\n")
    elif l.split()[1] in ["("]:
        fo.write(" "*s+l)    #(
        l=fi.readline()
        lno+=1
        compileExpression(classST,subST)   #expression
        errortt("<symbol>",")")
        fo.write(" "*s+l)  #)
        l=fi.readline()
        lno+=1
    elif l.split()[1] in ["-","~"]:
        fo.write(" "*s+l)  
        unop=unary[l.split()[1]]
        l=fi.readline()
        lno+=1
        compileTerm(classST,subST)
        fv.write(unop)
    s-=2
    fo.write(" "*s+"</term>\n")
    return
"""
MAIN
"""
               
while l not in ["</tokens>\n"] and len(l) > 1:
    if l in ["<tokens>\n"]:
        l=fi.readline()
        lno+=1
    elif "class" in l.split():
        compileClass()
        l=fi.readline()
        lno+=1
    else:
        l=fi.readline()
        lno+=1
fi.close()
fo.close()
fv.close()
err.close()