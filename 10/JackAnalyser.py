# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:21:33 2019

@author: Ritvik
"""
import sys

fn=input()

fi=open(fn+".tok","r")
fo=open(fn+".anz","w")

l=fi.readline()
s=0
lno=0

def compileClass():
    global s, lno
    global l
    fo.write(" "*s+"<class>\n")
    s += 2
    fo.write(" "*s+l)  #class
    l=fi.readline()
    lno+=1
    if "<identifier>" not in l.split():
        print("Syntax error : <identifier> expected\n ")
        sys.exit()
    fo.write(" "*s+l)  #className
    l=fi.readline()
    lno+=1
    if l.split()[1] not in ["{"]:
        print("Syntax error : { expected\n")
        sys.exit()
    fo.write(" "*s+l)  #{
    l=fi.readline()
    lno+=1
    compileClassVarDec()
    compileSubroutineDec()
    if l.split()[1] not in ["}"]:
        print("Syntax error : } expected\n")
        sys.exit() 
    fo.write(" "*s+l)  #}
    s-=2
    l=fi.readline()
    lno+=1
    fo.write(" "*s+"</class>\n")
    return

def compileClassVarDec():
    global s,lno
    global l
    while "static" in l.split() or "field" in l.split():
        fo.write(" "*s+"<classVarDec>\n")
        #l=fi.readline()
        s+=2
        while "static" in l.split() or "field" in l.split():
            fo.write(" "*s+l)   #static|field
            l=fi.readline()
            lno+=1
            fo.write(" "*s+l)   #type
            l=fi.readline()
            lno+=1
            while "<identifier>" in l.split():
                fo.write(" "*s+l)    #name
                l=fi.readline()
                lno+=1
                if l.split()[1] in [","] :
                    fo.write(" "*s+l)
                    l=fi.readline()
                    lno+=1
        if l.split()[1] not in [";"]:
            print("Syntax error : ; expected\n")
            sys.exit()
        fo.write(" "*s+l)
        l=fi.readline()
        lno+=1
        s-=2
        fo.write(" "*s+"</classVarDec>\n")
    return

def compileSubroutineDec():
    global s,lno
    global l
    while l.split()[1] in ["constructor", "function", "method"]:
        fo.write(" "*s+"<subroutineDec>\n")
        s+=2
        fo.write(" "*s+l)    #constructor,function,method...etc.
        l=fi.readline()
        lno+=1
        fo.write(" "*s+l)    #void | type
        l=fi.readline()
        lno+=1
        if "<identifier>" not in l.split():
            print("Syntax error : <identifier> expected\n")
            sys.exit()
        fo.write(" "*s+l)   #subroutine name
        l=fi.readline()
        lno+=1
        if "(" not in l.split():
            print("Syntax error : ( expected\n")
            sys.exit()
        fo.write(" "*s+l)  #(
        l=fi.readline()
        lno+=1
        compileParameterList()
        if ")" not in l.split():
            print("Syntax error : ) expected\n")
            sys.exit()
        fo.write(" "*s+l)  #)
        l=fi.readline()
        lno+=1
        compileSubroutineBody()
        s-=2
        fo.write(" "*s+"</subroutineDec>\n")
    return

def compileParameterList():
    global s,lno
    global l
    fo.write(" "*s+"<parameterList>\n")
    s+=2
    while l.split()[1] in ["int", "boolean", "char", fn]:
        fo.write(" "*s+l)
        l=fi.readline()
        lno+=1
        if "<identifier>" not in l.split():
            print("Syntax error : <identifier> expected\n")
            sys.exit()
        fo.write(" "*s+l)
        l=fi.readline()
        lno+=1
        if l.split()[1] in [","]:
            fo.write(" "*s+l)
            l=fi.readline()
            lno+=1
    s-=2
    fo.write(" "*s+"</parameterList>\n")
    return

def compileSubroutineBody():
    global s,lno
    global l
    fo.write(" "*s+"<subroutineBody>\n")
    s+=2
    if l.split()[1] not in ["{"]:
        print("Syntax error : { expected\n")
        sys.exit()
    fo.write(" "*s+l)
    l=fi.readline()
    lno+=1
    compileVarDec()
    compileStatements()
    if l.split()[1] not in ["}"]:
        print("Syntax error : } expected\n")
        sys.exit()
    fo.write(" "*s+l)
    s-=2
    l=fi.readline()
    lno+=1
    fo.write(" "*s+"</subroutineBody>\n")
    return

def compileVarDec():
    global s
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
            l=fi.readline()
            lno+=1
            while "<identifier>" in l.split():
                fo.write(" "*s+l)    #name
                l=fi.readline()
                lno+=1
                if l.split()[1] in [","] :
                    fo.write(" "*s+l)
                    l=fi.readline()
                    lno+=1
        if l.split()[1] not in [";"]:
            print("Syntax error : ; expected\n")
            sys.exit()
        fo.write(" "*s+l)
        l=fi.readline()
        lno+=1
        s-=2
        fo.write(" "*s+"</varDec>\n")
    return

def compileStatements():
    global s
    global l
    fo.write(" "*s+"<statements>\n")
    s+=2
    while l.split()[1] in ["let", "if", "while","do", "return"]:
        if l.split()[1] in ["let"]:
            compileLetStatement()
        elif l.split()[1] in ["if"]:
            compileIfStatement()
        elif l.split()[1] in ["while"]:
            compileWhileStatement()
        elif l.split()[1] in ["do"]:
            compileDoStatement()
        elif l.split()[1] in ["return"]:
            compileReturnStatement()
    s-=2
    fo.write(" "*s+"</statements>\n")
    return

def compileLetStatement():
    global s
    global l,lno
    fo.write(" "*s+"<letStatement>\n")
    s+=2
    fo.write(" "*s+l)  #let
    l=fi.readline()
    lno+=1
    fo.write(" "*s+l)  #varName
    l=fi.readline()
    lno+=1
    if l.split()[1] in ["["]:
        fo.write(" "*s+l)  #[
        l=fi.readline()
        lno+=1
        compileExpression()
        if l.split()[1] not in ["]"]:
            print("Syntax error : ] expected\n")
            sys.exit()
        fo.write(" "*s+l)  #]
        l=fi.readline()
        lno+=1
    fo.write(" "*s+l)  #=
    l=fi.readline()
    lno+=1
    compileExpression()   #expression
    if l.split()[1] not in [";"]:
        print("Syntax error : ; expected\n")
        sys.exit()
    fo.write(" "*s+l)
    l=fi.readline()
    lno+=1#;
    s-=2
    fo.write(" "*s+"</letStatement>\n")
    return

def compileIfStatement():
    global s,lno
    global l
    fo.write(" "*s+"<ifStatement>\n")
    s+=2
    fo.write(" "*s+l)  #if
    l=fi.readline()
    lno+=1
    if "(" not in l.split():
        print("Syntax error : ( expected\n")
        sys.exit()
    fo.write(" "*s+l)  #(
    l=fi.readline()
    lno+=1
    compileExpression()   #expression
    if ")" not in l.split():
        print("Syntax error : ) expected\n")
        sys.exit()
    fo.write(" "*s+l)  #)
    l=fi.readline()
    lno+=1
    if l.split()[1] not in ["{"]:
        print("Syntax error : { expected\n")
        sys.exit()
    fo.write(" "*s+l)  #{
    l=fi.readline()
    lno+=1
    compileStatements()  #statements
    if l.split()[1] not in ["}"]:
        print("Syntax error : } expected\n")
        sys.exit()
    fo.write(" "*s+l)   #}
    l=fi.readline()
    lno+=1
    if l.split()[1] in ["else"]:
        fo.write(" "*s+l)   #else
        l=fi.readline()
        lno+=1
        if l.split()[1] not in ["{"]:
            print("Syntax error : { expected\n")
            sys.exit()
        fo.write(" "*s+l)  #{
        l=fi.readline()
        lno+=1
        compileStatements()  #statements
        if l.split()[1] not in ["}"]:
            print("Syntax error : } expected\n")
            sys.exit()
        fo.write(" "*s+l)   #}
        l=fi.readline()
        lno+=1
    s-=2
    fo.write(" "*s+"</ifStatement>\n")
    return

def compileWhileStatement():
    global s,lno
    global l
    fo.write(" "*s+"<whileStatement>\n")
    s+=2
    fo.write(" "*s+l)  #while
    l=fi.readline()
    lno+=1
    if "(" not in l.split():
        print("Syntax error : ( expected\n")
        sys.exit()
    fo.write(" "*s+l)  #(
    l=fi.readline()
    lno+=1
    compileExpression()   #expression
    if ")" not in l.split():
        print("Syntax error : ) expected\n")
        sys.exit()
    fo.write(" "*s+l)  #)
    l=fi.readline()
    lno+=1
    if l.split()[1] not in ["{"]:
        print("Syntax error : { expected\n")
        sys.exit()
    fo.write(" "*s+l)  #{
    l=fi.readline()
    lno+=1
    compileStatements()  #statements
    if l.split()[1] not in ["}"]:
        print("Syntax error : } expected\n")
        sys.exit()
    fo.write(" "*s+l)   #}
    l=fi.readline()
    lno+=1
    s-=2
    fo.write(" "*s+"</whileStatement>\n")
    return

def compileDoStatement():
    global s,lno
    global l
    fo.write(" "*s+"<doStatement>\n")
    s+=2
    fo.write(" "*s+l)  #do
    l=fi.readline()
    lno+=1
    fo.write(" "*s+l)  #id1
    l=fi.readline()
    lno+=1
    if l.split()[1] in ["."]:
        fo.write(" "*s+l)  #.
        l=fi.readline()
        lno+=1
        fo.write(" "*s+l)  #id2
        l=fi.readline()
        lno+=1
        if "(" not in l.split():
            print("Syntax error : ( expected\n")
            sys.exit()
        fo.write(" "*s+l)  #(
        l=fi.readline()
        lno+=1
        compileExpressionList()   #expressionlist
        if ")" not in l.split():
            print("Syntax error : ) expected\n")
            sys.exit()
        fo.write(" "*s+l)  #)
        l=fi.readline()
        lno+=1
    else:
        if "(" not in l.split():
            print("Syntax error : ( expected\n")
            sys.exit()
        fo.write(" "*s+l)  #(
        l=fi.readline()
        lno+=1
        compileExpressionList()   #expressionlist
        if ")" not in l.split():
            print("Syntax error : ) expected\n")
            sys.exit()
        fo.write(" "*s+l)  #)
        l=fi.readline()
        lno+=1
    if l.split()[1] not in [";"]:
        print("Syntax error : ; expected\n")
        sys.exit()
    fo.write(" "*s+l)   #;
    l=fi.readline()
    lno+=1
    s-=2
    fo.write(" "*s+"</doStatement>\n")
    return

def compileReturnStatement():
    global s,lno
    global l
    fo.write(" "*s+"<returnStatement>\n")
    s+=2
    fo.write(" "*s+l)  #return
    l=fi.readline()
    lno+=1
    if l.split()[1] not in [";"]:
        compileExpression()
    if l.split()[1] not in [";"]:
        print("Syntax error : ; expected\n")
        sys.exit()
    fo.write(" "*s+l)
    l=fi.readline()
    lno+=1#;
    s-=2
    fo.write(" "*s+"</returnStatement>\n")
    return

op=["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]

def compileExpression():
    global s,lno
    global l
    fo.write(" "*s+"<expression>\n")
    s+=2
    compileTerm()   #term
    if l.split()[1] in op:
        fo.write(" "*s+l)  #op
        l=fi.readline()
        lno+=1
        compileTerm()     #term
    s-=2
    fo.write(" "*s+"</expression>\n")
    return

def compileExpressionList():
    global s
    global l,lno
    fo.write(" "*s+"<expressionList>\n")
    s+=2
    while l.split()[1] not in [")"]:
        compileExpression()   #expression
        if l.split()[1] not in [","]:
            break
        fo.write(" "*s+l)  #,
        l=fi.readline()
        lno+=1
    s-=2
    fo.write(" "*s+"</expressionList>\n")
    return

def compileTerm():
    global s
    global l,lno
    fo.write(" "*s+"<term>\n")
    s+=2
    if l.split()[0] in ["<integerConstant>","<stringConstant>","<keyword>"]:
        fo.write(" "*s+l)  
        l=fi.readline()
        lno+=1
    elif l.split()[0] in ["<identifier>"]:
        fo.write(" "*s+l)  
        l=fi.readline()
        lno+=1
        if l.split()[1] in ["["]:
            fo.write(" "*s+l)  #[
            l=fi.readline()
            lno+=1
            compileExpression()
            if l.split()[1] not in ["]"]:
                print("Syntax error : ] expected\n")
                sys.exit()
            fo.write(" "*s+l)  #]
            l=fi.readline()
            lno+=1
        elif l.split()[1] in ["."]:   
            fo.write(" "*s+l)  #.
            l=fi.readline()
            lno+=1
            fo.write(" "*s+l)  #id2
            l=fi.readline()
            lno+=1
            if "(" not in l.split():
                print("Syntax error : ( expected\n")
                sys.exit()
            fo.write(" "*s+l)  #(
            l=fi.readline()
            lno+=1
            compileExpressionList()   #expressionlist
            if ")" not in l.split():
                print("Syntax error : ) expected\n")
                sys.exit()
            fo.write(" "*s+l)  #)
            l=fi.readline()
            lno+=1
        elif l.split()[1] in ["("]:
            fo.write(" "*s+l)  #(
            l=fi.readline()
            lno+=1
            compileExpressionList()   #expressionlist
            if ")" not in l.split():
                print("Syntax error : ) expected\n")
                sys.exit()
            fo.write(" "*s+l)  #)
            l=fi.readline()
            lno+=1
    elif l.split()[1] in ["("]:
        fo.write(" "*s+l)    #(
        l=fi.readline()
        lno+=1
        compileExpression()   #expression
        if ")" not in l.split():
            print("Syntax error : ) expected\n")
            sys.exit()
        fo.write(" "*s+l)  #)
        l=fi.readline()
        lno+=1
    elif l.split()[1] in ["-","~"]:
        fo.write(" "*s+l)  
        l=fi.readline()
        lno+=1
        compileTerm()
    s-=2
    fo.write(" "*s+"</term>\n")
    return

               
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