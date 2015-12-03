import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def subplt2dScatters(Fig,pos,title,xvalues,yvalues,Xlabel='',Ylabel='Expected'):
    
    ax = Fig.add_subplot(pos)
    ax.scatter(xvalues,yvalues,s=10,marker='s',alpha=0.2)
    ax.set_xlabel(Xlabel)
    ax.set_ylabel(Ylabel)
    ax.set_title(title)

def main():

    infile = 'train.csv'
    print('[>] Reading %s...'%infile)
    fp = pd.read_csv(infile)
    print('[*] Finished reading files.')
    #data = fp.ix[:,:].fillna()
    att = fp.columns.tolist()[2:-1]
    
    
#    fig =plt.fig()
    print (att)
    expected = np.array( fp['Expected'].values.tolist() )
    
    fig = plt.figure()
    print ('[*] Output images')
    for att_name in att:
        a = np.array( fp[att_name].values.tolist() )
        xv = a[np.isfinite(a)]
        yv = expected[np.isfinite(a)]
        subplt2dScatters(fig,111,att_name,xv,yv,Xlabel=att_name,Ylabel='Expected')
        fig.savefig('%s.png'%(att_name),dpi=200)	
        fig.clf()
    
    
    
    #for attribute in att :
    
    
    
    print ('[*] Done.')
    
    

if __name__ == '__main__':
    main()
