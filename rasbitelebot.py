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
# bot token must be changed with yours



import sys
import time

from tokens import coinmarket
from tokens import token

import requests
import json
import re

from  flask import Flask
from flask import request
from flask import Response

import RPi.GPIO as GPIO


GPIO.cleanup()

red1=21
red2=20
red3=16
red4=12
red5=7

green1=26
green2=19
green3=13
green4=6
green5=5

def setuprasbi():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(red1,GPIO.OUT)
    GPIO.setup(red2,GPIO.OUT)
    GPIO.setup(red3,GPIO.OUT)
    GPIO.setup(red4,GPIO.OUT)
    GPIO.setup(red5,GPIO.OUT)

    GPIO.setup(green1,GPIO.OUT)
    GPIO.setup(green2,GPIO.OUT)
    GPIO.setup(green3,GPIO.OUT)
    GPIO.setup(green4,GPIO.OUT)
    GPIO.setup(green5,GPIO.OUT)

setuprasbi()


html0='<head> <title> Rasbitelebot Welcome</title> <meta http-equiv="refresh" content="30"> </head> <h1> Rasbitelebot Welcome </h1> <p>Rasberry Telegram Bot has been created for the purpose of education.</p> In order to reach repositories visit </p> <a href="https://github.com/arsivcix/rasbitelebot/">https://github.com/arsivcix/rasbitelebot/</a> '
html = html0

invest_symbol=''
invest_price=0

print('RasbiteleBot online')
print('------------------ ')








def redled(pr):
    GPIO.output(red1,pr)
    GPIO.output(red2,pr)
    GPIO.output(red3,pr)
    GPIO.output(red4,pr)
    GPIO.output(red5,pr)

def greenled(pg):
    GPIO.output(green1,pg)
    GPIO.output(green2,pg)
    GPIO.output(green3,pg)
    GPIO.output(green4,pg)
    GPIO.output(green5,pg)



def pinsoff():
    redled(0)
    greenled(0)

def pinson():
    redled(1)
    greenled(1)


def cleanrasbi():
    pinsoff()
    GPIO.cleanup()



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
    compat=r'_[a-zA-Z]{2,6}'
    ticker = re.findall(pattern, txt)
    if ticker:
        symbol = ticker[0][1:].upper()  #it contains data which is suitable our pattern
    else:
        symbol = ''

    cticker = re.findall(compat,txt)
    if cticker:
        command = cticker[0][1:].upper()
    else:
        command = ''


    return chat_id,symbol,command




def send_message(chat_id, text='your text'):
    url=f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text':text}

    r= requests.post(url,json = payload)

    return r


@app.route('/', methods=['POST', 'GET'])
def index():
    global html
    global invest_price
    global invest_symbol
    if request.method == 'POST':
        msg = request.get_json()
        write_json(msg, 'telegram_request.json')
        chat_id, symbol,command = parse_message(msg)

        if not symbol:  #   / show default format
            send_message(chat_id, 'your command must be :  /yourcoin _command (_invest or _exit) for example /btc _invest /btc exit')
            return Response('Ok', status=200)
        else:
            price=get_cmc_data(symbol)
            if not command: # only show value
                send_message(chat_id,price)
                return Response('Ok', status=200)


            else: # show continuos ----->

                # if there is a @command (invest or exit)

                if command=='PINON':
                    pinson()

                if command=='PINOFF':
                    pinsoff()

                if command=='REDON':
                    redled(1)

                if command=='REDOFF':
                    redled(0)

                if command =='GRON':
                    grenled(1)

                if command =='GROFF':
                    greenled(0)

                if command=='EXIT':
                    send_message(chat_id, 'copy exit')
                    html=html0  #html zero position
                    invest_price=0
                    pinsoff()
                    cleanrasbi()
                    return Response('Ok', status=200)


                if command=='INVEST': # loop is created here..


                    setuprasbi()
                    invest_symbol=symbol
                    invest_price=price

                    html=f'<head> <title>Rasbitelebot On The Job</title> <meta http-equiv="refresh" content="15"> </head> <body> <h1>Rasbitelebot</h1><h2>You are selected to invest in {invest_symbol} </h2> <h3>The value is {invest_price}</h3> <h3> You can see price change from the red and green lights down and up. </h3> </body>'

                    send_message(chat_id, f'You are invested in {invest_symbol} with value of {invest_price}')
                    return Response('Ok', status=200)






                else:
                    send_message(chat_id, 'your command must be :  /yourcoin _command (_invest or _exit) for example /btc _invest /btc exit')
                    return Response('Ok', status=200)
# if command is invest it will check price continuously


#if no post and get show bellow
    else:

        if invest_price!=0:
            price=get_cmc_data(invest_symbol)
            if price > invest_price:
                html=html+f'<body><p style="color:green;">latest value is {price}<p></body>'
                greenled(1)
                time.sleep(5)
                greenled(0)

            if price == invest_price:
                html=html+f'<body><p style="color:black;">latest value is {price}<p></body>'
                pinsoff()

            if price < invest_price:
                html=html+f'<body><p style="color:red;">latest value is {price}<p></body>'
                redled(1)
                time.sleep(5)
                redled(0)



        return html



def main():
    get_cmc_data('BTC')





if __name__ == '__main__':
    #main()
    setuprasbi() #raspberry is set as default pin mapping and 10 pis is set as output to blink led
    pinsoff()   # after raspberry was set we set pins 0 volt .

    app.run(debug=True)
