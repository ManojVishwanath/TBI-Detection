# import lib
import numpy as np
import pandas as pd
import random

from Feature_selection import fea_sel
from Standardize_features import MR_control,MR_tbi
from ML_algorithms import ML_Classifier

# function to calculate Independent validation accuracy
def IV(Total_dataframe_human,sub_human,Control_human,Tbi_human,p,*argv):
    """_summary_

    Args:
        Total_dataframe_human (_type_): _description_
        sub_human (_type_): _description_
        Control_human (_type_): _description_
        Tbi_human (_type_): _description_
        p (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    print('Individual validation (Leave 2 out)')
    num_control_human = len(Control_human)
    num_tbi_human = len(Tbi_human)

    #p['max_features']=int((len(Total_dataframe))/10)

    count1=0
    count_fea={}
    for i in Total_dataframe_human.columns[:-2]:
        count_fea[i]=0

    z=0
    
    # set number of test combinations
    num_iter=int((num_control_human*num_tbi_human)/10)
    print("No. of iterations = %d"%(num_iter))
    #num_iter=1

    


    selected_fea={}

    if argv:
        x = argv[0]
        y = argv[1]
    else:
        #x = np.random.randint(0,num_control_human,num_iter)
        #y = np.random.randint(0,num_tbi_human,num_iter)
        x = random.sample(range(num_control_human), num_iter)
        y = random.sample(range(num_tbi_human), num_iter)

    dtree=np.zeros((6,len(x)))
    k1=np.zeros((6,len(x)))
    k2=np.zeros((6,len(x)))
    k3=np.zeros((6,len(x)))
    rf=np.zeros((6,len(x)))
    nn=np.zeros((6,len(x)))
    svecm=np.zeros((6,len(x)))
    xgb=np.zeros((6,len(x)))

    #x=[0]
    #y=[0]
    
    # x=[14, 15,  3, 13,  1,  5, 11,  0,  7,  2,  2,  3,  4,  5,  3, 15,  5,	
    #    11, 13, 14,  4, 13, 11,  9,  6,  0,  2,  5, 12, 14,  7, 14,  2,  8,	
    #    12,  8,  5, 12,  8,  7,  9,  5,  0,  3,  6, 15,  3,  0, 12, 15, 13,	
    #     6,  8,  7, 11,  0,  0, 11, 10,  5,  3,  1,  4,  0, 15, 13,  5,  9,	
    #     0,  9,  7,  8,  1, 14, 10, 12,  4,  0,  3,  4,  0,  0,  8,  0,  9,	
    #     1,  8,  1, 10, 15,  4, 14,  2, 12,  2,  0, 12,  5, 11,  3, 10,  9,	
    #     8,  2,  7,  9,  7, 10,  6, 11, 10,  2,  9,  5,  9,  2,  6,  5,  2,	
    #     0,  0,  3,  8,  2,  0,  6,  6,  3,  5,  1,  1,  0, 11,  0,  0,  6,	
    #     3,  5,  4,  9,  1,  2, 15,  2, 13,  5, 14,  6,  7,  9,  0,  8]	

    # y=[1, 12,  2,  9, 10, 17,  3, 17, 17,  5, 16, 12, 10, 14, 17, 17, 17,	
    #         9,  9,  8, 13,  6, 18,  2,  3,  0,  2, 12, 10, 17, 10, 13,  1,  4,	
    #        17,  3, 11,  5,  7, 14, 12, 16, 18,  8, 16, 16, 10, 12, 18, 15, 12,	
    #        12,  7, 10,  9,  0,  0,  1, 18, 18,  0,  3,  5, 18, 11,  7, 14, 16,	
    #         3,  3, 10, 10,  9, 17,  3, 15,  4, 17, 11, 17, 14,  1,  0,  5, 15,	
    #         2,  3,  4,  5, 13,  6,  0, 15,  4, 12,  3, 11, 14, 16, 14,  9, 12,	
    #        10,  7,  3, 13, 14,  1,  0, 15,  0,  6, 18,  4, 18, 17, 10,  2, 10,	
    #         8, 12,  9, 13,  2, 13, 11,  3,  5,  6, 16,  6, 13, 13,  1, 14,  0,	
    #        18, 18, 12,  7,  9, 18,  1,  1,  5,  8, 15, 17,  0,  8, 11, 13]	

    #for a in range(num_iter):
    for a in range(len(x)):
        i=x[a]
        j=y[a]

    #for i in range(num_control_human):
    #    for j in range(num_tbi_human):

        Training_Control_human = []
        Training_Tbi_human = []
        Testing_Control_human = []
        Testing_Tbi_human = []
        Training_Control_human  =   [x for x in Control_human if x != Control_human[i]]
        Training_Tbi_human      =   [x for x in Tbi_human if x != Tbi_human[j]]

        Testing_Control_human.append(Control_human[i])
        Testing_Tbi_human.append(Tbi_human[j])

        Testing =sub_human[Testing_Control_human[0]].append(sub_human[Testing_Tbi_human[0]], ignore_index = True)

        Training=pd.DataFrame()

        for k in (Training_Control_human):
            Training = Training.append(sub_human[k], ignore_index = True) 

        for k in (Training_Tbi_human):
            Training = Training.append(sub_human[k], ignore_index = True) 

        Training, col_mean_test, col_std_test = MR_control(Training)
        Testing = MR_tbi(Testing,col_mean_test,col_std_test)

    #    print('-----------------------------------------------------------------------')
        print(a)
    #    print('Training Control:',Training_Control_human)
    #    print('Training TBI:',Training_Tbi_human)
    #    print('Testing Control:',Testing_Control_human)
    #    print('Testing TBI:',Testing_Tbi_human)

        train_fea = Training.iloc[:,0:-2]
        Y = Training.iloc[:,-1]

        training,selected_fea[Testing_Control_human[0],Testing_Tbi_human[0]]=fea_sel(train_fea,Y,p)
        training['Tbi_label']=Y
        print(training.shape)
    #    print(selected_fea[Testing_Control_human[0],Testing_Tbi_human[0]])
        for g in selected_fea[Testing_Control_human[0],Testing_Tbi_human[0]]:
            count1=count_fea[g]
            count_fea[g]=count1+1

        testing = Testing[training.columns]
        dtree[:,z],k1[:,z],k1_val,k2[:,z],k2_val,k3[:,z],k3_val,rf[:,z],nn[:,z],svecm[:,z],xgb[:,z]=ML_Classifier(training, testing)
        #dtree[:,z],k1[:,z],k1_val,k2[:,z],k2_val,k3[:,z],k3_val,rf[:,z],svecm[:,z],xgb[:,z]=ML_Classifier(training, testing)
        z=z+1
    
    #return dtree,k1,k1_val,k2,k2_val,k3,k3_val,rf,nn,svecm,xgb,count_fea,Training,num_iter,x,y
    return dtree,k1,k1_val,k2,k2_val,k3,k3_val,rf,nn,svecm,xgb,count_fea,Training,num_iter