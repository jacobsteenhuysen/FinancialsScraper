from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as datetime

df = pd.read_excel('C:/Users/Jacob Steenhuysen/Downloads/REIT Tickers1.xlsx', sheet_name='Sheet1')

tickers_list = df['Ticker'].tolist()
data = pd.DataFrame(columns=tickers_list)

yahoo_financials_ecommerce = YahooFinancials(data)

ecommerce_income_statement_data = yahoo_financials_ecommerce.get_financial_stmts('annual', 'balance')

data = ecommerce_income_statement_data['balanceSheetHistory']

df_dict = dict()

for ticker in tickers_list:

    df_dict[ticker] = pd.concat([pd.DataFrame(data[ticker][x]) for x in range(len(data[ticker]))],
               sort=False, join='outer', axis=1)

df = pd.concat(df_dict, sort=True)

df_l = pd.DataFrame(df.stack())
df_l.reset_index(inplace=True)
df_l.columns = ['ticker', 'financials', 'date', 'value']

df = df_l.pivot_table(index=['date', 'financials'], columns='ticker', values='value')

#df_2.index['date'] = pd.to_datetime(df_2.index['date'])

#df.reset_index()

#df['date'] = pd.to_datetime(df['date'])
#df = pd.melt(df,id_vars=['date','financials'],var_name='ticker')
              
df = pd.melt(df.reset_index(),id_vars=['date','financials'],var_name='ticker')

df['date'] = pd.to_datetime(df['date'])
df = df.groupby([df['date'].dt.year,df['financials'],df['ticker']])['value'].sum().unstack()

export_excel = df.to_excel(r'C:/Users/Jacob Steenhuysen/Downloads/REIT Balance Sheet Histories.xlsx', sheet_name="Sheet1", index= True)

