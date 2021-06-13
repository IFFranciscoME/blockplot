
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Tutorial 1: Updated version of python indexer exploration                                              #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- Repository: https://github.com/IFFranciscoME/visual-block                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# -- Base packages
import pandas as pd
import numpy as np
import os

# -- Time handling
import datetime

# -- AlgoRand Python SDK
from algosdk.v2client import indexer

# -- Visualization
from rich import inspect

# -- Read Token
# Option 1: Put it here
index_token = "I0QNiYw6Ly2O0sMI0MhM17V6QNF0Tj1TnHiJB728"
# Option 2: Read it as environment variable
# index_token = os.environ.get['ALGOTOKEN']

# -- Indexer address 

# You can choose 1: main, test, beta net, 2: local node or thirdparty node like purestake
index_address = "https://mainnet-algorand.api.purestake.io/idx2"
indexer_client = indexer.IndexerClient("", index_address, {"X-API-Key": index_token,})

# -- Timestamps in human readable format
ini_ts = '2020-12-18 03:10:00'
end_ts = '2020-12-18 03:11:00'
format = "%Y-%m-%d %H:%M:%S"

# Prepare dates in RFC format
pre_ini = datetime.datetime.strptime(ini_ts, format)
ini_timestamp = pre_ini.astimezone(datetime.timezone.utc).isoformat('T')
pre_end = datetime.datetime.strptime(end_ts, format)
end_timestamp = pre_end.astimezone(datetime.timezone.utc).isoformat('T')

"""
- Add a human readable timestamp dd-mm-YYYY HH:MM:SS
- Create 1,000 sized calls since 1k is the max transactions for each request
- Parse the whole result in a dict of dicts
- Create human readble output with principal characteristics to show
"""

response = indexer_client.search_transactions(start_time=ini_timestamp, end_time=end_timestamp)

# See the response first layer contents
response.keys()

# Block from where the transactions where extracted
inspect(response['current-round'])

# Next-Token is for continuity when multiple calls are performed
inspect(response['next-token'])

# Information of transactions 
inspect(response['transactions'])

inspect(response['transactions'][0], help=False)

for key,value in response['transactions'][0].items():
    print("--------------\nKey: {} \n-------------- \nValue: {} \n--------------\n".format(key, value))
