import sys
import time
from tokens import coinmarket
from tokens import token
import requests
import json


print('RasbiteleBot online')
print('------------------ ')


# Using Your API Key
# You may use any server side programming language that can make HTTP requests to target the CoinMarketCap API. All requests should target domain
# https://pro-api.coinmarketcap.com
#
# You can supply your API Key in REST API calls in one of two ways:
#
# Preferred method: Via a custom header named X-CMC_PRO_API_KEY
# Convenience method: Via a query string parameter named CMC_PRO_API_KEY
# Security Warning: It's important to secure your API Key against public access. The custom header option is strongly recommended over the querystring option for passing your API Key in a production environment.
# Query Parameters > id   /  symbol = BTC-ETH-....etc   /  convert  = default USD

def write_json(data, filename='response.json'):
    with open(filename,'w') as f:
        json.dump(data,f,indent=4, ensure_ascii=False)




def get_cmc_data(crypto):
    url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    # ?symbol=BTC&convert=USD
    params = {'symbol' : crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY' : coinmarket}

    r=requests.get(url, headers=headers, params=params).json()
    price=r['data'][crypto]['quote']['USD']['price']

    write_json(r)

    print(price)



def main():
    get_cmc_data('BTC')





if __name__ == '__main__':
    main()
