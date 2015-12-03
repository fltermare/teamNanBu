#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import copy
import re
import sys

def deleteMissing(rawfile, tmpfile):
    fp = open(rawfile, 'r')
    print("[*] Read train.csv")
    fw = open(tmpfile, 'w')
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
    print("[>] Deleting finished")

def mergeID(tmpfile, outputfile, setting):
    #merging instance with same id
    fp = pd.read_csv(tmpfile)
    print("[*] Read train without empty")
    data = fp.ix[:,:]
    dataT = data.values.tolist()

    ##name list of  attributes
    fw = open(outputfile, 'w')
    outData = [data.columns.tolist()]
    writer = csv.writer(fw)
    writer.writerows(outData)

    #Merge by minutes_past
    current_id = int(dataT[0][0])
    lastMin = 0
    summ = np.array([0.0]*22)
    numTotol = len(dataT)
    print("[*] Start merging")
    for i in range(0, numTotol):
        tmpID = int(dataT[i][0])
        if tmpID == current_id:
            summ = summ + partId(np.array(dataT[i]), setting) * (dataT[i][1] - lastMin)

            if i == numTotol-1:
                avg = avgId(dataT[i-1], summ/dataT[i][1])
                writer.writerows([list(avg)])
            else:
                lastMin = dataT[i][1]
        else :
            avg = avgId(dataT[i-1], summ/lastMin)
            if lastMin != 0:
                writer.writerows([list(avg)])

            if i == numTotol-1:
                #This ID has only 1 instance and it's the last one
                avg = dataT[i]
                writer.writerows([list(avg)])
            else:
                summ = partId(np.array(dataT[i]), setting) * dataT[i][1]
                current_id = int(dataT[i][0])
                lastMin = dataT[i][1]

    fw.close()
    print("[>] Merging finished")

def partId(thisRow, setting):
    if setting == "train":
        return thisRow[1:-1]
    elif setting == "test":
        return thisRow[1:]
    else:
        print("[-] Error: setting:" + setting)

def avgId(lastRow, averageId):
    avg = lastRow
    for i in range(len(averageId)):
        avg[i+1] = averageId[i]
    return avg

def main():
    if len(sys.argv) != 4:
        print("[-] Usage: python3 preProcData.py [rawfile] [MergedFile] [test|train]")
        print("[*] Execute with default configuration")
        rawfile = "./csv/train.csv"
        tmpfile = "./csv/trainWithoutEmpty.csv"
        outputfile = "./csv/trainMerged.csv"
        setting = "train"

    else:
        rawfile = sys.argv[1]
        tmpfile = "./csv/"+sys.argv[3]+"WithoutEmpty.csv"
        outputfile = sys.argv[2]
        setting = sys.argv[3]
    deleteMissing(rawfile, tmpfile)
    mergeID(tmpfile, outputfile, setting)


if __name__ == "__main__":
    main()
