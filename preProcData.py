#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys
import re

infile="./csv/train.csv"
outfile="./csv/trainWithoutEmpty.csv"

def main():
    fp = open(infile, 'r')
    fw = open(outfile, 'w')
    print("[*] Read raw training data")
    for line in fp:
        if not re.findall(",,", line):
            fw.write(line)
    fw.close()
    fp.close()
    print("[*] Done")

if __name__ == "__main__":
    main()
