# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 18:41:10 2020

@author: Charan C
"""

import os
from os import strerror
import sys
import time
import datetime
from gtts import gTTS
from tika import parser
from threading import Thread


def displayTime():
    sec = 0
    symb = ['/', '-', '\\', '']
    
    print("")
    
    while True:
        for symb_ in symb:
            sys.stdout.write('\rCreating audiobook - {0} {1} '.format(datetime.timedelta(seconds=sec), symb_))
            sys.stdout.flush()
            time.sleep(0.25)
        sec += 1 
        
        global stopDisplayTime, printMsg
        if stopDisplayTime: 
            print('\n\n' + printMsg)
            break
    
def stopDisplayTimeThread(msg):
    global stopDisplayTime, printMsg
    printMsg = msg
    stopDisplayTime = True
    # thread killed
    
def stopAudioGeneratorTTsTread():
    sys.exit()
    # thread killed

def audioGeneratorTTS(filePath, txt):
    try:
        tts = gTTS(txt, lang='en', slow=False)
        tts.save(filePath.replace('.pdf', '.mp3'))
        stopDisplayTimeThread('Audiobook created successfully')
    except Exception:
       print("Failed to establish a new connection")
       stopDisplayTimeThread('Audiobook creation failed')
    finally:
        stopAudioGeneratorTTsTread()
    

try:
    close = True

    folderPath = input('Enter the folder path: ')
    fileName = input('Enter pdf file name: ')

    if not fileName.endswith('.pdf'):
        fileName += '.pdf'

    filePath = os.path.join(folderPath ,fileName)
    
    parsedPDF = parser.from_file(filePath)
    pdfText = parsedPDF['content']
    txt = pdfText.replace('\n', '')
    
    stopDisplayTime = False
    stopAudioGeneratorTTS = False
    printMsg = ''
     
    a = Thread(target = displayTime)
    b = Thread(target = audioGeneratorTTS, args = (filePath, txt))
    a.start()
    b.start()
    
    while True:
        if not a.is_alive():
            close = False
            input("Press any key to exit")
            sys.exit()
        
except IOError as ioe:
    print('I/o error occured: ', strerror(ioe.errno))
except Exception as e:
    print(e)
finally:
    while close:
        input("Press any key to exit")
        sys.exit()
            
