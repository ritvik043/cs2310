# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 17:10:02 2019

@author: Ritvik
"""

import sys
import os

x=sys.argv[1]

for i in range(int(x)):
    os.system("python Compiler.py "+str(sys.argv[i+2])+"\n")