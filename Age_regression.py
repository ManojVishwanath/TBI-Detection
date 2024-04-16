# import lib
import numpy as np

def age_reg_control_human(data):
    """remove age related correlation with features in control subjects

    Args:
        data (dictionary): data

    Returns:
        data(dictionary): age regressed control data
        m,b (array): regression parameters calculated on control sucjects (y=mx+b)
    """
    
    # y=mx+b formula used
    m=np.zeros((len(data.iloc[0])-2))
    b=np.zeros((len(data.iloc[0])-2))
    #n=np.zeros((len(data.iloc[0])-2))
    #c=np.zeros((len(data.iloc[0])-2))
    
    for i in range(len(data.iloc[0])-2):
        #print(data.columns[i])
        y=np.array(data.iloc[:,i],dtype=float)
        x=np.log10(np.array(data['age'],dtype=float))
        m[i], b[i] = np.polyfit(x,y, 1)
        #fig = plt.figure()
        #ax1 = fig.add_subplot(121)
        #ax1.plot(x,y,'o')
        #ax1.plot(x,m[i]*x+b[i])
        #ax1.set_xlabel('log(Subject Age)')
        #lab=data.columns[i]
        #ax1.set_ylabel('Log transformed '+lab)
        
        data.iloc[:,i]=y-x*m[i]
        #y=np.array(data.iloc[:,i],dtype=float)
        #n[i], c[i] = np.polyfit(x,y, 1)
        #ax2 = fig.add_subplot(122)
        #ax2.plot(x,y-x*n[i],'o')
        #ax2.plot(x,n[i]*x+c[i])
        #ax2.set_xlabel('log(Subject Age)')
        #lab=data.columns[i]
        #ax2.set_ylabel('Log transformed '+lab)
        #plt.tight_layout()
                
    return data,m,b

# perform age regression on TBI subjects using parameters obtained from control subjects
def age_reg_tbi_human(data,m,b):
    """use regression parameters calculated for control sucjects to regress tbi subjects

    Args:
        data (dictionary): data
        m,b (array): regression parameters calculated on control sucjects (y=mx+b)

    Returns:
        dictionary: age regressed tbi dataset
    """
    for i in range(len(data.iloc[0])-2):
        #print(data.columns[i])
        y=np.array(data.iloc[:,i],dtype=float)
        x=np.log10(np.array(data['age'],dtype=float))
        #m[i], b[i] = np.polyfit(x,y, 1)
        data.iloc[:,i]=y-x*m[i]
        
    return data
