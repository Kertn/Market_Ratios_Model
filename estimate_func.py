from statistics import mean
from matplotlib import pyplot as plt
import numpy as np
from sklearn import preprocessing
import pandas as pd
def estimate_annualy_income(models, X_estimate, tickers, price_coll, price_discount=0.8):

    #fig, axs = plt.subplots(5)

    for ind, model in enumerate(models):
        prev_ticker = ''
        total_income_percent = []
        total_income_values = []
        total_invested = 0
        total_income = 0
        invest_price = 0
        total_balance = 5000
        for X, ticker, actual_price in zip(X_estimate, tickers, price_coll):
            print('Tiker', ticker)
            current_ticker = str(ticker).split('.')[0]
            current_year = str(ticker).split('.')[1]

            if invest_price == 0 or prev_ticker != current_ticker:
                prev_ticker = current_ticker

                price_pred = model.predict(X.reshape(1, -1))

                if price_pred * price_discount > actual_price:
                    stocks = total_balance / actual_price
                    invest_price = stocks * actual_price
                    total_invested += invest_price
                    side = 1
                elif price_pred < actual_price * price_discount:
                    stocks = total_balance / actual_price
                    invest_price = stocks * actual_price
                    total_invested += invest_price
                    side = 0

                else:
                    invest_price = 0

            else:
                if side:
                    total_income_percent.append((stocks * actual_price)/invest_price)
                    total_income += stocks * actual_price - invest_price
                    total_income_values.append(total_income)
                else:
                    total_income_percent.append(invest_price / (stocks * actual_price))
                    total_income += invest_price - stocks * actual_price
                    total_income_values.append(total_income)

                price_pred = model.predict(X.reshape(1, -1))

                if price_pred * price_discount > actual_price:
                    stocks = total_balance / actual_price
                    invest_price = stocks * actual_price
                    total_invested += invest_price
                    side = 1
                elif price_pred < actual_price * price_discount:
                    stocks = total_balance / actual_price
                    invest_price = stocks * actual_price
                    total_invested += invest_price
                    side = 0

                else:
                    invest_price = 0

        # print('INCOME_RESULT', total_income)
        print('len_total_invest', len(total_income_percent))
        # print('TOTAL_INVESTED', total_invested)
        # print('Income ratio', total_income/total_invested)
        # print('MEAN', mean(total_income_percent))
        #
        # print('ind', ind)

        #axs[ind].plot(np.linspace(0, 1, len(total_income_values)), total_income_values)
    # plt.show()
    return total_income/total_invested


def estimate_annualy_income_test(models, train_df, y_test, price_discount, bear_inv):
    test_df = train_df.groupby(train_df['Ticker'].astype(int)).last()
    tickers = test_df['Ticker']
    price_coll = test_df['Stock_Price']
    test_df.drop(['Stock_Price', 'Ticker'], axis=1, inplace=True)
    test_df = preprocessing.normalize(test_df.to_numpy())
    if not len(test_df) == len(tickers) == len(price_coll) == len(y_test):
        print('Len_all', len(test_df), len(tickers), len(price_coll), len(y_test))
        raise ValueError('Len test error')

    for ind, model in enumerate(models):
        prev_ticker = ''
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
                if side:
                    total_income_percent.append((stocks * y_price) / invest_price)
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
        print('good invest', sum([1 if i > 1.25 else 0 for i in total_income_percent]))
        try:
            estim = total_income/total_invested
        except:
            estim = 0
        print('Income ratio', estim)

        print('sum([1 if i > 1.25 else -2 for i in total_income_percent])', sum([1 if i > 1.25 else -2 for i in total_income_percent]))
        # print('ind', ind)

        # axs[ind].plot(np.linspace(0, 1, len(total_income_values)), total_income_values)

    # plt.show()

    return sum([1 if i > 1.25 else -2 for i in total_income_percent])