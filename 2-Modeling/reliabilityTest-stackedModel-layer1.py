import pandas as pd
import pickle
from pathlib import Path

from utilities import single_moda_retest

add_suffix = lambda x: '_std.csv' if use_sd_files else '.csv'

# glabal settings #############################
use_sd_files = True
path_input = ''
path_output = ''
Path(path_output).mkdir(parents=True, exist_ok=True)

## load data ############################
target={} #dict for target
features={} #dict for features
for sett in ['train1','train2','test1','test2']:
    target[sett] = pd.read_csv(path_input+'target_y_'+sett+'.csv', index_col=0, header=None)
        
for mod in ['wm', 'lan', 'rel', 'mot', 'emo', 'soc', 'gam', 'rest-pca75', 'surf', 'VolBrain', 'subc', 'cort']:
    features[mod] = {}
    for sett in ['train1','train2','test1','test2']:
        features[mod][sett] =  pd.read_csv(path_input+mod+'_'+sett+add_suffix(use_sd_files), index_col=0)

#############################
#new dictionary
layer1_output = {}
for use_reg in ['svr', 'xgb', 'rf', 'eNet']:
    layer1_output[use_reg] = {}
    for moda in ['wm', 'lan', 'rel', 'mot', 'emo', 'soc', 'gam', 'rest-pca75', 'surf', 'VolBrain', 'subc', 'cort']:
        layer1_output[use_reg][moda] = {'best_para':{}}
        for sett in ['train1','train2','test1','test2']:
            for item in ['_r2','_mse','_pred']:
                layer1_output[use_reg][moda][sett+item] = {}
    
    
# first layer training and output ############################
for moda in ['wm', 'lan', 'rest-pca75', 'rel', 'mot', 'emo', 'soc', 'surf', 'VolBrain', 'subc', 'cort', 'gam']:
    print('\n\n  -----',moda,'-----')
    
    y_train1 = target['train1'].values[:,0]
    y_train2 = target['train2'].values[:,0]
    y_test1 = target['test1'].values[:,0]
    y_test2 = target['test2'].values[:,0]
        
    X_train1 = features[moda]['train1']
    X_train2 = features[moda]['train2']
    X_test1 = features[moda]['test1']
    X_test2 = features[moda]['test2']
        
    for use_reg in ['svr', 'xgb', 'rf', 'eNet']:
        print(use_reg)
        layer1_output[use_reg][moda]['train1_r2'], layer1_output[use_reg][moda]['train1_mse'],layer1_output[use_reg][moda]['train2_r2'], layer1_output[use_reg][moda]['train2_mse'],layer1_output[use_reg][moda]['test1_r2'], layer1_output[use_reg][moda]['test1_mse'],layer1_output[use_reg][moda]['test2_r2'], layer1_output[use_reg][moda]['test2_mse'],layer1_output[use_reg][moda]['train1_pred'], layer1_output[use_reg][moda]['train2_pred'],layer1_output[use_reg][moda]['test1_pred'], layer1_output[use_reg][moda]['test2_pred'],layer1_output[use_reg][moda]['best_para'] = single_moda_retest(use_reg, X_train1, X_train2, X_test1, X_test2, y_train1, y_train2, y_test1, y_test2, verbose=True)


    info = 'retest'
    with open(path_output+info+'_layer1_output.pkl', 'wb') as f:
            pickle.dump(layer1_output, f)

