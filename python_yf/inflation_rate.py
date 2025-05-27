import pandas_datareader.data as web
import datetime

start_date = datetime.datetime(2010, 1, 1)
end_date = datetime.datetime(2024, 4, 15)

#inflation_data = web.DataReader('FPCPITOTLZGEUU', 'fred', start_date, end_date)
inflation_data = web.DataReader('CPIAUCNS', 'fred', start_date, end_date)

inflation_data.to_csv("inflation_data.csv")