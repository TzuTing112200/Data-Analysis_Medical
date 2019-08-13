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


# In[ ]:


'''
read features and functions
'''


# In[ ]:


features = {}
rf = open('features.json', 'r')
for r in rf.readlines():
    temp = json.loads(r)
    for t in temp.items():
        features[t[0]] = json.loads(t[1])
rf.close()


# In[ ]:


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False


# In[ ]:


def getObjectData(GUID, ORBGNDT):
    resultData = [-100]*len(SYB_NAME)
    oTime = datetime.datetime(int(ORBGNDT[0:4]), int(ORBGNDT[4:6]) , int(ORBGNDT[6:9]))
    
    if GUID not in features:
        return resultData
	
    for f in features[GUID]:
        if 'O_' + f in SYB_NAME:
            
            data = features[GUID][f]
            temp = -1
            tempDif = -1
            for d in data:
                value = d[0]
                if len(value)>1 and value[-1] == '%':
                    value=value[:-1]
                if not is_number(str(value)):
                    continue
                if len(d[1]) < 1:
                    continue
                if d[1][0]!='|' or d[1][-1]!='|':
                    continue
                    
                value = float(value)
                time = d[1][1:-1]
                if time[0] == '*':
                    time = time[1:]
                time = datetime.datetime(int(time[0:4]), int(time[4:6]) , int(time[6:9]))
                td = abs((oTime - time).days)
                
                if tempDif == -1:
                    temp = value
                    tempDif = td
                elif tempDif > td:
                    temp = value
                    tempDif = td

                if SYB_NAME['O_' + f][2] == 0:
                    temp = 0
                else:
                    temp = float('%.6f' % ((temp-SYB_NAME['O_' + f][1])/SYB_NAME['O_' + f][2]))
            
            resultData[SYB_NAME['O_' + f][0]]=temp
    
    return resultData


# In[ ]:


'''
get lab's sybName
'''


# In[ ]:


