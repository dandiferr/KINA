#Code Adapted from http://stackoverflow.com/questions/12074963/t9-system-to-numpad
import serial
from collections import Counter
import re
import itertools
import time
import xml.etree.ElementTree as ET
import socket               # Import socket module

arduino = serial.Serial('COM4', 115200, timeout=.1)

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 15669                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.       
    arrayList = [1]
    all_words=Counter()
    n2l={2:'qwerty',3:'uilpgh',4:'asdfko',5:'zxcvbnm',6:'',7:'',8:'',9:''}
    #n2l={2:'abcxyz',3:'defghij',4:'ghi',5:'jkl',6:'mno',7:'pqrs',8:'tuv',9:''}

    with open('google-10000-english.txt','r') as di:  # UNIX 250k unique word list 
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
        wordlist = []
        for i, word in enumerate([w for w in sorted(all_words,key=all_words.get, reverse=True) if w in s],1):
            wordlist.append(word)
        if len(wordlist) > 0:
            return wordlist[0]
        else:
            return "No matches, continue"

    def get_word(*word_calculation):
        if (len(word_calculation) == 0):
            done = True
            return ""
        s = set(t9(*word_calculation))
        isInRotation.text = "1"
        c.send(ET.tostring(root, encoding="us-ascii", method="xml"))
        selected = False
        wordlist = []
        for i, word in enumerate([w for w in sorted(all_words,key=all_words.get, reverse=True) if w in s],1):
            wordlist.append(word)
        moving_on = False
        i = 0
        while (not selected) and (i < len(wordlist)): 
            while not moving_on:
                second_input = arduino.readline()[:-2]
                if second_input:
                    num = int(second_input)
                    if num == 1:
                        moving_on = True
                        c.send(ET.tostring(root, encoding="us-ascii", method="xml"))
                    elif num == 4:
                        i -= 2
                        moving_on = True
                        c.send(ET.tostring(root, encoding="us-ascii", method="xml"))
                    elif num == 3:
                        selected = True
                        return wordlist[i] + "."
                    else:
                        selected = True
                        return wordlist[i]
            i += 1
            moving_on = False
        return ""

        root = ET.Element("T9Response")
        curString = ET.SubElement(root, "CurString")
        curString.text = ""
        curWord = ET.SubElement(root, "CurWord")
        isInRotation = ET.SubElement(root, "IsInRotation")
        isInRotation.text = "0"
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
                        curWord.text = try_it(*arrayList)
                        c.send(ET.tostring(root, encoding="us-ascii", method="xml"))
                    elif num == 1:
                        csold = constructed_string
                        newWord = get_word(*arrayList)
                        constructed_string = constructed_string + newWord + " "
                        curString.text = constructed_string
                        isInRotation.text = "0"
                        if len(csold) == len(constructed_string) - 1:
                            break
                        c.send(ET.tostring(root, encoding="us-ascii", method="xml"))
                        del arrayList[:]
            done = True
        c.send(ET.tostring(root, encoding="us-ascii", method="xml"))

