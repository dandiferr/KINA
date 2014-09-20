#Code Aadapted from http://stackoverflow.com/questions/12074963/t9-system-to-numpad

from collections import Counter
import re
import itertools 


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

            

num = 6
while num != 0:
    num = raw_input("put your input ")
    arayList = list(num)
    arrayList = [int(i) for i in arayList]
    
    if len(arrayList) == 1:
        try_it(int(arrayList[0]))
    if len(arrayList) == 2:
         try_it(int(arrayList[0]), int(arrayList[1]))
    if len(arrayList) == 3:
         try_it(int(arrayList[0]), int(arrayList[1]), int(arrayList[2]))
    if len(arrayList) == 4:
        try_it(int(arrayList[0]), int(arrayList[1]), int(arrayList[2]), int(arrayList[3]))
    if len(arrayList) == 5:
        try_it(int(arrayList[0]), int(arrayList[1]), int(arrayList[2]), int(arrayList[3]), int(arrayList[4]))
    if len(arrayList) == 6:
        try_it(int(arrayList[0]), int(arrayList[1]), int(arrayList[2]), int(arrayList[3]), int(arrayList[4]), int(arrayList[5]))
    if len(arrayList) == 7:
        try_it(int(arrayList[0]), int(arrayList[1]), int(arrayList[2]), int(arrayList[3]), int(arrayList[4]), int(arrayList[5]), int(arrayList[6]))    
    if len(arrayList) == 8:
        try_it(int(arrayList[0]), int(arrayList[1]), int(arrayList[2]), int(arrayList[3]), int(arrayList[4]), int(arrayList[5]), int(arrayList[6]), int(arrayList[7]))

