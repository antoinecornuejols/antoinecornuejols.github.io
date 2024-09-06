#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 18:25:30 2024

@author: antoinecornuejols
"""

import sys, re

#pattern = "([\\w.-]+@[\\w-]+(\\.[\\w-]+)*)"
pattern = "([\\w.-]+@[\\w-]+(\\.[\\w-]+)*)(.*)"
#for arg in sys.argv[1:]:
# input = open(arg, 'r')
#for line in input:
for line in sys.stdin:
    m = re.search(pattern, line)
    if m :
        address = m.group(1)
        print(address)
#input.close()
