import numpy as np
import pandas as pd
import pickle
from pathlib import Path

from utilities import layer2_reg_retest

## glabal settings ##################################
path_input_y = ''
path_input_X = ''
path_output = ''
Path(path_output).mkdir(parents=True, exist_ok=True)


## read layer1 output ##################################
y_train = pd.read_csv(path_input_y+'target_y_train2.csv', index_col=0, header=None)
y_test1 = pd.read_csv(path_input_y+'target_y_test1.csv', index_col=0, header=None)
y_test2 = pd.read_csv(path_input_y+'target_y_test2.csv', index_col=0, header=None)
    
with open(path_input_X+'retest_layer1_output.pkl', 'rb') as f:
    data = pickle.load(f)
    
    
##############################
#new dict
layer2_output = {}

for fir_reg in ['svr','rf','xgb', 'eNet']:
    layer2_output[fir_reg] = {}
    for sec_reg in ['svr','rf','xgb', 'eNet']:
        layer2_output[fir_reg][sec_reg] = {}
        for stacked_moda in ['all', 'task', 'non-task', 'top-task']:
            layer2_output[fir_reg][sec_reg][stacked_moda] = {
                             'r2_train':{},
                             'mse_train':{},
                             'pred_train':{},
                             'r2_test1':{},
                             'mse_test1':{},
                             'pred_test1':{},
                             'r2_test2':{},
                             'mse_test2':{},
                             'pred_test2':{},
                             'best_para':{},
                            }
            
#############################################
#iterate over 4 algorithms for each layer
for fir_reg in ['svr','rf','xgb', 'eNet']:
    for sec_reg in ['svr','rf','xgb', 'eNet']:
        print('\n\n##################fir_reg:',fir_reg,'     sec_reg:',sec_reg,'##################')

        for stacked_moda in ['all', 'task', 'non-task', 'top-task']:
            if stacked_moda == 'all':
                use_moda = ['wm', 'lan', 'rest-pca75', 'rel', 'mot', 'emo', 'soc', 'surf', 'VolBrain', 'subc', 'cort', 'gam']
            elif stacked_moda == 'task':
                use_moda = ['wm', 'lan', 'rel', 'mot', 'emo', 'soc', 'gam']
            elif stacked_moda == 'non-task':
                use_moda = ['rest-pca75','surf', 'VolBrain', 'subc', 'cort']  
            elif stacked_moda == 'top-task':
                use_moda = ['wm', 'lan', 'rel']
            print('stacked_moda:',stacked_moda)
            
            X_train = data[fir_reg][use_moda[0]]['train2_pred'].reshape(-1,1)
            X_test1 = data[fir_reg][use_moda[0]]['test1_pred'].reshape(-1,1)        
            X_test2 = data[fir_reg][use_moda[0]]['test2_pred'].reshape(-1,1)        
            for moda in use_moda[1:]:   
                    X_train =  np.hstack((X_train, data[fir_reg][moda]['train2_pred'].reshape(-1,1)))
                    X_test1 =  np.hstack((X_test1, data[fir_reg][moda]['test1_pred'].reshape(-1,1)))
                    X_test2 =  np.hstack((X_test2, data[fir_reg][moda]['test2_pred'].reshape(-1,1)))
         

            layer2_output[fir_reg][sec_reg][stacked_moda]['r2_train'],layer2_output[fir_reg][sec_reg][stacked_moda]['mse_train'], layer2_output[fir_reg][sec_reg][stacked_moda]['r2_test1'],layer2_output[fir_reg][sec_reg][stacked_moda]['mse_test1'],layer2_output[fir_reg][sec_reg][stacked_moda]['r2_test2'],layer2_output[fir_reg][sec_reg][stacked_moda]['mse_test2'],layer2_output[fir_reg][sec_reg][stacked_moda]['pred_train'],layer2_output[fir_reg][sec_reg][stacked_moda]['pred_test1'],layer2_output[fir_reg][sec_reg][stacked_moda]['pred_test2'],layer2_output[fir_reg][sec_reg][stacked_moda]['best_para'] = layer2_reg_retest(sec_reg, X_train, X_test1, X_test2, y_train, y_test1, y_test2)

##############################
#output
with open(path_output+'retest_layer2_output.pkl', 'wb') as f:
    pickle.dump(layer2_output, f)