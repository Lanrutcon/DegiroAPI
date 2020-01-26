# DegiroAPI
Unofficial Degiro API for Python

---

An unofficial API for [Degiro](https://www.degiro.pt/) made in Python.
It can be used to:
 - Check your portfolio, cash funds and orders
 - Get info from products (e.g. Stocks and ETFs) 
 - Set new orders (Buy/Sell)
 - Delete current orders


Based on [Pladaria's work](https://github.com/pladaria/degiro).

---

### Install

pip:

    pip install git+https://github.com/Lanrutcon/DegiroAPI.git

Without pip:

    git clone https://github.com/Lanrutcon/DegiroAPI.git
    cd DegiroAPI
    python setup.py install

---

### Examples

Login:

    from DegiroAPI import *
    account = DegiroAPI('username', 'password')
    account.login()
    
Setting a limit order to buy 5 shares of 'MSFT', 150$ a share:

    buyOrder = {
        'buySell': 0, #buy = 0, sell = 1
        'orderType': 0, #limit order
        'productId': account.search_product('MSFT')['id'], #getting Degiro's id for MSFT
        'size': 5, #number of shares to buy/sell
        'timeType': 1, #day = 1, permanent = 3
        'price': 150 #price per share
    }
    api.set_order(buyOrder)

