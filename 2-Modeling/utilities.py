from IPython.display import display
import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from sklearn.model_selection import GridSearchCV

import xgboost as xgb
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet

#############################################################

def single_moda(use_reg, X_train1, X_train2, X_test, y_train1, y_train2, y_test, verbose=True):
    
    if use_reg =='svr':
        param = {'kernel' : ['rbf'],#poly,'sigmoid'],
                 'gamma' : ['scale','auto', 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 3e-08, 3e-07, 3e-06, 3e-05, 3e-04, 3e-03,6e-08, 6e-07, 6e-06, 6e-05, 6e-04, 6e-03],
                 'C': [1,6,9,10,12,15,20,50],
                }
        regressor = SVR()
        
    if use_reg == 'eNet':
        param = {'alpha': np.logspace(-6, 4, 500), #500
                    'l1_ratio':np.linspace(0,1,100), #100
                    'max_iter': [1000],
                }
        regressor = ElasticNet()

    if use_reg == 'xgb':
        param ={'booster': ['gbtree'],#'gblinear'
                        'eta':[0.03,0.06,0.1],#[0.1,0.2,0.3],copy1
                        'max_depth':list(range(1,5)),#[2,4,6,8,10],copy1 
                        'subsample':[0.6,0.8,1],#[0.3,0.6,1],copy1
                        }
        regressor = xgb.XGBRegressor()
        
    if use_reg =='rf':
        param ={'n_estimators': [5000],
                'max_depth':list(range(1,11)),
                'max_features':['auto','sqrt','log2']
                }
        regressor = RandomForestRegressor()
        
    reg = GridSearchCV(regressor, param, cv=5, n_jobs = -1, verbose = 0)
    reg.fit(X_train1,y_train1)
    train1_preds = reg.predict(X_train1)
    train2_preds = reg.predict(X_train2)
    test_preds = reg.predict(X_test)    
    
    if verbose: 
        print(reg.best_params_, '\n train1 r2: {:.6}   train1 mse: {:.6}   |   train2 r2: {:.6}   train2 mse: {:.6}   |   test r2: {:.6}   test mse: {:.6}    '.format(
                r2_score(y_train1,train1_preds),
                mean_squared_error(y_train1,train1_preds),
                r2_score(y_train2,train2_preds),
                mean_squared_error(y_train2,train2_preds),
                r2_score(y_test,test_preds),
                mean_squared_error(y_test, test_preds),
        ))
 
    return r2_score(y_train1,train1_preds), mean_squared_error(y_train1,train1_preds), r2_score(y_train2,train2_preds), mean_squared_error(y_train2,train2_preds),r2_score(y_test,test_preds), mean_squared_error(y_test,test_preds), reg.predict(X_train1), reg.predict(X_train2), reg.predict(X_test), reg.best_params_

#############################################################

def layer2_reg(use_reg, X_train, X_test, y_train, y_test, verbose=True):
    
    if use_reg =='svr':
        param = {'kernel' : ['rbf'],
                 'gamma' : ['scale','auto', 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 3e-08, 3e-07, 3e-06, 3e-05, 3e-04, 3e-03,6e-08, 6e-07, 6e-06, 6e-05, 6e-04, 6e-03],
                 'C': [1,6,9,10,12,15,20,50],
                }
        regressor = SVR()
        
    if use_reg == 'eNet':
        param = {'alpha': np.logspace(-6, 4, 500), #500
                    'l1_ratio':np.linspace(0,1,100), #100
                    'max_iter': [1000],
                }
        regressor = ElasticNet()

    if use_reg == 'xgb':
        param ={'booster': ['gbtree'],#'gblinear'
                        'eta':[0.1,0.2,0.3],
                        'max_depth':[1,2,3,4,5,6], #gbtree
                        #'subsample':[0.3,0.6,1],
                        #'lambda':[0,0.5,1],
                        #'alpha':[0,0.5,1],
                        }
        regressor = xgb.XGBRegressor()
        
    if use_reg =='rf':
        param ={'n_estimators': [5000],
                'max_depth':[1,2,3,4,5,6],
                'max_features':['auto','sqrt','log2']
                }
        regressor = RandomForestRegressor()
        
    reg = GridSearchCV(regressor, param, cv=5, n_jobs = -1, verbose = 0)
    reg.fit(X_train,y_train)
    train_preds = reg.predict(X_train)
    test_preds = reg.predict(X_test)    
    
    if verbose: 
        print(reg.best_params_, '\n train r2: {:.6}   train mse: {:.6}   |   test r2: {:.6}   test mse: {:.6}    '.format(
                r2_score(y_train,train_preds),
                mean_squared_error(y_train,train_preds),
                r2_score(y_test,test_preds),
                mean_squared_error(y_test, test_preds),
        ))
 
    return r2_score(y_train,train_preds), mean_squared_error(y_train,train_preds), r2_score(y_test,test_preds), mean_squared_error(y_test,test_preds), train_preds,test_preds,reg.best_params_

