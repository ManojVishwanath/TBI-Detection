#Set parameters for mice dataset in dictionary "p_mice"

def mice_param():
    """declare dictionary "p" which contains all parameters for mice dataset


    Returns:
        dictionary: dictionary "p" containing all parameters for mice dataset

    """
    #declare dictionary "p_mice"
    p_mice = dict()
    
    # set data path
    # p['data_folder_mice']        =   os.getcwd()+'\\'+'mice'
    p_mice['data_folder_mice']        =   r'D:\final_mice\data'

    # set datasets
    #'old','new','both'
    p_mice['data_mice'] = 'new'
    
    # set subjects in dataset
    #['Sham102_BL5','Sham103_BL5','Sham104_BL5','Sham105_BL5','Sham107_BL5','Sham108_BL5'] 
    p_mice['Old_Control_mice']       =   ['Sham102_BL5','Sham103_BL5','Sham104_BL5','Sham107_BL5','Sham108_BL5']
    #['TBI101_BL5','TBI102_BL5','TBI103_BL5','TBI104_BL5','TBI106_BL5']
    p_mice['Old_Tbi_mice']           = ['TBI101_BL5','TBI102_BL5','TBI103_BL5','TBI104_BL5','TBI106_BL5']
    
    #['m001_G30_BaselineDay1_sham','m001_G31_BaselineDay1_sham','m001_I40_BaselineDay1_sham','m001_J44_BaselineDay1_sham','m001_K50_BaselineDay1_sham','m001_L54_BaselineDay1_sham','m001_M61_BaselineDay1_sham','m010_TPE01_BaselineDay2_sham','m010_TPE03_BaselineDay2_sham','m010_TPE06_BaselineDay2_sham','m010_TPE08_BaselineDay2_sham','m010_TPE10_BaselineDay2_sham','m010_TPE12_BaselineDay2_sham','m010_TPE15_BaselineDay2_sham','m010_TPE18_BaselineDay2_sham','m010_TPE19_BaselineDay2_sham']
    p_mice['New_Control_mice'] = ['m010_TPE01_BaselineDay2_sham','m010_TPE03_BaselineDay2_sham','m010_TPE06_BaselineDay2_sham','m010_TPE08_BaselineDay2_sham','m010_TPE10_BaselineDay2_sham']#,'m010_TPE12_BaselineDay2_sham','m010_TPE15_BaselineDay2_sham','m010_TPE18_BaselineDay2_sham','m010_TPE19_BaselineDay2_sham']
    #['m001_M60_BaselineDay1_CCI','m001_L56_BaselineDay1_CCI','m001_L55_BaselineDay1_CCI','m001_K51_BaselineDay1_CCI','m001_J43_BaselineDay1_CCI','m001_I41_BaselineDay1_CCI','m001_H36_BaselineDay1_CCI','m001_G29_BaselineDay1_CCI','m001_E20_BaselineDay1_CCI']
    p_mice['New_Tbi_mice']     = ['m001_M60_BaselineDay1_CCI','m001_L56_BaselineDay1_CCI','m001_L55_BaselineDay1_CCI','m001_K51_BaselineDay1_CCI','m001_J43_BaselineDay1_CCI']#,'m001_I41_BaselineDay1_CCI','m001_H36_BaselineDay1_CCI','m001_G29_BaselineDay1_CCI']#,'m001_E20_BaselineDay1_CCI']
        
    # set sampling frequency
    p_mice['fs']            =   256

    # set domain for filtering
    #'tim','freq'
    p_mice['filter_extract'] =   'freq'
    
    # filter using mne while extracting
    if p_mice['filter_extract'] == 'tim':
        p_mice['lf2'] = 0.5
        p_mice['hf2'] = 50

    # choose raw data or data which has undergone ECG removal through ICA
    #'Y','N'
    p_mice['ica'] = 'N'

    # set sleep stages
    #['W','NR','R']
    p_mice['sleep_stage']    =   'R'

    # set electrode positions(dummy) 
    ##do not change##
    p_mice['channel']        =   ['A']
      
    # set EEG epoch length (sec)
    p_mice['epoch_len']      =   28

    # set total data duration (min or 'NA')
    p_mice['duration']       =   30

    # set features
    #['absolute_power','relative_power','slow_fast','frequency amplitude asymmetry','phase synchrony','coherence','hjorth','spectral_entropy','phase amplitude coupling']
    p_mice['features']=['absolute_power','relative_power','slow_fast','frequency amplitude asymmetry','phase synchrony','coherence','hjorth','spectral_entropy','phase amplitude coupling']
    
    # set maximum number of features to be considered for final ML
    p_mice['max_features']=30

    # return final dictionary "p_mice"
    return p_mice