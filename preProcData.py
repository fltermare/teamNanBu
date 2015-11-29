#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys
import re

infile="./csv/train.csv"
outfile1="./csv/trainWithoutEmpty.csv"
outfile2="./csv/trainMerged.csv"
outfile3="./csv/trainDBZ.csv"
def deleteMissing():
    fp = open(infile, 'r')
    fw = open(outfile1, 'w')
    print("[*] Read raw training data")
    print("[*] Deleting missing data")
    for line in fp:
        if not re.findall(",,", line):
            fw.write(line)
    fw.close()
    fp.close()
    print("[*] Done")

def mergeID():
    #merging instance with same id
    fp = pd.read_csv(outfile1)
    print("[*] Read trainWithoutEmpty")
    data = fp.ix[:,:]
    dataT = data.values.tolist()

    ##name list of  attributes
    fw = open(outfile2, 'w')
    outData = [data.columns.tolist()]
    writer = csv.writer(fw)
    writer.writerows(outData)
    #print(outData[0])

    #Merge by minutes_past
    current_id = int(dataT[0][0])
    lastMin = dataT[0][1]
    avg = np.array([0.0]*22)
    numTotol = len(dataT)

    for i in range(0, numTotol):
        tmpID = int(dataT[i][0])
        if tmpID == current_id:
            avg = avg + np.array(dataT[i])[1:-1] * (dataT[i][1] - lastMin)

            if i == numTotol-1:
                dd = dataT[i-1]
                dd[1:-1] = avg/dataT[i][1]
                #print("[>] avg at line "+ str(i)+":", end = "")
                #print(dd)
                writer.writerows([list(dd)])
            else:
                lastMin = dataT[i][1]
        else :
            dd = dataT[i-1]
            dd[1:-1] = avg/lastMin
            #print("[>] avg at line "+ str(i)+":", end = "")
            #print(dd)
            writer.writerows([list(dd)])

            if i == numTotol-1:
                #print("[>] avg at line "+ str(i)+":", end = "")
                #print(dataT[i])
                writer.writerows([list(dataT[i])])
            else:
                avg = np.array(dataT[i])[1:-1] * dataT[i][1]
                current_id = int(dataT[i][0])
                lastMin = dataT[i][1]

    fw.close()
    print("[*] Done")

def DBZ():
    fp = pd.read_csv(outfile2)
    print("[*] Read trainMerged")
    data = fp.ix[:,:]
    dataT = data.values.tolist()
    
    ##name list of  attributes
    fw = open(outfile3, 'w')
    outData = [data.columns.tolist()]
    writer = csv.writer(fw)
    writer.writerows(outData)
    #print(outData[0])
    
    #replace target by the DBZ formula
    print("[*] Delete (Expected - Formula) smaller than 5 mm/hr")
    for i in range(0,len(dataT)):
        dbz = dataT[i][3]
        est = mmperhr = pow(pow(10, dbz/10)/200, 0.625)
        delta = dataT[i][-1] - est #(Expected - Formula)
        lw = dataT[i][:-1] # list to be written
        lw.append(delta)
        if delta<5:
            writer.writerows([lw])
    fw.close()
    print("[*] Done")
    
def main():
    #deleteMissing()
    #mergeID()
    DBZ()

if __name__ == "__main__":
    main()