#############################################################

def single_moda_alltrain(use_reg, X_train, X_test, y_train, y_test, verbose=True):
    
    if use_reg =='svr':
        param = {'kernel' : ['rbf'],#poly,'sigmoid'],
                 'gamma' : ['scale','auto', 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 3e-08, 3e-07, 3e-06, 3e-05, 3e-04, 3e-03,6e-08, 6e-07, 6e-06, 6e-05, 6e-04, 6e-03],
                 'C': [1,6,9,10,12,15,20,50],
                }
        regressor = SVR()
        
    if use_reg == 'eNet':
        param = {'alpha': np.logspace(-6, 4, 500), #500
                    'l1_ratio':np.linspace(0,1,100), #100
                    'max_iter': [1000],
                }
        regressor = ElasticNet()

    if use_reg == 'xgb':
        param ={'booster': ['gbtree'],#'gblinear'
                        'eta':[0.03,0.06,0.1],#[0.1,0.2,0.3],copy1
                        'max_depth':list(range(1,5)),#[2,4,6,8,10],copy1 
                        'subsample':[0.6,0.8,1],#[0.3,0.6,1],copy1
                        }
        regressor = xgb.XGBRegressor()
        
    if use_reg =='rf':
        param ={'n_estimators': [5000],
                'max_depth':list(range(1,11)),
                'max_features':['auto','sqrt','log2']
                }
        regressor = RandomForestRegressor()
        
    reg = GridSearchCV(regressor, param, cv=5, n_jobs = -1, verbose = 0)
    reg.fit(X_train,y_train)
    train_preds = reg.predict(X_train)
    test_preds = reg.predict(X_test)    
    
    if verbose: 
        print(reg.best_params_, '\n train r2: {:.6}   train mse: {:.6}   |   test r2: {:.6}   test mse: {:.6}    '.format(
                r2_score(y_train,train_preds),
                mean_squared_error(y_train,train_preds),
                r2_score(y_test,test_preds),
                mean_squared_error(y_test, test_preds),
        ))
 
    return r2_score(y_train,train_preds), mean_squared_error(y_train,train_preds), r2_score(y_test,test_preds), mean_squared_error(y_test,test_preds), reg.predict(X_train), reg.predict(X_test), reg.best_params_

#############################################################

