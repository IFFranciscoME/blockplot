
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Project: Visualization tools of Algorand Blockchain Data                                            -- #
# -- main.py: python script with main method                                                             -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- Repository: https://github.com/IFFranciscoME/visual-block                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# -- Basic functions
import pandas as pd

# -- Timestamps tools
import datetime

# -- Algorand interaction
from algosdk.v2client import indexer

"""
How to set environment variables when using vscode
https://code.visualstudio.com/docs/python/environments#_environment-variable-definitions-file

"""

def get_env_vars(path):
    """
    Function to retrieve a dict with the token previously stored in environment file (.env)
    """
    
    with open(path, 'r') as f:
        data_dict = dict(tuple(line.replace('\n', '').split('='))
                         for line in f.readlines() if not line.startswith('#'))
    return data_dict

env_data = get_env_vars('visual_block_dev_venv/.env')

# -- Init
index_token = "I0QNiYw6Ly2O0sMI0MhM17V6QNF0Tj1TnHiJB728"
algo_address = 'https://mainnet-algorand.api.purestake.io/ps2'
headers = {"X-API-Key": index_token,}
indexer_client = indexer.IndexerClient("", algo_address, headers)

# -- ----------------------------------------------------------------------------------------- -- #

# -- Get historical transactions

def get_transactions(client, ini_ts, end_ts, time_blocks='4H'):
    """
    Returns all transactions added to the blockchain between 'ini_timestamp' and 'end_timestamp'

    Parameters
    ----------

    client: algosdk.v2client.indexer
        instantiated client with algosdk.v2client

    ini_ts, end_ts: str
        Initial and Final timestamp from where to retrieve the transactions, in format 'MM-DD-YYYY HH:MM:SS'


    time_blocks: str
        Time blocks with which the API calls will be iteratively be performed, using a pandas functionalyti [1[1]. The default option is 4 hours, see [2] for more options of time periods division.
    
    References
    ----------
    [1] https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html
    [2] https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
    """

    # create dates for recurrent API calls
    # timestamps = pd.date_range(ini_ts, end_ts, freq=time_blocks)
    # for ini_ts, end_ts in zip(timestamps[:-1], timestamps[1:]):

    # p_ini_date = '2021-05-11 8:10:00'
    # p_end_date = '2021-05-12 8:20:00'
    start_time = datetime.datetime.strptime(ini_ts, '%Y-%m-%d %H:%M:%S').isoformat('T') + 'Z'
    end_time = datetime.datetime.strptime(end_ts, '%Y-%m-%d %H:%M:%S').isoformat('T') + 'Z'

    # The indexer expacting time inputs to be in RFC 3339 format
    # start_time = datetime.datetime.strptime(str(ini_ts), '%Y-%m-%d %H:%M:%S').isoformat('T') + 'Z'
    # end_time = datetime.datetime.strptime(str(end_ts), '%Y-%m-%d %H:%M:%S').isoformat('T') + 'Z'

    nexttoken = ""
    numtx = 1
    responses = {}

    # Retrieve a max quantity of 1000 transactions at each request.
    while numtx > 0:
        response = client.search_transactions(start_time=start_time, end_time=end_time,
                                                next_page=nexttoken, limit=1000)

        transactions = response['transactions']
        responses.update(transactions)
        numtx = len(transactions)
        if numtx > 0:
            nexttoken = response['next-token']

    return responses


# initial timestamp in UTC
ini_timestamp = '2021-05-12 7:10:00'
# end timestamp in UTC
end_timestamp = '2021-05-12 7:21:00'

responses = get_transactions(client=indexer_client, ini_ts=ini_timestamp, end_ts=end_timestamp)
df_transactions = pd.DataFrame(responses)
df_transactions.head()
