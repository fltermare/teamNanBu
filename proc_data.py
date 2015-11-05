#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys

infile="~/Documents/kaggle/traincc.csv"
#outfile="~/Documents/kaggle/proc_train.csv"

def main():
    fp = pd.read_csv(infile)
    data = fp.ix[:,:].fillna(0)
    dataT = data.values.tolist()
    print(len(dataT))

    dataout = []

    current_id = 1
    current_len = 0
    current_arr = np.zeros(23)
    for row in dataT:
        current_len+=1
        attr = np.array(row[1:])
        if int(row[0] ) == current_id:
            current_arr = current_arr +attr
        else: # next id
            current_arr /= (current_len-1)
            current_arr = np.append(np.array([current_id]) ,current_arr)
            dataout.append(list(current_arr))
            current_id = row[0]
            current_len = 1
            current_arr = attr
    current_arr /= current_len
    current_arr = np.append(np.array([current_id]) ,current_arr)
    dataout.append(list(current_arr))
    current_id = row[0]
    current_len = 1
    current_arr = attr
    #print(fp.columns.tolist())
    #exit()
    dataout = dataout[::-1]
    dataout.append(fp.columns.tolist())
    dataout = dataout[::-1]
    print(dataout)
    for row in dataout:
        print(row)
    with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(dataout)



if __name__ == "__main__":
    main()
