import os
import re
import sys
import sklearn as skl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.cluster
import glob
import dataproc
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import dataproc.operations
from dataproc.operations.hitp import bayesian_block_finder
from dataproc.operations.hitp import fit_peak


def reshape():
    '''
    For an XRD datapoint, reshape() combines the 8 parameters for the 4 curves which make up each peak into 1 column
    Output should be (n,32) where n is the number of peaks in that XRD pattern.
    
    Note: You might need to change the file path. File should contain all the 8 parameters for all the curves that make
    up all the peaks in the XRD pattern. These parameters can be obtained from feat_extr() function.
   
    '''


    #Directory to pull files
    path = "C:/Users/oluwa/Jupyter notebooks/"
    regex = "TiNiSn_500C_Y20190218_14x14_t60_(?P<num>.*?)_bkgdSub_1D_extr_param.csv"

    # Pull data from file
    files = os.listdir(path)

    #regex to parse grid location from file
    pattern = re.compile(regex)

    if len(files) == 0:
         print("no files in path")
         sys.exit()


    #Get the needed files only

    filess=[]
    data={}
    II=0
    for file in files:
        match = pattern.match(file)
        if(match == None):
            continue
        filess.append(match)
        num = int(match.group("num"))
        #print(num)

        pp = pd.read_csv(path+file, names = ['x0/Q','y0','I','alpha','gamma','FWHM','area','area-err','X0'])
        
        data[II+1]=np.array(pp[pp.columns[0:8]])
        II+=1


    #find the minimum no of peaks of all the XRD patterns

    min_no_peaks = 100
    for k in data.keys():
        min_no_peaks = min(min_no_peaks,len(data[k]))
        
    
    print(min_no_peaks)
    
    
    #Reshape the output dictionary--data
    
    reshape_dic={}
    for k in range(0,len(data.keys())):
        reshape=[]
        for i in range(len(data[k+1])//4):
                if len(data[k+1])%4 != 0:
                    kk = k+1
                    print('Length of datapoint %d not a multiple of 4' %kk)

                ppp = list(data[k+1][4*i])+list(data[k+1][(4*i)+1])+ list(data[k+1][(4*i)+2])+ list(data[k+1][(4*i)+3])
                reshape.append(ppp)

        #reshape.append(list(data[k+1][4*i:(4*i)+4]))

        #print(k)
        #print(np.shape(data[k+1]))
        print(np.shape(reshape)) 

        reshape_dic[k+1] = reshape
        
    
    
 
            
    
    
    
    
     
        
        
        
        
     
             
            
    #Find average of the intensities
    #for k in range(0,len(reshape_dic.keys()))
        
        
    
    #Remove the least intense peaks
    #params = {}
    #for k in data.keys():
     #   if len(data[k]['I']) > min_no_peaks:
      #      mm = len(data[k]['I']) - min_no_peaks
            #print(mm)
            #print(k)
       #     subdata = data[k].sort_values('I')
        #    subdata = subdata.drop(subdata.index[range(0,mm)])

         #   subdata = subdata.sort_index()
          #  params[k] = subdata
        #else: 
         #   continue
            
            
    return reshape_dic
        
        
       
    
    
