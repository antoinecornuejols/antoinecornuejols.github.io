#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 18:25:30 2024

@author: antoinecornuejols
"""

import sys, re

pattern = "([\w\.]+@[\w]+(\.[\w]+)*)(.*)"
for line in sys.stdin:
    while line:
        m = re.search(pattern, line)
        if m :
            address = m.group(1)
            remainder = m.group(3)
            print(address)
            line = remainder
#            print(remainder)
        else:
            line = None
