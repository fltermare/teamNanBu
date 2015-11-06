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
	dataT_merge = []

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
							
			id_new = np.zeros(feature_num)
			for i in indexList:
				id_new = id_new + np.array(dataT[i])
			id_new = id_new / len(indexList)
			dataT_merge.append(list(id_new))
				
			indexList = []
			count = [0]*24
			summ = [0.0]*24
		#else: # no Id changing
			
		index += 1
		
#	dataT_merge = [,dataT_merge]
	outData = [data.columns.tolist()]
	outData.extend(dataT_merge)

	with open('output.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(outData)


	

if __name__ == "__main__":
    main()
