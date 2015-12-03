#!/usr/bin/env python
#
#  Python program that will create the sample solution
#
#  @author: lak@climate.com
#  @version: $Id:$
#
#  you may have to install the master branch of 'dask' using:
#     pip install --upgrade git+https://github.com/blaze/dask
#

#import dask.dataframe as dd
import pandas as pd
import numpy as np
import sys
import csv

# change the location of the downloaded test file as necessary.

# Make sure you are using 64-bit python.
if sys.maxsize < 2**32:
    print ("You seem to be running on a 32-bit system ... this dataset might be too large.")
else:
    print ("Hurray! 64-bit.")

# read file


#alldata = dd.read_csv(infile)
#alldata = alldata.set_index('Id')

def interpolation(ref_list,valid_time_list,number=100):
    ans_valid_time = np.array([valid_time_list[0]])
    ans_ref = np.array([ref_list[0]])
    
    #ref_list_extend = np.append(np.append(np.array([0]),ref_list),60)
    
    for dbzprev ,timeprev ,dbznext ,timenext in zip(ref_list[:-1],valid_time_list[:-1],ref_list[1:],valid_time_list[1:]):
    
        dbzval = np.array([dbzprev, dbznext])
        
        timeval = np.empty(number+1) #len = 101
        timeval[:] = timenext/(number+1)
        #timeval = np.append(t)
        
        x = np.array([0 ,1])
        xsmp = np.linspace(0,1,num=number,endpoint=False)
        dbz_interp = np.interp(xsmp,x,dbzval)[1:] #len = 101-1 =100
        #time_interp = np.interp(xsmp,x,timeval)[1:] #len = 101-1 =100
        ans_ref = np.append(ans_ref,dbz_interp)
        ans_valid_time = np.append(ans_valid_time,timeval)
    
    return (ans_ref,ans_valid_time)

def marshall_palmer(ref, minutes_past):
    #print "Estimating rainfall from {0} observations".format(len(minutes_past))
    # how long is each observation valid?
    valid_time = np.zeros_like(minutes_past)
    valid_time[0] = minutes_past[0]
    for n in range(1, len(minutes_past)):
        valid_time[n] = minutes_past[n] - minutes_past[n-1]
    valid_time[-1] = valid_time[-1] + 60 - np.sum(valid_time)
    valid_time = valid_time / 60.0

    # sum up rainrate * validtime
    
    rf,vt = interpolation(ref,valid_time,number=100)
    sum = 0
    #for dbz, hours in zip(ref, valid_time):
    for dbz, hours in zip(rf, vt):
        # See: https://en.wikipedia.org/wiki/DBZ_(meteorology)
        if np.isfinite(dbz): # handle NaN here
            mmperhr = pow(pow(10, dbz/10)/200, 0.625)
            sum = sum + mmperhr * hours
    return sum


# each unique Id is an hour of data at some gauge
def myfunc(hour):
    
    #rowid = hour['Id'].iloc[0]
    # sort hour by minutes_past
    #hour = hour.sort('minutes_past', ascending=True)
    
    if len(hour['Ref'])>0:
        est = marshall_palmer(hour['Ref'], hour['minutes_past'])
        return est
    else:
        return 0.0254

# this writes out the file, but there is a bug in dask
# where the column name is '0': https://github.com/blaze/dask/pull/621
#estimates = alldata.groupby(alldata.index).apply(myfunc, columns='Expected')
#estimates.to_csv(outfile, header=True)

def main():
    infile="train.csv"
    outfile="sample_solution_hd100_train.csv"
    
    fp = pd.read_csv(infile)
    time = fp['minutes_past'].values.tolist()
    ref = fp['Ref'].values.tolist()
    ID = fp['Id'].values.tolist()
    
    fw = open(outfile, 'w')
    writer = csv.writer(fw)
    
    print('[*] Open file success.')
    print('[*] Calculating...')
    
    newID = []
    expected = []
    hour = {'Ref':np.array([]),'minutes_past':np.array([])}
    for i, Idp,Idn,reflect,min_past in zip(range(len(ID)-1),ID[:-1],ID[1:],ref[:-1],time[:-1]):
        
        if Idp != Idn:
            newID.append(Idp)
            print('[*] Calculating -> ID %d'%Idp)
            expected.append(myfunc(hour))
            hour = {'Ref':np.array([]),'minutes_past':np.array([])}
        else:
            if reflect:
                hour['Ref'] = np.append(hour['Ref'],reflect)
                hour['minutes_past'] = np.append(hour['minutes_past'],min_past)
            
    if ref[-1]:
        hour['Ref'] = np.append(hour['Ref'],ref[-1])
        hour['minutes_past'] = np.append(hour['minutes_past'],time[-1])
    newID.append(ID[-1])
    expected.append(myfunc(hour))
    
    print('[>] Write into %s.'%outfile)
    writer.writerows([['Id','Expected']])
    for Id,rainfall in zip(newID,expected):
    
        writer.writerows([['%d'%Id,'%f'%rainfall]])
    
    
    fw.close()
    try:
        measured = numpy.array(fp['Expected'].values.tolist())
        calculated = numpy.array(expected)
        MSE = pow( np.average((measured - calculated )**2) ,0.5)
        print('MSE:%f'%MSE)
    except:
        pass
    print('[*] Done.')
    
    
    
if __name__ == "__main__":
    main()
