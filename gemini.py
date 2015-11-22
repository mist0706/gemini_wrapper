#!/usr/bin/env python
"""
   Please see https://docs.gemini.com/
"""

import hmac
import time
import json
import base64
import urllib
import hashlib
import requests

PRIVATE_METHODS = [
                    'order',
                    'orders',
                    'mytrades',
                    'balances',
                    'heartbeat'
                    ]

PUBLIC_METHODS = [
                    'symbols',
                    'book',
                    'trades'
                    ]

class Gemini(object):
    """
    Use for requesting Gemini with API key and Secret
    """

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.public_methods = set(PUBLIC_METHODS)
        self.private_methods = set(PRIVATE_METHODS)

    def api_query(self, method, payload=None):
        """
        Queries Gemini with given method and options

        :param method: Query method for getting info
        :type method: str

        :param : Specify additional path values depending on method
        :type variable: str

        :return: JSON response from Gemini
        :rtype : dict
        """

        if not payload:
            payload = {}

        nonce = int(time.time() * 1000)
        base_url = 'https://api.gemini.com'
        request_url = ''

        api_path = '/v1/' + method
        request_url = base_url + api_path

        if method.split("/")[0] in self.public_methods:
            response = requests.get(request_url)
            return response.json()

        payload['request'] = api_path
        payload['nonce'] = nonce
        encoded_payload = base64.b64encode(json.dumps(payload))
        signature = hmac.new(self.api_secret, encoded_payload, hashlib.sha384).hexdigest()

        headers = {
                    'X-GEMINI-APIKEY' : '%s' % self.api_key,
                    'X-GEMINI-PAYLOAD' : '%s' % encoded_payload,
                    'X-GEMINI-SIGNATURE' : '%s' % signature
                    }

        response = requests.post(request_url, headers=headers)

        return response.json()

    def get_symbols(self):
        return self.api_query('symbols')

    def get_book(self, symbol):
        return self.api_query('book/' +  symbol)

    def get_trades(self, symbol):
        return self.api_query('trades/'+ symbol)

    def order_new(self, symbol, amount, price, side, __type):
        payload = {
                    'symbol' : symbol,
                    'amount' : amount,
                    'price': price,
                    'side' : side,
                    'type' : __type
        }

        return self.api_query('order/new', payload=payload)

    def order_status(self, order_id):
        payload = {
                    'order_id' : order_id
        }
        return self.api_query('order/status', payload=payload)

    def order_cancel(self, order_id):
        payload = {
                    'order_id' : order_id
        }
        return self.api_query('order/cancel', payload=payload)

    def order_cancel_all(self):
        return self.api_query('order/cancel/all')

    def order_cancel_session(self):
        return self.api_query('order/cancel/session')
   
    def orders(self):
       return self.api_query('orders')

    def mytrades(self, symbol, timestamp, limit_trades=None):
        if not limit_trades:
            limit_trades = 50

        payload = {
                    'symbol' : symbol,
                    'limit_trades' : limit_trades,
                    'timestamp' : timestamp
        }
        return self.api_query('mytrades', payload=payload)

    def balances(self):
        return self.api_query('balances')

    def heartbeat(self):
        return self.api_query('heartbeat')