def single_moda_retest(use_reg, X_train1, X_train2, X_test1, X_test2, y_train1, y_train2, y_test1, y_test2,  verbose=True):
    
    if use_reg =='svr':
        param = {'kernel' : ['rbf'],#poly,'sigmoid'],
                 'gamma' : ['scale','auto', 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 3e-08, 3e-07, 3e-06, 3e-05, 3e-04, 3e-03,6e-08, 6e-07, 6e-06, 6e-05, 6e-04, 6e-03],
                 'C': [1,6,9,10,12,15,20,50],
                }
        regressor = SVR()
        
    if use_reg == 'eNet':
        param = {'alpha': np.logspace(-6, 4, 500), #500
                    'l1_ratio':np.linspace(0,1,100), #100
                    'max_iter': [1000],
                }
        regressor = ElasticNet()

    if use_reg == 'xgb':
        param ={'booster': ['gbtree'],#'gblinear'
                        'eta':[0.03,0.06,0.1],#[0.1,0.2,0.3],copy1
                        'max_depth':list(range(1,5)),#[2,4,6,8,10],copy1 
                        'subsample':[0.6,0.8,1],#[0.3,0.6,1],copy1
                        }
        regressor = xgb.XGBRegressor()
        
    if use_reg =='rf':
        param ={'n_estimators': [5000],
                'max_depth':list(range(1,11)),
                'max_features':['auto','sqrt','log2']
                }
        regressor = RandomForestRegressor()
        
    reg = GridSearchCV(regressor, param, cv=5, n_jobs = -1, verbose = 0)
    reg.fit(X_train1,y_train1)
    train1_preds = reg.predict(X_train1)
    train2_preds = reg.predict(X_train2)
    test1_preds = reg.predict(X_test1)
    test2_preds = reg.predict(X_test2)
    
    if verbose: 
        print(reg.best_params_, '\n train1 r2: {:.6}   train1 mse: {:.6}   |   train2 r2: {:.6}   train2 mse: {:.6}   |   test1 r2: {:.6}   test1 mse: {:.6}    |   test2 r2: {:.6}   test2 mse: {:.6}'.format(
                r2_score(y_train1,train1_preds),
                mean_squared_error(y_train1,train1_preds),
                r2_score(y_train2,train2_preds),
                mean_squared_error(y_train2,train2_preds),
                r2_score(y_test1,test1_preds),
                mean_squared_error(y_test1, test1_preds),
                r2_score(y_test2,test2_preds),
                mean_squared_error(y_test2, test2_preds),

        ))
 
    return r2_score(y_train1,train1_preds), mean_squared_error(y_train1,train1_preds), r2_score(y_train2,train2_preds),mean_squared_error(y_train2,train2_preds),r2_score(y_test1,test1_preds), mean_squared_error(y_test1,test1_preds),r2_score(y_test2,test2_preds),mean_squared_error(y_test2,test2_preds), train1_preds, train2_preds, test1_preds, test2_preds, reg.best_params_

#############################################################

def layer2_reg_retest(use_reg, X_train, X_test1, X_test2, y_train, y_test1, y_test2, verbose=True):
    
    if use_reg =='svr':
        param = {'kernel' : ['rbf'],
                 'gamma' : ['scale','auto', 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 3e-08, 3e-07, 3e-06, 3e-05, 3e-04, 3e-03,6e-08, 6e-07, 6e-06, 6e-05, 6e-04, 6e-03],
                 'C': [1,6,9,10,12,15,20,50],
                }
        regressor = SVR()
        
    if use_reg == 'eNet':
        param = {'alpha': np.logspace(-6, 4, 500), #500
                    'l1_ratio':np.linspace(0,1,100), #100
                    'max_iter': [1000],
                }
        regressor = ElasticNet()

    if use_reg == 'xgb':
        param ={'booster': ['gbtree'],#'gblinear'
                        'eta':[0.1,0.2,0.3],
                        'max_depth':[1,2,3,4,5,6], #gbtree
                        #'subsample':[0.3,0.6,1],
                        #'lambda':[0,0.5,1],
                        #'alpha':[0,0.5,1],
                        }
        regressor = xgb.XGBRegressor()
        
    if use_reg =='rf':
        param ={'n_estimators': [5000],
                'max_depth':[1,2,3,4,5,6],
                'max_features':['auto','sqrt','log2']
                }
        regressor = RandomForestRegressor()
        
    reg = GridSearchCV(regressor, param, cv=5, n_jobs = -1, verbose = 0)
    reg.fit(X_train,y_train)
    train_preds = reg.predict(X_train)
    test1_preds = reg.predict(X_test1)
    test2_preds = reg.predict(X_test2)
    
    if verbose: 
        print(reg.best_params_, '\n train r2: {:.6}   train mse: {:.6}   |   test1 r2: {:.6}   test1 mse: {:.6}   |   test2 r2: {:.6}   test2 mse: {:.6} '.format(
                r2_score(y_train,train_preds),
                mean_squared_error(y_train,train_preds),
                r2_score(y_test1,test1_preds),
                mean_squared_error(y_test1, test1_preds),
                r2_score(y_test2,test2_preds),
                mean_squared_error(y_test2, test2_preds),
        ))
 
    return r2_score(y_train,train_preds), mean_squared_error(y_train,train_preds), r2_score(y_test1,test1_preds), mean_squared_error(y_test1,test1_preds), r2_score(y_test2,test2_preds), mean_squared_error(y_test2,test2_preds), train_preds, test1_preds, test2_preds, reg.best_params_

#############################################################