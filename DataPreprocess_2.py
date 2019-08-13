#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import csv
import json
import datetime
import numpy as np


# In[ ]:


'''change OPDSectionNMC here'''
OPDSectionNMC = '新陳代謝'
MainDiagCodeTitle = 'E11.'
DiagCodeIndex = ['DiagCode1', 'DiagCode2', 'DiagCode3', 'DiagCode4', 'DiagCode5', 'DiagCode6', 'DiagCode7']


# In[ ]:


print(1)
'''
get EncntIDX's DiagCode
'''


# In[ ]:


DiagCode = {}
with open('EncntIDX-201801-20190316175828390.csv', newline = '', encoding = 'utf8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
	
        if not row['OPDSectionNMC'] == OPDSectionNMC:
            continue
        
        for i in range(7):
            if row[DiagCodeIndex[i]] == '':
                break
            elif row[DiagCodeIndex[i]] not in DiagCode:
                index = len(DiagCode)
                DiagCode[row[DiagCodeIndex[i]]] = index


# In[ ]:


print(2)
'''
get encntno
'''


# In[ ]:

aa=0
ENCNTNO = {}
MainDiagCodes = {}
with open('EncntIDX-201801-20190316175828390.csv', newline = '', encoding = 'utf8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
	
        if not row['OPDSectionNMC'] == OPDSectionNMC:
            continue
        
        if row[DiagCodeIndex[0]] == '':
            continue

        MainDiagCode = row['MainDiagCode']
        if MainDiagCode[:4] != MainDiagCodeTitle:
            aa += 1
            continue
			
        MainDiagCode = MainDiagCode[4:]
        if MainDiagCode not in MainDiagCodes:
            index = len(MainDiagCodes)
            MainDiagCodes[MainDiagCode] = index

        ENCNTNO[row['ENCNTNO']] = ([False] * len(DiagCode), int(MainDiagCode[0]), MainDiagCodes[MainDiagCode])
        for i in range(7):
            if row[DiagCodeIndex[i]] == '':
                break
            elif row[DiagCodeIndex[i]] in DiagCode:
                ENCNTNO[row['ENCNTNO']][0][DiagCode[row[DiagCodeIndex[i]]]] = True

print(aa)
# In[ ]:


print(3)
'''
write file
'''


# In[ ]:


jsObj = '\n'.join([json.dumps({e:ENCNTNO[e]}) for e in ENCNTNO])
fileObject = open('Classifier.json', 'w')
fileObject.write(jsObj)
fileObject.close()


# In[ ]:


jsObj = []
for i in range(len(DiagCode)):
    for s in DiagCode:
        if DiagCode[s] == i:
            jsObj.append(str(i) + '：  \t' + s)
            break
jsObj = '\n'.join(jsObj)
fileObject = open('Classifier_ItemNames.json', 'w')
fileObject.write(jsObj)
fileObject.close()


# In[ ]:


jsObj = []
for i in range(len(MainDiagCodes)):
    for d in MainDiagCodes:
        if MainDiagCodes[d] == i:
            jsObj.append(str(i) + '：  \t' + d)
            break
jsObj = '\n'.join(jsObj)
fileObject = open('Classifier_MainDiagCodes.json', 'w')
fileObject.write(jsObj)
fileObject.close()


# In[ ]:


print(4)
'''
end
'''


# In[ ]: