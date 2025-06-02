from entsoe import EntsoePandasClient
import pandas as pd

token = 'c6c1aef9-8dd5-4339-b964-fc3431ffa20f'
client = EntsoePandasClient(api_key=token)

start = pd.Timestamp('20250601', tz='Europe/Brussels')
end = pd.Timestamp('20250602', tz='Europe/Brussels')

country_codes = ["SE_3", "SE_4"]

dfs = []
for country_code in country_codes:
  df = client.query_day_ahead_prices(country_code, start=start, end=end)
  df.name = country_code
  dfs.append(df)

df = pd.concat(dfs, axis=1)

df.plot(title='Day Ahead Prices', ylabel='EUR/MWh', xlabel='Time', figsize=(10, 5))

def get_day_ahead_prices(country_code, start, end):
    """
    Fetches day-ahead prices for a given country code and time range.
    
    :param country_code: The country code to fetch prices for.
    :param start: Start time as a pandas Timestamp.
    :param end: End time as a pandas Timestamp.
    :return: DataFrame with day-ahead prices.
    """
    return client.query_day_ahead_prices(country_code, start=start, end=end)

def get_day_ahead_prices_plot(country_code, start, end):
    """
    Fetches and plots day-ahead prices for a given country code and time range.
    
    :param country_code: The country code to fetch prices for.
    :param start: Start time as a pandas Timestamp.
    :param end: End time as a pandas Timestamp.
    """
    df = get_day_ahead_prices(country_code, start, end)
    df.plot(title=f'Day Ahead Prices for {country_code}', ylabel='EUR/MWh', xlabel='Time', figsize=(10, 5))
    return df