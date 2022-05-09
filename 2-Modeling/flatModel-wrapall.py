import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from utilities import single_moda_alltrain

##############################
use_sd_files = True

path_input_test = ''
path_input_train = ''
path_output = ''
Path(path_output).mkdir(parents=True, exist_ok=True)
    

## load data ############################
target={} #dict for target
features={} #dict for features

add_suffix = lambda x: '_std.csv' if True else '.csv'

for fold in ['Fold_0', 'Fold_1', 'Fold_2', 'Fold_3', 'Fold_4', 'Fold_5', 'Fold_6', 'Fold_7']:
    target[fold] = {}
    features[fold] = {}
    features[fold]['train']={}
    features[fold]['test']={}
    
    target[fold]['train'] = pd.read_csv(path_input_train+fold+'/target_y_trainFlat.csv', index_col=0, header=None)
    target[fold]['test'] = pd.read_csv(path_input_test+fold+'/target_y_test.csv', index_col=0, header=None)
    
    for mod in ['wm', 'lan', 'rel', 'mot', 'emo', 'soc', 'gam', 'rest-pca75', 'surf', 'VolBrain', 'subc', 'cort']:
        features[fold]['train'][mod] =  pd.read_csv(path_input_train+fold+'/'+mod+'_trainFlat'+add_suffix(use_sd_files), index_col=0)
        features[fold]['test'][mod] =  pd.read_csv(path_input_test+fold+'/'+mod+'_test'+add_suffix(use_sd_files), index_col=0)
                
#############################
#############################


#iterate over 4 algorithms 
for use_reg in ['svr','xgb','rf','eNet']:
    print('\n\n use_reg:',use_reg)            

    for stacked_moda in ['all','task', 'non-task', 'top-task']:
        if stacked_moda == 'all':
            use_moda = ['wm', 'lan', 'rest-pca75', 'rel', 'mot', 'emo', 'soc', 'surf', 'VolBrain', 'subc', 'cort', 'gam']
        elif stacked_moda == 'task':
            use_moda = ['wm', 'lan', 'rel', 'mot', 'emo', 'soc', 'gam']
        elif stacked_moda == 'non-task':
            use_moda = ['rest-pca75','surf', 'VolBrain', 'subc', 'cort']  
        elif stacked_moda == 'top-task':
            use_moda = ['wm', 'lan', 'rel']
        print('\n-- stacked_moda:',stacked_moda,'--')
        
        #new dictionary
        flat_output = {'use_reg':use_reg,
                         'train_r2':{},
                         'test_r2':{},
                         'train_mse':{},
                         'test_mse':{},
                         'train_pred':{},
                         'test_pred':{},
                         'best_para':{},
                        }
        #############################
        for fold in target.keys():
            y_train = target[fold]['train'].values[:,0]
            y_test = target[fold]['test'].values[:,0]

            for idx,moda in enumerate(use_moda):
                X_train = features[fold]['train'][moda].values
                X_test = features[fold]['test'][moda].values

                if idx==0:
                    X_train_f,X_test_f = X_train.copy(),X_test.copy() 
                else:
                    X_train_f = np.hstack((X_train_f,X_train))
                    X_test_f = np.hstack((X_test_f,X_test))
            print(X_train.shape, X_test.shape, y_train.shape,y_test.shape)

            flat_output['train_r2'][fold], flat_output['train_mse'][fold], flat_output['test_r2'][fold], flat_output['test_mse'][fold], flat_output['train_pred'][fold], flat_output['test_pred'][fold], flat_output['best_para'][fold] = single_moda_alltrain(use_reg, X_train_f, X_test_f, y_train, y_test, verbose=True)

        #############################
        with open(path_output+use_reg+'-'+stacked_moda+'_flat_output.pkl', 'wb') as f:
                pickle.dump(flat_output, f)
            

        