import numpy as np
import pandas as pd
import panel as pn
from scipy.optimize import minimize

def compute_random_allocations(log_return, num_ports=15000):
    _, ncols = log_return.shape
    
    # Compute log and mean return
    mean_return = np.nanmean(log_return, axis=0)
    
    # Allocate normalized weights
    weights = np.random.random((num_ports, ncols))
    normed_weights = (weights.T / np.sum(weights, axis=1)).T
    data = dict(zip(log_return.columns, normed_weights.T))

    # Compute expected return and volatility of random portfolios
    data['Return'] = expected_return = np.sum((mean_return * normed_weights) * 252, axis=1)
    return_covariance = np.cov(log_return[1:], rowvar=False) * 252
    if not return_covariance.shape:
        return_covariance = np.array([[252.]])
    data['Volatility'] = volatility = np.sqrt((normed_weights * np.tensordot(return_covariance, normed_weights.T, axes=1).T).sum(axis=1))
    data['Sharpe'] = sharpe_ratio = expected_return/volatility
    
    df = pd.DataFrame(data)
    df.attrs['mean_return'] = mean_return
    df.attrs['log_return'] = log_return
    return df

def check_sum(weights):
    return np.sum(weights) - 1

def get_return(mean_ret, weights):
    return np.sum(mean_ret * weights) * 252

def get_volatility(log_ret, weights):
    return np.sqrt(np.dot(weights.T, np.dot(np.cov(log_ret[1:], rowvar=False) * 252, weights)))

def compute_frontier(df, n=30):
    frontier_ret = np.linspace(df.Return.min(), df.Return.max(), n)
    frontier_volatility = []

    cols = len(df.columns) - 3
    bounds = tuple((0, 1) for i in range(cols))
    init_guess = [1./cols for i in range(cols)]
    for possible_return in frontier_ret:
        cons = (
            {'type':'eq', 'fun': check_sum},
            {'type':'eq', 'fun': lambda w: get_return(df.attrs['mean_return'], w) - possible_return}
        )
        result = minimize(lambda w: get_volatility(df.attrs['log_return'], w), init_guess, bounds=bounds, constraints=cons)
        frontier_volatility.append(result['fun'])
    return pd.DataFrame({'Volatility': frontier_volatility, 'Return': frontier_ret})

def minimize_difference(weights, des_vol, des_ret, log_ret, mean_ret):
    ret = get_return(mean_ret, weights)
    vol = get_volatility(log_ret, weights)
    return abs(des_ret-ret) + abs(des_vol-vol)

@pn.cache
def find_best_allocation(log_return, vol, ret):
    cols = log_return.shape[1]
    vol = vol or 0
    ret = ret or 0
    mean_return = np.nanmean(log_return, axis=0)
    bounds = tuple((0, 1) for i in range(cols))
    init_guess = [1./cols for i in range(cols)]
    cons = (
        {'type':'eq','fun': check_sum},
        {'type':'eq','fun': lambda w: get_return(mean_return, w) - ret},
        {'type':'eq','fun': lambda w: get_volatility(log_return, w) - vol}
    )
    opt = minimize(
        minimize_difference, init_guess, args=(vol, ret, log_return, mean_return),
        bounds=bounds, constraints=cons
    )
    ret = get_return(mean_return, opt.x)
    vol = get_volatility(log_return, opt.x)
    return pd.Series(list(opt.x)+[ret, vol], index=list(log_return.columns)+['Return', 'Volatility'], name='Weight')