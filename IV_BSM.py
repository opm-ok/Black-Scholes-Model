# import numpy as np
# import scipy.stats as si
# import datetime
#
# n = si.norm.pdf
# N = si.norm.cdf
#
# def bs_price(cp_flag,S,K,T,r,v,q=0.0):
#     d1 = (np.log(S/K)+(r+v*v/2.)*T)/(v*np.sqrt(T))
#     d2 = d1-v*np.sqrt(T)
#     if cp_flag == 'c':
#         price = S*np.exp(-q*T)*N(d1)-K*np.exp(-r*T)*N(d2)
#     else:
#         price = K*np.exp(-r*T)*N(-d2)-S*np.exp(-q*T)*N(-d1)
#     return price
#
# def bs_vega(cp_flag,S,K,T,r,v,q=0.0):
#     d1 = (np.log(S/K)+(r+v*v/2.)*T)/(v*np.sqrt(T))
#     return S * np.sqrt(T)*n(d1)
#
# def find_vol(target_value, call_put, S, K, T, r):
#     MAX_ITERATIONS = 100
#     PRECISION = 0.000001
#
#     sigma = 0.5
#     for i in range(0, MAX_ITERATIONS):
#         price = bs_price(call_put, S, K, T, r, sigma)
#         vega = bs_vega(call_put, S, K, T, r, sigma)
#
#         price = price
#         diff = target_value - price  # our root
#
#
#         if (abs(diff) < PRECISION):
#             return sigma
#         sigma = sigma + diff/vega # f(x) / f'(x)
#
#     # value wasn't found, return best guess so far
#     return sigma
#
# V_market = 37.65
# K = 275
# T = (datetime.datetime(2020, 12, 18) - datetime.datetime.now()).days / 365
# print(T)
# S = 298
# r = 0.0275
# cp = 'c' # call option
#
# implied_vol = find_vol(V_market, cp, S, K, T, r)
#
# print('Implied vol: %.2f%%' % (implied_vol * 100))


#------------

