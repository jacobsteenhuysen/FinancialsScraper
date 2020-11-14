from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as datetime

df = pd.read_excel('C:/Users/Jacob Steenhuysen/Downloads/Test Tickers.xlsx', sheet_name='Sheet1')

tickers_list = df['Ticker'].tolist()
data = pd.DataFrame(columns=tickers_list)



#ecommerce = ['MMM', 'CCJ']

yahoo_financials_ecommerce = YahooFinancials(data)

ecommerce_cash_flow_data = yahoo_financials_ecommerce.get_financial_stmts('annual', 'cash')

data = ecommerce_cash_flow_data['cashflowStatementHistory']

df_dict = dict()

for ticker in tickers_list:

    df_dict[ticker] = pd.concat([pd.DataFrame(data[ticker][x]) for x in range(len(data[ticker]))],
               sort=False, join='outer', axis=1)

df = pd.concat(df_dict, sort=True)

df_l = pd.DataFrame(df.stack())
df_l.reset_index(inplace=True)
df_l.columns = ['ticker', 'financials', 'date', 'value']

df_w = df_l.pivot_table(index=['date', 'financials'], columns='ticker', values='value')

df_w
export_excel = df_w.to_excel(r'C:/Users/Jacob Steenhuysen/Downloads/TEST History1.xlsx', sheet_name="Sheet1", index= True)
