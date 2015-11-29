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
    print("[*] Read train.csv")
    fw = open(outfile1, 'w')
    print("[*] Deleting missing data")

    lastMin = 0
    lastId = 1

    for line in fp:
        if not re.findall(",,", line) :
            lines = line.strip().split(',')
            currId = lines[0]
            try:
                currMin = int(lines[1])
            except:
                currMin = int(0)

            if currId != lastId or currMin >= lastMin:
                fw.write(','.join(lines))
                fw.write('\n')
                lastId = currId
                lastMin = currMin
            elif currId == lastId and (currMin == 0):
                #minutes_past = 0 but it means 60
                lines[1] = str(60)
                fw.write(','.join(lines))
                fw.write('\n')
                lastMin = 0
            else:
                print("[*]Error: " + line)
                print("lastId: "+lastId+" / lastMin: "+lastMin)
                print("currId: "+currId+" / currMin: "+currMin)
                break

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

    #Merge by minutes_past
    current_id = int(dataT[0][0])
    lastMin = 0
    summ = np.array([0.0]*22)
    numTotol = len(dataT)

    for i in range(0, numTotol):
        tmpID = int(dataT[i][0])
        if tmpID == current_id:
            summ = summ + np.array(dataT[i])[1:-1] * (dataT[i][1] - lastMin)

            if i == numTotol-1:
                avg = dataT[i-1]
                avg[1:-1] = summ/dataT[i][1]
                #dd = np.array(dd, dtype = np.float32)
                #print("[>] summ at line "+ str(i)+":", end = "")
                #print(dd)
                writer.writerows([list(avg)])
            else:
                lastMin = dataT[i][1]
        else :
            avg = dataT[i-1]
            avg[1:-1] = summ/lastMin
            #dd = np.array(dd, dtype = np.float32)
            #dd[0] = int(dd[0])
            #print("[>] summ at line "+ str(i)+":", end = "")
            #print(dd)
            writer.writerows([list(avg)])

            if i == numTotol-1:
                #This ID has only 1 instance and it's the last one
                avg = dataT[i]
                #dd = np.array(dd, dtype = np.float32)
                #print("[>] summ at line "+ str(i)+":", end = "")
                #print(dd)
                writer.writerows([list(avg)])
            else:
                summ = np.array(dataT[i])[1:-1] * dataT[i][1]
                current_id = int(dataT[i][0])
                lastMin = dataT[i][1]

    fw.close()

def main():
    deleteMissing()
    mergeID()


if __name__ == "__main__":
    main()
