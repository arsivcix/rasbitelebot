# CoinmarketCAP
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


#Telegram Bot API
# https://api.telegram.org/bot<token>/METHOD_NAME
# /getMe
# /getUpdates
# /sendMessage
# getUpdates and SendMessage will be handled by webhook
# webHook : https://api.telegram.org/bot797643623:AAGd-IT0Dz0bVjX7xuscSmJduT25myxeJKU/setWebhook?url=https://parum.serveo.net/
#


import sys
import time
from tokens import coinmarket
from tokens import token
import requests
import json
from  flask import Flask
from flask import request
from flask import Response
import re





print('RasbiteleBot online')
print('------------------ ')


app = Flask(__name__)

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

    return price


def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt=message['message']['text']
    pattern=r'/[a-zA-Z]{2,4}'
    ticker = re.findall(pattern, txt)
    if ticker:
        symbol = ticker[0][1:].upper()  #it contains data which is suitable our pattern
    else:
        symbol = ''

    return chat_id,symbol

def send_message(chat_id, text='your text'):
    url=f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text':text}

    r= requests.post(url,json = payload)

    return r


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, symbol = parse_message(msg)

        if not symbol:
            send_message(chat_id, 'wrong data')
            return Response('Ok', status=200)

        price=get_cmc_data(symbol)
        send_message(chat_id,price)
        write_json(msg, 'telegram_request.json')
        return Response('Ok', status=200)


    else:
        return '<h1> Rasbitelebot</h1>'



def main():
    get_cmc_data('BTC')





if __name__ == '__main__':
    #main()
    app.run(debug=True)
