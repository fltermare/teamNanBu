#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys
import re



def DBZ(infile,outfile):
    fp = pd.read_csv(infile)
    print("[*] Read trainMerged")
    data = fp.ix[:,:]
    dataT = data.values.tolist()
    
    ##name list of  attributes
    fw = open(outfile, 'w')
    outData = [data.columns.tolist()]
    writer = csv.writer(fw)
    writer.writerows(outData)
    #print(outData[0])
    
    #replace target by the DBZ formula
    #print("[*] Delete (Expected - Formula) smaller than 5 mm/hr")
    
    for i in range(0,len(dataT)):
        dbz = dataT[i][3]
        est = pow(pow(10, dbz/10)/200, 0.625) # mm per hour
        delta = dataT[i][-1] - est #(Expected - Formula)
        lw = dataT[i][:-1] # list to be written
        lw.append(delta)
        #lw_original = dataT[i]
        #if delta<5:
        writer.writerows([lw])
    fw.close()
    print("[*] Done")
    print("[>] Output to %s"%outfile)
def main():
    infile=None
    outfile=None
    if len(sys.argv) != 3:
        print("[-] Usage: python3 processDBZ.py [MergedFile] [Output File]" )
        print("[*] Execute with default configuration")
        infile = "./csv/trainMerged.csv"
        outfile = "./csv/trainDBZ.csv"

    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    DBZ(infile,outfile)

if __name__ == "__main__":
    main()
