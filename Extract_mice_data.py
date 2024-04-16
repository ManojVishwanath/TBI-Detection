# import lib
import pandas as pd
import numpy as np
import mne

# function to extract mice eeg data
# Extract data from .edf file
def extract_mice_sleepdata(mice,p,label,label2):
    """function to extract mice eeg data from the file

    Args:
        mice (list): list of mice ID
        p (dictionary): containing all parameters of mice data
        label (string): Control / Tbi
        label2 (string): old / new
    """
    no_data=[]
    if label == 'Control':
        control = {}
    else:
        tbi = {}
    
    if label2 == 'new':
        df2=pd.read_csv(p['data_folder_mice']+'\\'+'Channel_Contents'+'.txt',header=None, index_col=None,error_bad_lines=False)
        groups=df2.iloc[1:,0].str.split(expand=True)
        groups.columns=['File','EMG','EEG','EEG','Group','Label']

        
    for l in range (len(mice)):
        print()
        print('Subject #',mice[l])
        
        if label2 == 'new':
            df = pd.read_csv(p['data_folder_mice']+'\\'+mice[l]+'_Stages.txt',  error_bad_lines=False,sep='delimiter', header=None)
            if label == 'Control':
                nu=16
                df = df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]])
            elif label == 'Tbi':
                nu=0
            x  = df.loc[nu]
            a  = x.str.split('\t',expand=True)
            for j in range(nu,len(df)+nu-1):
                x = df.loc[j]
                b = x.str.split('\t',expand=True)
                a = a.append(b)
            a.columns = a.iloc[0]
            a = a[a.iloc[:,3] != 'Stage']
            a= a.iloc[2:]
        elif label2 == 'old':
            df = pd.read_csv(p['data_folder_mice']+'\\'+mice[l]+'_Stages.csv', sep='delimiter', header=None)
            df = df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]])
            #df.iloc[0:5,:]
            x  = df.loc[18]
            a  = x.str.split(',',expand=True)
            for j in range(19,len(df)+18):
                x = df.loc[j]
                b = x.str.split(',',expand=True)
                a = a.append(b)
            a.columns = a.iloc[0]
            a = a[a.iloc[:,3] != 'Stage']
            a= a.iloc[2:]

        raw = mne.io.read_raw_edf(p['data_folder_mice']+'\\'+mice[l]+".edf", preload=True,verbose=None)
        
        if p['filter_extract'] == 'tim':
            filt_raw = raw.copy()
            filt_raw.load_data().filter(p['lf2'], p['hf2'])    
            raw = filt_raw
            
        raw_eeg = raw[:, :][0]
        if label == 'Control' and label2 == 'old':
            if mice[l] == 'Sham104_BL5':
                index = raw.ch_names.index('SHA'+mice[l][4:7]+'-E')
            elif mice[l] == 'Sham105_BL5':
                index = raw.ch_names.index('SH'+mice[l][4:7]+'-E')
            else:
                index = raw.ch_names.index('SHM'+mice[l][4:7]+'-E')
        elif label == 'Tbi' and label2 == 'old':
            if mice[l] == 'TBI106_BL5':
                index = raw.ch_names.index('TBI'+mice[l][3:6]+'E')
            else:
                index = raw.ch_names.index('TBI'+mice[l][3:6]+'-E')
        elif label2 == 'new':
            ch_inter=(groups.iloc[groups[groups['File']==mice[l]].index.values-1,2])
            if len(ch_inter.iloc[0]) == 1:
                ch='Ch0'+(ch_inter.iloc[0])
            else:
                ch='Ch'+(ch_inter.iloc[0])
            for i in range(len(raw.ch_names)):
                if raw.ch_names[i][0:4] == ch:
                    index=i
        raw_data = (raw_eeg[index,:])

        count = 0
        j = 0
        data_control = []
        
        for i in range(len(a)):
            if a.iloc[i,2]==p['sleep_stage']:
                #print(i+1)
                count = count+1
                data_control[j:j+4*p['fs']] = (raw_data[i*p['fs']*4:i*p['fs']*4+(p['fs']*4)])
                #print(j)
                j = j+4*p['fs']
        
        if len(data_control) !=0:
            data_control=data_control-np.mean(data_control)

            if label == 'Control':
                #name = 'control_'+p['sleep_stage']+mice[l]#+'_'+p['channel'][e]#.split('-')[0]
                name = mice[l]
                control[name] = data_control.reshape((1, len(data_control)))
                #print(data_control)
            else:
                #name = 'tbi_'+p['sleep_stage']+mice[l]#+'_'+p['channel'][e]#.split('-')[0]
                name = mice[l]
                tbi[name] = data_control.reshape((1, len(data_control)))
                #print(data_tbi)
        else:
            if mice[l] in no_data:
                pass
            else:
                no_data.append(mice[l])

        print('Subject data shape ',np.shape(data_control))
        #print(count)
    if len(no_data) != 0:
        print('----------------------------------------------------------')
        print('No '+p['sleep_stage']+' stage in '+label +' subjects ', no_data)
    
#    for ij in mice:
#        print(mice)
#        if ij in no_data:
#            mice.remove(ij)
#            print(ij)
#            print(mice)
    ind = np.where(np.in1d(mice, no_data))[0]
    new_list = [val for n, val in enumerate(mice) if n not in ind]
    print('==========================================================')
    
    if label == 'Control': 
        return control,new_list,no_data
    else:
        return tbi,new_list,no_data
