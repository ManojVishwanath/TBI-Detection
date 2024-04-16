
def length_sel(data,label,p):
    """extract first few epochs from each subject based on duration selected in parameter

    Args:
        data (dictionary): artifact removed data 
        label (dictionary): corresponding labels
        p (dictionary): contains all parameters of the dataset

    Returns:
        data (dictionary): data
        label (dictionary): corresponding labels
    """
    
    for ele in data:
        
        if p['duration'] != 'NA':
            data[ele]=data[ele][:,:,0:p['duration']*int(60/p['epoch_len'])]
            label[ele]=label[ele][0:p['duration']*int(60/p['epoch_len'])]
        
        elif p['duration'] == 'NA':
            data[ele]=data[ele]
            label[ele]=label[ele]
            
    return data,label