# get SYB_NAME id
SYB_NAME = {}
with open('Lab-201801-20190316191848551.csv', newline='', encoding = 'utf8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if not is_number(row['SYB_VALUE']):
            continue
        value = float(row['SYB_VALUE'])
            
        if row['SYB_NAME'] not in SYB_NAME:
            SYB_NAME[row['SYB_NAME']]=(value,value,0)    
        elif value>SYB_NAME[row['SYB_NAME']][1]:
            SYB_NAME[row['SYB_NAME']]=(SYB_NAME[row['SYB_NAME']][0],value,0)
        elif value<SYB_NAME[row['SYB_NAME']][0]:
            SYB_NAME[row['SYB_NAME']]=(value,SYB_NAME[row['SYB_NAME']][1],0)


# In[ ]:


with open('Lab-201801-20190316191848551.csv', newline='', encoding = 'utf8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if not is_number(row['SYB_VALUE']) and row['SYB_NAME'] in SYB_NAME:
            del SYB_NAME[row['SYB_NAME']]


# In[ ]:


'''
get features' sybName
'''


# In[ ]:


rf = open('features.json', 'r')
for r in rf.readlines():
    temp = json.loads(r)
    for t in temp.items():
        dataDic = json.loads(t[1])
    for d in dataDic:
        for dd in dataDic[d]:
            value = dd[0]
            if len(value)>1 and value[-1] == '%':
                value=value[:-1]
            if not is_number(value):
                continue
            value = float(value)
            
            if 'O_' + d not in SYB_NAME:
                SYB_NAME['O_' + d]=(value,value,0)    
            elif value>SYB_NAME['O_' + d][1]:
                SYB_NAME['O_' + d]=(SYB_NAME['O_' + d][0],value,SYB_NAME['O_' + d][2]+1)
            elif value<SYB_NAME['O_' + d][0]:
                SYB_NAME['O_' + d]=(value,SYB_NAME['O_' + d][1],SYB_NAME['O_' + d][2]+1)
            else:
                SYB_NAME['O_' + d]=(SYB_NAME['O_' + d][0],SYB_NAME['O_' + d][1],SYB_NAME['O_' + d][2]+1)
        
rf.close()


# In[ ]:


rf = open('features.json', 'r')
for r in rf.readlines():
    temp = json.loads(r)
    for t in temp.items():
        dataDic = json.loads(t[1])
    for d in dataDic:
        for dd in dataDic[d]:
            if 'O_' + d in SYB_NAME:
                value = dd[0]
                if len(value)>1 and value[-1] == '%':
                    value=value[:-1]
                if len(d)>10 or SYB_NAME['O_' + d][2]<10 or not is_number(value) or len(dd) != 2:
                    del SYB_NAME['O_' + d]
rf.close()


# In[ ]:


'''
get sybName's index and normalize parameter
'''


# In[ ]:


i=0
for sn in SYB_NAME:
    SYB_NAME[sn]=(i, SYB_NAME[sn][0], (SYB_NAME[sn][1]-SYB_NAME[sn][0]))
    i += 1


# In[ ]:


'''
computer each encntno
'''


# In[ ]:


ENCNTNO = {}
with open('Lab-201801-20190316191848551.csv', newline='', encoding = 'utf8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if row['SYB_NAME'] not in SYB_NAME:
            continue
        
        if not is_number(row['SYB_VALUE']):
            continue
		
        temp = float(row['SYB_VALUE'])
        if SYB_NAME[row['SYB_NAME']][2] == 0:
            temp = 0
        else:
            temp = float('%.6f' % ((temp-SYB_NAME[row['SYB_NAME']][1])/SYB_NAME[row['SYB_NAME']][2]))

        if row['ENCNTNO'] not in ENCNTNO:
            ENCNTNO[row['ENCNTNO']] = getObjectData(row['VGHTC_GUID'], row['ORBGNDT'])
            
        ENCNTNO[row['ENCNTNO']][SYB_NAME[row['SYB_NAME']][0]]=temp


# In[ ]:


'''
record the encntno's MainDiagCode
'''


# In[ ]:


for e in ENCNTNO:
    ENCNTNO[e] = (ENCNTNO[e], -1, -1)


# In[ ]:

DiagCodes = {}
with open('EncntIDX-201801-20190316175828390.csv', newline='', encoding = 'utf8') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if row['OPDSectionNMC'] != OPDSectionNMC:
            continue
        MainDiagCode = row['MainDiagCode']
        if MainDiagCode[:4] != MainDiagCodeTitle:
            continue
        MainDiagCode = MainDiagCode[4:]
        if MainDiagCode not in DiagCodes:
            index = len(DiagCodes)
            DiagCodes[MainDiagCode] = index
        if row['ENCNTNO'] in ENCNTNO:
            ENCNTNO[row['ENCNTNO']] = (ENCNTNO[row['ENCNTNO']][0], int(MainDiagCode[0]), DiagCodes[MainDiagCode])


# In[ ]:

ketList = []
for e in ENCNTNO:
	ketList.append(e)

for k in ketList:
    if ENCNTNO[k][1] == -1:
        del ENCNTNO[k]


# In[ ]:


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
for i in range(len(SYB_NAME)):
    for s in SYB_NAME:
        if SYB_NAME[s][0] == i:
            jsObj.append(str(i) + '：  \t' + s)
            break
jsObj = '\n'.join(jsObj)
fileObject = open('Classifier_ItemNames.json', 'w')
fileObject.write(jsObj)
fileObject.close()


# In[ ]:


jsObj = []
for i in range(len(DiagCodes)):
    for d in DiagCodes:
        if DiagCodes[d] == i:
            jsObj.append(str(i) + '：  \t' + d)
            break
jsObj = '\n'.join(jsObj)
fileObject = open('Classifier_DiagCodes.json', 'w')
fileObject.write(jsObj)
fileObject.close()