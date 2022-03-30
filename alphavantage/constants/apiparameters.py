class ApiParameters:
    URL = 'https://www.alphavantage.co/query'
    DATA_TYPE = 'function'
    TICKER = 'symbol'
    API_KEY = 'apikey'

    # temp_url=            f'{URL}?{ApiParameters.DATA_TYPE}=TIME_SERIES_INTRADAY&{ApiParameters.TICKER}=IBM&interval=5min'
    #         f'&{ApiParameters.API_KEY}=JULI7BLT9T36YLN2'


api_parameters = ApiParameters()
