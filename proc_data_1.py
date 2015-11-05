#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys

infile="../trainless.csv"
#outfile="~/Documents/kaggle/proc_train.csv"


def main():
	fp = pd.read_csv(infile)
	data = fp.ix[:,:].fillna("NA")
	dataT = data.values.tolist()

	current_id = dataT[0][0]
	count = [0]*24
	summ = [0.0]*24
	current_arr = np.zeros(23)

#    for x in range(2,5):
#        print(x)


	index = 0
	indexList = []
	while index <len(dataT):
		instance = dataT[index]
		feature_num = len(instance)
		current_id = instance[0]
		next_id = False
		indexList.append(index)
		if index +1 <len(dataT):
			next_id = dataT[index+1][0]
			
		for i in range(feature_num):
			if str(instance[i])!="NA":
				count[i] += 1
				summ[i] += instance[i]
		if next_id == False or next_id != current_id: # EOF or Change Id
			for i in indexList:
				inst = dataT[i]
				for j,col in enumerate(inst):
					if str(col) == 'NA':
						try:
							inst[j] = summ[j]/count[j] 
						except:
							inst[j] = 0
			indexList = []
			count = [0]*24
			summ = [0.0]*24
		#else: # no Id changing
			
		index += 1
		

	with open('output.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(dataT)
'''
    for i in range(0,23):
        if count[i] != 0:
            summ[i] /= count[i]

    for instance in dataT:
        for i in range(24):
            if (str(instance[i]) == "NA"):
                instance[i] = summ[i]
'''
    #print(str(instance[6]).isdigit())
    #print(dataT)

	

if __name__ == "__main__":
    main()
