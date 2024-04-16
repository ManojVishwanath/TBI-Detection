#Set parameters for human dataset in dictionary "p"

def human_param():
    """declare dictionary "p" which contains all parameters for human dataset

    Returns:
        dictionary: dictionary "p" containing all parameters for human dataset
    """
    
    p = dict()
    
    # set data path
    # p['data_folder']         =   os.getcwd()+'\\'+'human'
    p['data_folder']        =   r'D:\final_human\data'
    
    # set datasets
    p['data']=['dataset1','dataset2']

    # set subjects in dataset
    p['dataset1_Control_human']  =   ['102','208','457']#,'495','556','563','744']
    p['dataset1_Tbi_human']      =   ['244','340','399']#,'424','488','510','670']
    
    p['dataset2_Control_human'] = ['XVZ2FYATE8M0SSF','XVZ2FYAQH8YMGKY','XVZ2FYATE84ZTFV']#,'XVZ2FYATE8AJWX0','XVZ2FYATE8BBO87','XVZ2FFAG8875MNV','XVZ2FYATE8ZYTB2','XVZ2FYATE8YDANN','XVZ2FYATE8X4YXQ']
    p['dataset2_Tbi_human']      =['XVZ2FYAQH8WVIUC','XVZ2FYATE84MSWI','XVZ2FYATE8B9R6X']#,'XVZ2FYATE8DFIYL','XVZ2FYATE8FN4DS','XVZ2FYATE8HSYB3','XVZ2FYATE8I41U0','XVZ2FYATE8JWW0A','XVZ2FYATE8K9U90','XVZ2FYATE8W7FI6','XVZ2FYATE8Z362L','XVZ2FFAG885GFUG']
    
    # set sampling frequency
    p['dataset1_fsh']            =   200
    p['dataset2_fsh']            =   200

    # set age of subjects
    p['age'] = {
        '102': [48],
        '208': [26],
        '457': [33],
        '495': [59],
        '399': [30],
        '556': [59],
        '563': [32],
        '603': [61],
        '744': [33],
        '153': [31],
        '244': [49],
        '340': [40],
        '424': [26],
        '488': [30],
        '510': [32],
        '670': [61],
        '440': [27],
        '610': [58],
        '101': [38],
        'XVZ2FYAQH8WM6TP' : [39],
        'XVZ2FYAQH8WVIUC' : [50],
        'XVZ2FYATE84MSWI' : [34],
        'XVZ2FYATE8B9R6X' : [33],
        'XVZ2FYATE8DFIYL' : [32],
        'XVZ2FYATE8FA7E2' : [59],
        'XVZ2FYATE8FN4DS' : [30],
        'XVZ2FYATE8HSYB3' : [23],
        'XVZ2FYATE8I41U0' : [47],
        'XVZ2FYATE8IF50T' : [31],
        'XVZ2FYATE8JWW0A' : [43],
        'XVZ2FYATE8K9U90' : [25],
        'XVZ2FYATE8W7FI6' : [29],
        'XVZ2FYATE8YIMAH' : [46],
        'XVZ2FYATE8Z362L' : [40],
        'XVZ2FFAG885GFUG' : [27],
        'XVZ2FFAG888P52H' : [35],
        'XVZ2FFAG88ACGI4' : [64],
        'XVZ2FYATE8M0SSF' : [37],
        'XVZ2FYATE8X4YXQ' : [55],
        'XVZ2FYATE8AALDJ' : [33],
        'XVZ2FYATE875N3G' : [36],
        'XVZ2FFAG889F317' : [58],
        'XVZ2FYATE86FLYZ' : [30],
        'XVZ2FYATE8B60OJ' : [26],
        'XVZ2FYAQH8YMGKY' : [31],
        'XVZ2FYATE84ZTFV' : [43],
        'XVZ2FYATE8AJWX0' : [72],
        'XVZ2FYATE8BBO87' : [69],
        'XVZ2FYATE8TW5E7' : [64],
        'XVZ2FYAQH8XLFTM' : [29],
        'XVZ2FYAQH906525' : [64],
        'XVZ2FYAQH90QFES' : [69],
        'XVZ2FYATE8245MT' : [64],
        'XVZ2FYATE83RBU3' : [37],
        'XVZ2FYATE87IKI5' : [69],
        'XVZ2FYATE8ALXGF' : [26],
        'XVZ2FYATE8U1TQ5' : [22],
        'XVZ2FYATE8E94H2' : [32],
        'XVZ2FFAG886UF84' : [84],
        'XVZ2FFAG8875MNV' : [67],
        'XVZ2FYATE8ZYTB2' : [76],
        'XVZ2FYATE8YDANN' : [67],
        'XVZ2FYATE8XUPX7' : [63]
    }

    # set filter parameters
    #'delta','theta','alpha','sigma','beta','gama','normal'(0-50Hz)
    p['freq_band']      =   'normal'
        
    # set domain for filtering
    #'tim','freq'
    p['filter_extract'] =   'freq'
    
    # filter using mne while extracting
    if p['filter_extract'] == 'tim':
        p['lf2'] = 0.5
        p['hf2'] = 50

    # choose raw data or data which has undergone ECG removal through ICA
    #'Y','N'
    p['ica'] = 'Y'
    
    # set sleep stages
    #['W','N1','N2','N3','R']
    p['sleep_stage']    =   ['R']
    
    # set electrode positions
    #['F3-A2', 'F4-A1', 'C3-A2', 'C4-A1', 'O1-A2', 'O2-A1', 'EOG-L', 'EOG-R', 'Chin', 'L Leg', 'R Leg', 'ECG', 'Snore', 'Airflow', 'P-Flo', 'C-FLOW', 'Chest', 'Abdomen', 'SpO2', 'C-Press', 'R-R', 'EtCO2']
    p['channel']        =   ['F3', 'F4', 'C3', 'C4', 'O1','O2']
    
    # set EEG epoch length (sec)
    p['epoch_len']      =   30
    
    # set total data duration (min or 'NA')
    p['duration']       =   30
    
    # set features 
    #['absolute_power','relative_power','slow_fast','frequency amplitude asymmetry','phase synchrony','coherence','hjorth','spectral_entropy','phase amplitude coupling']
    p['features']=['absolute_power','relative_power','slow_fast','frequency amplitude asymmetry','phase synchrony','coherence','hjorth','spectral_entropy','phase amplitude coupling']

    # set age regression
    #'Y','N'
    p['age_regg']='Y'

    # set maximum number of features to be considered for final ML
    p['max_features']=23

    # return final dictionary "p"
    return p