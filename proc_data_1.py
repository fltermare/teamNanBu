#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys

infile="~/Documents/kaggle/train3.csv"
#outfile="~/Documents/kaggle/proc_train.csv"

def main():
    fp = pd.read_csv(infile)
    data = fp.ix[:,:].fillna("NA")
    dataT = data.values.tolist()

    current_id = 1
    count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    summ = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    current_arr = np.zeros(23)

#    for x in range(2,5):
#        print(x)


    for instance in dataT:
        for i in range(0,23):
            if str(instance[i]) != "NA":
                count[i] += 1
                summ[i] += instance[i]


    for i in range(0,23):
        if count[i] != 0:
            summ[i] /= count[i]

    for instance in dataT:
        for i in range(0,23):
            if (str(instance[i]) == "NA"):
                instance[i] = summ[i]

    #print(str(instance[6]).isdigit())
    #print(dataT)

    with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(dataT)

if __name__ == "__main__":
    main()
