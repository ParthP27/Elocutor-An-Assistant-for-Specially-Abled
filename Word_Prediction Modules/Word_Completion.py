# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 22:45:55 2020

@author: Kaushal Mistry
"""

# import Trie_Structure as trie
import pyautogui as pag

# t = trie.get_root()

# while True:
#     key = input("Enter String : ") # key for autocomplete suggestions. 
#     status = ["Not found", "Found"] 
    
#     comp = t.printAutoSuggestions(key)
    
#     if comp == -1: 
#     	print("No other strings found with this prefix\n") 
#     elif comp == 0: 
#     	print("No string found with this prefix\n")

# from nltk.corpus import wordnet as wn

# print(wn.synsets('dog'))

# import autocomplete

# autocomplete.load()
# x = 'y'

# a = autocomplete.predict_currword(x, 10)
# b = autocomplete.predict('I', 'l', 10)
# print(a)
# print(b)

# s = " "
# print(len(s))
# print(s.isspace())

s = [2,0,1]
print(s.index(2))
s = ('altleft', 'tab')
pag.hotkey(s[0], s[1])