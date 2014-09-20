#Code Adapted from http://stackoverflow.com/questions/12074963/t9-system-to-numpad
import serial
from collections import Counter
import re
import itertools
import time


arduino = serial.Serial('COM4', 115200, timeout=.1)

arrayList = [1]
all_words=Counter()
n2l={2:'qwerty',3:'uilpgh',4:'asdfko',5:'zxcvbnm',6:'',7:'',8:'',9:''}
#n2l={2:'abcxyz',3:'defghij',4:'ghi',5:'jkl',6:'mno',7:'pqrs',8:'tuv',9:''}

with open('dictionary.txt','r') as di:  # UNIX 250k unique word list 
     all_words.update({line.strip() for line in di if len(line) < 6}) 

with open('holmes.txt','r') as fin:   # http://www.gutenberg.org/ebooks/1661.txt.utf-8 (this is used for weight)
    for line in fin:
         all_words.update([word.lower() for word in re.findall(r'\b\w+\b',line)])

def combos(*nums):
    t=[n2l[i] for i in nums]
    return tuple(''.join(t) for t in itertools.product(*(t)))

def t9(*nums):
    combo=combos(*nums)
    c1=combos(nums[0])
    first_cut=(word for word in all_words if word.startswith(c1))
    return (word for word in first_cut if word.startswith(combo) and len(word) == len(nums))

def try_it(*nums):
    s=set(t9(*nums))
    n=10
    print('({}) produces {:,} words. Top {}:'.format(','.join(str(i) for i in nums),
            len(s),min(n,len(s))))
    for i, word in enumerate(
          [w for w in sorted(all_words,key=all_words.get, reverse=True) if w in s],1):
        if i<=n:
            print ('\t{:2}:  "{}" -- weighted {}'.format(i, word, all_words[word]))

def get_word(*word_calculation):
    if (len(word_calculation) == 0):
        done = True
        return ""
    s = set(t9(*word_calculation))
    selected = False
    wordlist = []
    for i, word in enumerate([w for w in sorted(all_words,key=all_words.get, reverse=True) if w in s],1):
        wordlist.append(word)
        print word
    print len(wordlist)
    print "Press 4 to move down, press 1 to move up. Press 2 or 3 to select the word."
    moving_on = False
    i = 0
    while (not selected) and (i < len(wordlist)): 
        while not moving_on:
            second_input = arduino.readline()[:-2]
            if second_input:
                print wordlist[i]
                num = int(second_input)
                if num == 1:
                    moving_on = True
                elif num == 4:
                    i -= 2
                    moving_on = True
                elif num == 3:
                    print wordlist[i] + " added and ended sentence"
                    selected = True
                    return wordlist[i] + ". "
                else:
                    print wordlist[i] + " added"
                    selected = True
                    return wordlist[i]
        i += 1
        moving_on = False




done = False
while not done:
    arrayList = []
    num = -1
    constructed_string = ""
    while num != 0:
        data = arduino.readline()[:-2]
        if data:
            num = int(data)
            if num == 0:
                True
            if num != 1:
                arrayList.append(num)
                try_it(*arrayList)
            elif num == 1:
                constructed_string = constructed_string + get_word(*arrayList) + " "
                print constructed_string
                if get_word(*arrayList) == "":
                    break
                del arrayList[:]
    done = True

