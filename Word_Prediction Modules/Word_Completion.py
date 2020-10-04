# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 22:45:55 2020

@author: Kaushal Mistry
"""

import Trie_Structure as trie

t = trie.get_root()

while True:
    key = input("Enter String : ") # key for autocomplete suggestions. 
    status = ["Not found", "Found"] 
    
    comp = t.printAutoSuggestions(key)
    
    if comp == -1: 
    	print("No other strings found with this prefix\n") 
    elif comp == 0: 
    	print("No string found with this prefix\n")