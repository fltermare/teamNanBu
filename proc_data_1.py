#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import sys

def main():
	infile = sys.argv[1]
	outfile = sys.argv[2]
	fp = pd.read_csv(infile)
	print("blabla")
	data = fp.ix[:,:].fillna("NA")
	dataT = data.values.tolist()
	dataT_merge = []


	f = open(outfile, 'w')
	outData = [data.columns.tolist()]
	writer = csv.writer(f)
	writer.writerows(outData)

	current_id = dataT[0][0]
	count = [0]*24
	summ = [0.0]*24
	current_arr = np.zeros(23)

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
			writer.writerows([list(id_new)])
			#dataT_merge.append(list(id_new))

			indexList = []
			count = [0]*24
			summ = [0.0]*24
		#else: # no Id changing

		index += 1

	f.close()
	#outData = [data.columns.tolist()]
	#print(outData)
	#outData.extend(dataT_merge)

	#with open(outfile, 'w') as f:
	#	writer = csv.writer(f)
	#	writer.writerows(outData)

if __name__ == "__main__":
    main()
