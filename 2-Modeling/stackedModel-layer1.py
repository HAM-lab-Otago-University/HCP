import pandas as pd
import os
import pickle
from pathlib import Path

from utilities import single_moda

##############################

#choose the algorithm for first layer, single modality models
#use_reg = 'svr'
#use_reg = 'xgb'
#use_reg = 'rf'
use_reg = 'eNet'

use_sd_files = True

path_input = ''
path_output = ''
Path(path_output).mkdir(parents=True, exist_ok=True)

## load data ############################
target={} #dict for target
features={} #dict for features

add_suffix = lambda x: '_std.csv' if use_sd_files else '.csv'

for fold in sorted(os.listdir(path_input)):
    if 'Fold' not in fold:
        continue
    target[fold] = {}
    features[fold] = {}
    features[fold]['train1']={}
    features[fold]['train2']={}
    features[fold]['test']={}
    
    for sett in ['train1','train2','test']:
        target[fold][sett] = pd.read_csv(path_input+fold+'/target_y_'+sett+'.csv', index_col=0, header=None)
    
    for mod in ['wm', 'lan', 'rel', 'mot', 'emo', 'soc', 'gam', 'rest-pca75', 'surf', 'VolBrain', 'subc', 'cort']:
        for sett in ['train1','train2','test']:
            filename = path_input+fold+'/'+mod+'_'+sett+add_suffix(use_sd_files)
            features[fold][sett][mod] =  pd.read_csv(filename, index_col=0)
                
#############################
#new dictionary
layer1_output = {'use_reg':use_reg}
for moda in features['Fold_0']['train1'].keys():
    layer1_output[moda] = {'train1_r2':{},
                           'train2_r2':{},
                           'test_r2':{},
                           'train1_mse':{},
                           'train2_mse':{},
                           'test_mse':{},
                            'train1_pred':{},
                            'train2_pred':{},
                            'test_pred':{},
                            'best_para':{},
                          }
    
    
# first layer training and output ############################
for moda in ['wm', 'lan', 'rest-pca75', 'rel', 'mot', 'emo', 'soc', 'surf', 'VolBrain', 'subc', 'cort', 'gam']:
    print('\n\n  -----',moda,'-----')
    for fold in target.keys():
        y_train1 = target[fold]['train1'].values[:,0]
        y_train2 = target[fold]['train2'].values[:,0]
        y_test = target[fold]['test'].values[:,0]
        
        X_train1 = features[fold]['train1'][moda]
        X_train2 = features[fold]['train2'][moda]
        X_test = features[fold]['test'][moda]

        layer1_output[moda]['train1_r2'][fold], layer1_output[moda]['train1_mse'][fold], layer1_output[moda]['train2_r2'][fold], layer1_output[moda]['train2_mse'][fold], layer1_output[moda]['test_r2'][fold], layer1_output[moda]['test_mse'][fold], layer1_output[moda]['train1_pred'][fold], layer1_output[moda]['train2_pred'][fold], layer1_output[moda]['test_pred'][fold], layer1_output[moda]['best_para'][fold] = single_moda(use_reg, X_train1, X_train2, X_test, y_train1, y_train2, y_test, verbose=True)

with open(path_output+use_reg+'_layer1_output.pkl', 'wb') as f:
        pickle.dump(layer1_output, f)

