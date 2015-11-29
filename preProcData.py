#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys
import re

infile="./csv/train.csv"
outfile1="./csv/trainWithoutEmpty.csv"
outfile2="./csv/trainMerged.csv"
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
    print(outData[0])

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
                print("[>] avg at line "+ str(i)+":", end = "")
                print(dd)
                writer.writerows([list(dd)])
            else:
                lastMin = dataT[i][1]
        else :
            dd = dataT[i-1]
            dd[1:-1] = avg/lastMin
            print("[>] avg at line "+ str(i)+":", end = "")
            print(dd)
            writer.writerows([list(dd)])

            if i == numTotol-1:
                print("[>] avg at line "+ str(i)+":", end = "")
                print(dataT[i])
                writer.writerows([list(dataT[i])])
            else:
                avg = np.array(dataT[i])[1:-1] * dataT[i][1]
                current_id = int(dataT[i][0])
                lastMin = dataT[i][1]

    fw.close()

def main():
    deleteMissing()
    mergeID()


if __name__ == "__main__":
    main()
