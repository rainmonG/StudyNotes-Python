#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   unidecodetest.py
@Time    :   2023/12/14 23:38:54
@Author  :   rainmonG 
@Version :   1.0
@Desc    :   None
'''

import unicodedata
print(unicodedata.normalize('NFKD', 'ñ'.casefold()))