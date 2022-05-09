import numpy as np
import pandas as pd
import pickle

from utilities import layer2_reg


## glabal settings ##################################
path_input_y = ''
path_input_X = ''
path_output = ''

#############################################
#iterate over 4 algorithms for each layer
for fir_reg in ['eNet','svr','rf','xgb']:
    for sec_reg in ['eNet','svr','rf','xgb']:

        print('\n\n##################fir_reg:',fir_reg,'     sec_reg:',sec_reg,'##################')

        with open(path_input_X+fir_reg+'_layer1_output.pkl', 'rb') as f:
            data = pickle.load(f)

        #############################################
        for stacked_moda in ['task', 'non-task', 'top-task', 'all']:
            if stacked_moda == 'all':
                use_moda = ['wm', 'lan', 'rest-pca75', 'rel', 'mot', 'emo', 'soc', 'surf', 'VolBrain', 'subc', 'cort', 'gam']
            elif stacked_moda == 'task':
                use_moda = ['wm', 'lan', 'rel', 'mot', 'emo', 'soc', 'gam']
            elif stacked_moda == 'non-task':
                use_moda = ['rest-pca75','surf', 'VolBrain', 'subc', 'cort']  
            elif stacked_moda == 'top-task':
                use_moda = ['wm', 'lan', 'rel']
            print('\n--------------stacked_moda:',stacked_moda,'--------------')

            #new dict
            layer2_output = {'use_reg':[fir_reg,sec_reg],
                             'stacked_moda':stacked_moda,
                             'r2_train':{},
                             'mse_train':{},
                             'r2_test':{},
                             'mse_test':{},
                             'train_pred':{},
                             'test_pred':{},
                             'best_para':{},
                            }

            #8folds
            for fold in ['Fold_0', 'Fold_1', 'Fold_2', 'Fold_3', 'Fold_4', 'Fold_5', 'Fold_6', 'Fold_7']:
                y_train = pd.read_csv( path_input_y+fold+'/target_y_train2.csv', index_col=0, header=None).values[:,0]
                y_test = pd.read_csv( path_input_y+fold+'/target_y_test.csv', index_col=0, header=None).values[:,0]

                X_train = data[use_moda[0]]['train2_pred'][fold].reshape(-1,1)
                X_test = data[use_moda[0]]['test_pred'][fold].reshape(-1,1)        
                for moda in use_moda[1:]:   
                    X_train =  np.hstack((X_train, data[moda]['train2_pred'][fold].reshape(-1,1)))
                    X_test =  np.hstack((X_test, data[moda]['test_pred'][fold].reshape(-1,1)))

                layer2_output['r2_train'][fold],layer2_output['mse_train'][fold], layer2_output['r2_test'][fold], layer2_output['mse_test'][fold], layer2_output['train_pred'][fold], layer2_output['test_pred'][fold], layer2_output['best_para'][fold] = layer2_reg(sec_reg, X_train, X_test, y_train, y_test)

            #output
            with open(path_output+'layer2_'+stacked_moda+'_'+fir_reg+'_'+sec_reg+'.pkl', 'wb') as f:
                pickle.dump(layer2_output, f)