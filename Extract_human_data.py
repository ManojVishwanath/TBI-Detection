# import lib
import pandas as pd
import numpy as np
import mne

def extract_human_data(parameters,class_label,dataset_label):
    """function to extract human eeg data from the file

    Args:
        parameters (dictionary): contains parameters for human data
        class_label (string): Control / Tbi
        dataset_label (string): choice of dataset

    Returns:
        data (2D array): extracted dataset
        sleep_label (1D array): corresponding labels
        new_list (list): list of human subjects who contain corresponding sleep stage dataset
        no_data (list): list of human subjects who do not contain corresponding sleep stage dataset
    """

    no_data=[]
    data={}
    sleep_label={}
    subjects = parameters[dataset_label+'_'+class_label+'_human']

    for l in subjects:

        #print subject name---------------------------------------------------
        print()
        print('Subject ',l)

        #load stage file------------------------------------------------------
        if dataset_label == 'dataset2':
            a = pd.read_csv(parameters['data_folder']+'\\'+l+'_Stage.txt',header=None, index_col=None)
        elif dataset_label == 'dataset1':
            df = pd.read_csv(parameters['data_folder']+'\\'+l+'_Stage.txt',header=None, index_col=None)
            df = df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]])
            x  = df.loc[16]
            a  = x.str.split(expand=True)

            for j in range(17,len(df)+16):
                x = df.loc[j]
                b = x.str.split(expand=True)
                a = a.append(b)

        a.columns = a.iloc[0]
        a = a[a.iloc[:,20] != 'Stg']

        #load data file------------------------------------------------------
        if parameters['ica'] == 'Y':
            raw = mne.io.read_raw_fif(parameters['data_folder']+'\\'+l+"_ica.fif", preload=True,verbose=None)
        elif parameters['ica'] == 'N':
            raw = mne.io.read_raw_edf(parameters['data_folder']+'\\'+l+".edf", preload=True,verbose=None)

        #filter in time domain-----------------------------------------------
        if parameters['filter_extract'] == 'tim':
            filt_raw = raw.copy()
            filt_raw.load_data().filter(parameters['lf2'], parameters['hf2'])    
            raw = filt_raw

        #total data-----------------------------------------------------------
        raw_eeg = raw[:, :][0]
        print(np.shape(raw_eeg))

        temp=set(parameters['channel'])
        index = [i for i, val in enumerate(raw.ch_names) if val in temp]
        raw_data = (raw_eeg[index,:])

        count = 0
        j = 0
        data_control = np.zeros((len(parameters['channel']),1))

        b1=[]
        for i in range(len(a)):
            
            if a.iloc[i,20] in parameters['sleep_stage']:
                b1.append(a.iloc[i,20])
                #print(i+1)
                count = count+1
                if dataset_label == 'dataset2':
                    data_control = np.concatenate((data_control,(raw_data[:,i*parameters[dataset_label+'_fsh']*parameters['epoch_len']:i*parameters[dataset_label+'_fsh']*parameters['epoch_len']+(parameters[dataset_label+'_fsh']*parameters['epoch_len'])])),axis=1)   
                elif dataset_label == 'dataset1':
                    data_control = np.concatenate((data_control,(raw_data[:,i*parameters[dataset_label+'_fsh']*parameters['epoch_len']:i*parameters[dataset_label+'_fsh']*parameters['epoch_len']+(parameters[dataset_label+'_fsh']*parameters['epoch_len'])])*10**6),axis=1)   
                #print(j)
                j = j+parameters['epoch_len']*parameters[dataset_label+'_fsh']
            
        data_control = data_control[:,1:]
        print(np.shape(data_control))
        if np.shape(data_control)[1] !=0:
            data_control = data_control - data_control.mean(axis=1, keepdims=True)
            name = l
            data[name] = data_control
            if class_label == 'Control':
                b1 = [x + '0' for x in b1]
                sleep_label[name] = b1
            else:
                b1 = [x + '1' for x in b1]
                sleep_label[name] = b1
        else:
            if l in no_data:
                pass
            else:
                no_data.append(l)

    #print subjects with no sleep stage-------------------------------------
    if len(no_data) != 0:
        print('----------------------------------------------------------')
        print(f"No {parameters['sleep_stage']} stage in {class_label} subjects {no_data}")
        

    #create new list of subjects who have particular sleep stage-------------
    ind = np.where(np.in1d(subjects, no_data))[0]
    new_list = [val for n, val in enumerate(subjects) if n not in ind]
    print('==========================================================')
    
    return data,sleep_label,new_list,no_data


        