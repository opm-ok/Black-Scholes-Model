import numpy as np
import scipy.stats as sci
import pandas as pd
import datetime

import mibian



pd.set_option('display.expand_frame_repr', False)  # ADJUST PYTHON DISPLAY


# Standard Deviations to stress the model
STRESS_DEVIATION = 4.5


def black_scholes_merton(Stock_Price, K, Time, Rate, Sigma, Option_type):

    if Time <= (1/365):
        return "EXPIRING TODAY"

    # Current stock price stressed (1 day move based on a deviation move)
    if Option_type.upper() == 'C':
         stock_price_stressed = Stock_Price * (1 + (Sigma / np.sqrt(252)) * STRESS_DEVIATION)
    else:
        stock_price_stressed = Stock_Price * (1 - (Sigma / np.sqrt(252)) * STRESS_DEVIATION)
        print(stock_price_stressed)

    d1 = (np.log(stock_price_stressed / K) + (Rate + 0.5 * Sigma ** 2) * Time) / (Sigma * np.sqrt(Time))
    d2 = (np.log(stock_price_stressed / K) + (Rate - 0.5 * Sigma ** 2) * Time) / (Sigma * np.sqrt(Time))

    if Option_type == 'C':
        result = (stock_price_stressed * sci.norm.cdf(d1, 0, 1) - K * np.exp(-Rate * Time) * sci.norm.cdf(d2, 0, 1))
    elif Option_type == 'P':
        result = (K * np.exp(-Rate * Time) * sci.norm.cdf(-d2, 0, 1) - stock_price_stressed * sci.norm.cdf(-d1, 0, 1))
    else:
        result = 0

    return max(result, 0)


df = pd.read_csv(r'D:\BSM Option Pricing Model\test.csv')

fedRate = 0.0275
bsmPrices = []
expList = []
impliedVolatility = []


print(df.head(10))


for i in range(len(df.index)):
    stock_price = float(df["LastClosePrice"][i])
    option_price = df["OptionPrice"][i]
    K = df["K"][i]
    time_exp = (datetime.datetime.strptime(str(df["ExpDate"][i]), "%Y-%m-%d") - datetime.datetime.today()).days + 2 # Include today and end date
    option_type = str(df["OptionSymbol"][i][:1])

    print("stock price: {}, option price: {}, strike: {}, exp: {}, option_type: {}, IV: ".format(stock_price, option_price, K, time_exp, option_type))

    print(mibian.BS([299, 250, 2.75, 191], volatility=11.8 ,callPrice=51.78).impliedVolatility)

    if option_type.upper() == 'C':
        IV = round(((mibian.BS([stock_price, K, (fedRate * 100), time_exp], callPrice=option_price).impliedVolatility) / 100), 4)


    else:
        IV = round(max((mibian.BS([stock_price, K, (fedRate * 100), time_exp], putPrice=option_price).impliedVolatility), 31.25) /100, 4)


    BS_price = round(black_scholes_merton(stock_price, K, (time_exp / 365), fedRate, IV, option_type), 3)


    # Updating dataframe
    expList.append(time_exp)
    bsmPrices.append(BS_price)
    impliedVolatility.append(IV)

df["T_Days"] = expList
df["Implied Volatility"] = impliedVolatility
df["BSM_OptionPrice"] = bsmPrices


df.to_csv("BSM_RESULT.csv", index=False)
print(df.head(10))
