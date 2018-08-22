"""
sequence data format
"""

import os

def stock_raw2csv(filename, savedfilename):
    """format stock data
    """
    f=open(filename, 'r')
    out=open(savedfilename, 'w')
    out.write("date,opening,high,low,closing,volume,turnover\n")
    line=f.readline().strip()
    line = f.readline().strip()
    line = f.readline().strip()
    while line:
        eles=line.split(',')
        if(len(eles)<=1): break
        out.write(line+'\n')
        line=f.readline().strip()
    f.close()
    out.close()

if __name__=='__main__':
    path="../data/seq/stocks/"
    filenames=os.listdir(path+"raw/")
    for filename in filenames:
        file=path+"raw/"+filename
        if os.path.isfile(file):
            stock_raw2csv(file, path+(filename.split("_")[1]))
            print(filename)
