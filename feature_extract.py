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



def feat_extr():
    '''
    feat_extr() returns the parameters of all the curves that make up all the peaks in each XRD pattern in a dataset.
    These parameter values are found using bayesian_block_finder() and fit_peak() in Robert Tang-Kong's script 
    (see https://github.com/tangkong/dataproc/blob/master/dataproc/operations/hitp.py).
    
    '''
    
    
    
    
    BigParams = {}
    
    #Directory to pull files
    path = "C:/Users/oluwa/Downloads/TiNiSn_500C-20200714T190740Z-001/TiNiSn_500C/"
    regex = """TiNiSn_500C_Y20190218_14x14_t60_(?P<num>.*?)_bkgdSub_1D.csv"""
   
    # Pull data from file
    files = os.listdir(path)
    #regex to parse grid location from file
    pattern = re.compile(regex)

    if len(files) == 0:
         print("no files in path")
         sys.exit()
    #files = list(files[175:179])

    for file in files:
        match = pattern.match(file)
        if(match == None):
            continue
        num = int(match.group("num"))
        print(num)
        #if verbose:
            #print("\t:: " + str(num) + "\t| " + file)

        #data_array = np.array(pd.read_csv(path + file,header=None))
        #try:
         #   data_array[0].astype(np.float)
        #except:
         #   data_array = data_array[1:]
        #self.data[num] = data_array.astype(np.float)
        
        #print(path+file)

        data1 = pd.read_csv(path + file, names= ["angles","Intensity"])
        blocks1 = bayesian_block_finder(data1["angles"].values, data1["Intensity"].values)
        blocks1 = blocks1.astype(int)
        subdata1 = data1["angles"].values
        subdata2 = data1["Intensity"].values

         # Get peaks boundaries
        output = []
        for i in range(len(blocks1)-1):
            output.append(fit_peak(subdata1[blocks1[i]:blocks1[i+1]],subdata2[blocks1[i]:blocks1[i+1]],peakShape="Voigt"))

        # Get Peak Parameters and store as a csv file                  
        fullp = []
        for II in range(len(output)):

            out1,out2 = output[II]

            fullparams=[]
            fullparams1 =[]
            for name, param in out1.items():
                params = []
                for pname,subparam in param.items():
                    #print(name, pname, subparam)
                    params.append(subparam)
                fullparams.append(params)

            for name1, param1 in out2.items():
                params1 = []
                for pname1,subparam1 in param1.items():
                        #print(name1, pname1, subparam1)
                        params1.append(subparam1)
                fullparams1.append(params1)

                

            for i in range(len(fullparams)):
                fullp.append(fullparams[i]+fullparams1[i])


        print(np.shape(fullp))
        BigParams[num] = fullp

        if num > 99:
            nnn = "0" + str(num)
        elif num > 9:
            nnn = "00" + str(num)
        else: 
            nnn = "000" + str(num)

        #print('TiNiSn_500C_Y20190218_14x14_t60_'+ nnn +'_bkgdSub_1D_extr_param')
        np.savetxt('TiNiSn_500C_Y20190218_14x14_t60_'+ nnn +'_bkgdSub_1D_extr_param.csv',fullp,delimiter =',')


    
    return BigParams