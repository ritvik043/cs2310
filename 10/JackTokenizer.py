# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 19:13:59 2019

@author: Ritvik
"""

import re 
   
regex = '^[A-Za-z_][A-Za-z0-9_]*'

fn = input()

fi = open(fn+".jack", "r")
fo = open(fn+".tok", "w")

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
                fo.write(" "+token[:-2]+" </stringConstant>\n")
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
            print("Invalid token at line "+str(lno))
            break
            
fo.write("</tokens>\n")

fi.close()
fo.close()
        