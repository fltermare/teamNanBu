#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import copy
import re
import sys

def deleteMissing(inputfile, tmpfile, setting, indexlist):
    fp = open(inputfile, 'r')
    print("[*] Read "+inputfile)
    fw = open(tmpfile, 'w')
    print("[*] Deleting missing data")

    lastMin = 0
    lastId = 1

    for line in fp:
        lines = line.strip().split(',')
        #if not re.findall(",,", line) :
        if validOrNot(lines, setting, indexlist):
            currId = lines[0]
            try:
                currMin = int(lines[1])
            except:
                currMin = int(0)
            #0 means 0 or 60
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

def validOrNot(lines, setting, indexlist):
    #empty check
    for i in indexlist:
        if not lines[i]:
            return False

    if setting == "test":
        return True

    #rainfall < 70 mm/hr
    try :
        if float(lines[-1]) > 70:
            return False
    except:
        if lines[-1] != "Expected":
            print("[-] Error:"+lines[-1])

    return True

def mergeID(tmpfile, outputfile, setting, indexlist):
    #merging instance with same id
    fp = pd.read_csv(tmpfile)
    print("[*] Read train without empty")
    #data = fp.ix[:,:]

    if setting == "train":
        #adding Id, minutes_past, dbz, Expected (train)
        data = fp.iloc[:,[0,1]+indexlist+[-2,-1]]
    else:
        #adding Id, minutes_past, dbz (test)
        data = fp.iloc[:,[0,1]+indexlist+[-1]]
    dataT = data.values.tolist()
    print(len(dataT[0]))
    #name list of  attributes
    fw = open(outputfile, 'w')
    outData = [data.columns.tolist()]
    writer = csv.writer(fw)
    writer.writerows(outData)
    print(outData)
    print(len(outData[0]))
    #exit()

    #Merge by minutes_past
    current_id = int(dataT[0][0])
    lastMin = 0
    if setting == "train":
        summ = np.array([0.0]*(len(dataT[0])-3))
    else:
        summ = np.array([0.0]*(len(dataT[0])-2))
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
        return thisRow[1:-2]
    elif setting == "test":
        return thisRow[1:-1]
    else:
        print("[-] Error: setting:" + setting)

def avgId(lastRow, averageId):
    avg = lastRow
    for i in range(len(averageId)):
        avg[i+1] = averageId[i]
    return avg

def main():
    if len(sys.argv) != 5:
        print("[-] Usage: python3 preProcData.py [inputfile] [MergedFile] [test|train] [indexOfAttributes]")
        print("[-] Example : python3 preProcData.py ./csv/train_append_dbz.csv ./csv/trainMerged.csv train 2,3,5,6,7,9,10,11,15,17,18")
        print("[*] Execute with default configuration")
        inputfile = "./csv/train_append_dbz.csv"
        tmpfile = "./csv/trainWithoutEmpty.csv"
        outputfile = "./csv/trainMerged.csv"
        setting = "train"
        indexlist = [2, 3, 5, 6, 7, 9, 10, 11, 15, 17, 18]
    else:
        inputfile = sys.argv[1]
        tmpfile = "./csv/"+sys.argv[3]+"WithoutEmpty.csv"
        outputfile = sys.argv[2]
        setting = sys.argv[3]
        indexlist = [int(x) for x in list(sys.argv[4].strip().split(',')) ]

    deleteMissing(inputfile, tmpfile, setting, indexlist)
    mergeID(tmpfile, outputfile, setting, indexlist)


if __name__ == "__main__":
    main()
