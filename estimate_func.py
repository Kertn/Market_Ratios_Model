from statistics import mean
from matplotlib import pyplot as plt
import numpy as np
from sklearn import preprocessing
import pandas as pd

def estimate_annualy_income_test(model, train_df, y_test, price_discount, bear_inv):
    test_df = train_df.groupby(train_df['Ticker'].astype(int)).last()
    tickers = test_df['Ticker']
    price_coll = test_df['Stock_Price']
    test_df.drop(['Stock_Price', 'Ticker'], axis=1, inplace=True)
    test_df = preprocessing.normalize(test_df.to_numpy())
    if not len(test_df) == len(tickers) == len(price_coll) == len(y_test):
        print('Len_all', len(test_df), len(tickers), len(price_coll), len(y_test))
        raise ValueError('Len test error')
    print('Total len', len(test_df))
    total_income_percent = []
    total_income_values = []
    total_invested = 0
    total_income = 0
    invest_price = 0
    total_balance = 10000
    invest = False
    for X, ticker, actual_price, y_price in zip(test_df, tickers, price_coll, y_test):
        current_ticker = str(ticker).split('.')[0]
        current_year = str(ticker).split('.')[1]

        price_pred = model.predict(X.reshape(1, -1))
        # print('price_pred * price_discount', price_pred * price_discount)
        # print('actual_price', actual_price)
        # print('price discount', price_discount)
        if price_pred * price_discount > actual_price:
            invest = True
            if total_balance < actual_price:
                invest = False
            stocks = int(total_balance / actual_price)
            invest_price = stocks * actual_price
            total_invested += invest_price
            side = 1
        elif (price_pred < actual_price * price_discount) and bear_inv:
            stocks = int(total_balance / actual_price)
            invest_price = stocks * actual_price
            total_invested += invest_price
            side = 0
            invest = True
        else:
            invest_price = 0
            invest = False
        if invest:
            try:
                if (stocks * y_price) / invest_price > 30:
                    print('Check, act_pr, y_price', ticker, actual_price, y_price)
            except:
                None
            if side:
                total_income_percent.append((stocks * y_price) / invest_price)
                # print('total_income_percent',(stocks * y_price) / invest_price)
                total_income += stocks * y_price - invest_price
                total_income_values.append(total_income)
            else:
                total_income_percent.append(invest_price / (stocks * y_price))
                total_income += invest_price - stocks * y_price
                total_income_values.append(total_income)
        else:
            continue

    print('Percent', total_income_percent)
    print('len_total_invest', len(total_income_percent))
    print('good invest', sum([1 if i > 1.15 else 0 for i in total_income_percent]))
    try:
        estim = total_income/total_invested
    except:
        estim = 0
    print('Income ratio', estim)

    print('sum([1 if i > 1.15 else -1 for i in total_income_percent])', sum([1 if i > 1.15 else -1 for i in total_income_percent]))

    if len(test_df) / 32 > len(total_income_percent):
        return 0
    else:
        return estim


def est_invest(model, train_df, y_test, price_discount, bear_inv, sector_name):
    tickers = train_df['Ticker']
    train_df.drop(['Stock_Price', 'Ticker'], axis=1, inplace=True)
    test_df = preprocessing.normalize(train_df.to_numpy())
    if not len(test_df) == len(tickers) == len(y_test):
        print('Len_all', len(test_df), len(tickers), len(y_test))
        raise ValueError('Len test error')
    print('Total len', len(test_df))
    for X, ticker, actual_price in zip(test_df, tickers, y_test):
        current_ticker = str(ticker).split('.')[0]
        current_year = str(ticker).split('.')[1]

        price_pred = model.predict(X.reshape(1, -1))

        if price_pred * price_discount > actual_price:
            with open('Invest.txt', 'a') as file:
                file.write(f'Ticker - {current_ticker}, Year - {current_year}, Current price - {actual_price}, model_predicted price - {price_pred}, Model - {model}, Sector name - sector_name, Price discount - {price_pred/actual_price} - Buy\n\n')

        elif (price_pred < actual_price * price_discount) and bear_inv:
            with open('Invest.txt', 'a') as file:
                file.write(f'Ticker - {current_ticker}, Year - {current_year}, Current price - {actual_price}, model_predicted price - {price_pred}, Model - {model}, Sector name - sector_name, Price discount - {actual_price/price_pred} - Sell')