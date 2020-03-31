import requests
import json
from .constants import *

class DegiroAPI:

    def __init__(self, user, password):
        """
        Parameters
        ----------
        user : str
            Account's username
        password: str
            Account's password 
        """
        
        self.username = user
        self.password = password
        self.session_id = None
        self.account_no = None
        self.session = None
        self.pa_url = None
        self.product_search_url = None
        self.trading_url = None
        self.user_token = None

        self.base_url = base_trade_url


    def login(self):
        """
        Logs in to the server
        """
    
        url = self.base_url + '/login/secure/login'
        payload = {
            "username": self.username,
            "password": self.password,
            "isRedirectToMobile": False,
            "loginButtonUniversal": '',
            "queryParams": {'reason': 'session_expired'},
        }

        session = requests.session()
        res = session.post(url, json.dumps(payload))
        if res.cookies.get("JSESSIONID"):
            self.session = session
            self.session_id = res.cookies.get('JSESSIONID')
            self.get_config()
            self.get_client_info()
        else:
            print("Login Error: ", res.json())


    def get_config(self):
        """
        Get important URL's from server
        """

        config_url = self.base_url + '/login/secure/config'

        res = self.session.get(config_url)
        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            self.pa_url = res_json['data']['paUrl']
            self.product_search_url = res_json['data']['productSearchUrl']
            self.trading_url = res_json['data']['tradingUrl']
        else:
            print("Config Error: ", res.status_code)


    def get_client_info(self):
        """
        Get client info from server
        """
        
        url = self.pa_url + 'client?sessionId=' + self.session_id
        res = self.session.get(url)

        if res.status_code == requests.codes.ok:
            res_json = json.loads(res.content)
            self.account_no = res_json['data']['intAccount']
            self.user_token = res_json['data']['id']
        else:
            print("Config Info Error: ", res.status_code)


    def get_portfolio(self):
        """
        Get portfolio from server
        """
        
        update_url = '{trading_url}v5/update/'.format(trading_url=self.trading_url)
        res = self.session.get("{update_url}{account_id};""jsessionid={jsession_id}".format(
                update_url=update_url,
                account_id=self.account_no,
                jsession_id=self.session_id),
            params={'portfolio': 0, 'totalPortfolio': 0})
        if res.status_code == requests.codes.ok or res.status_code == 201:
            return res.json()
        else:
            print("Get Portfolio Error: ", res.status_code)


    def get_cash_funds(self):
        """
        Get cash funds info from server
        """
        
        update_url = '{trading_url}v5/update/'.format(trading_url=self.trading_url)
        res = self.session.get(
            "{update_url}{account_id};""jsessionid={jsession_id}".format(
                update_url=update_url,
                account_id=self.account_no,
                jsession_id=self.session_id),
            params={'cashFunds': 0})
        if res.status_code == requests.codes.ok or res.status_code == 201:
            return res.json()['cashFunds']['value'][5]['value'][2]['value'] #return EUR
        else:
            print("Get Cash Funds Error: ", res.status_code)


    def get_orders(self, session):
        """
        Get orders from server
        """
        
        update_url = '{trading_url}v5/update/'.format(trading_url=self.trading_url)
        res = self.session.get(
            "{update_url}{account_id};""jsessionid={jsession_id}".format(
                update_url=update_url,
                account_id=self.account_no,
                jsession_id=self.session_id
            ),
            params={'orders': 0, 'historicalOrders': 0, 'transactions': 0}
        )

        if res.status_code == requests.codes.ok or res.status_code == 201:
            return res.json()
        else:
            print("Get Orders Error: ", res.status_code)


    def get_open_orders(self, stock_id = None):
        """
        Get open orders from server
        """
        
        update_url = '{trading_url}v5/update/'.format(trading_url=self.trading_url)
        res = self.session.get(
            "{update_url}{account_id};""jsessionid={jsession_id}".format(
                update_url=update_url,
                account_id=self.account_no,
                jsession_id=self.session_id
            ),
            params={'orders': 0}
        )

        if res.status_code == requests.codes.ok or res.status_code == 201:
            if stock_id != None:
                for order in res.json()['orders']['value']:
                    if str(order['value'][2]['value']) == str(stock_id):
                        return order
                return '"Error in searching order", No stock found with id:{stock_id}'.format(stock_id=stock_id)

            return res.json()['orders']['value']
        else:
            print("Get Open Orders Error: ", res.status_code)


    def search_product(self, search_symbol, sort_column = None, sort_type = None, product_type=product_types.get("all"), limit=7, offset=0):
        """
        Search a product based on various criterion
        
        Parameters
        ----------
        search_symbol : str
            Ticker symbol to search for
        sort_column : str
            Sort by column. Default value 'name'
        sort_type : str
            Order the column. Check constants.py. Default value 'asc'
        product_type : int
            Filter for a type. Check constants.py. Default value 'None'
        limit : int
            Number of results. Default value 7        
        offset : int
            Results offset. Default value 0
            
        Returns
        -------
        stock : Dict
            Stock's information
        """
    
        payload = {
            'searchText': search_symbol,
            'productTypeId': product_type,
            'sortColumns': sort_column,
            'sortTypes': sort_type,
            'limit': limit,
            'offset': offset
        }

        search_url = '{search_url}v5/products/lookup?intAccount={account_id}&sessionId={session_id}&'.format(
            search_url=self.product_search_url,
            account_id=self.account_no,
            session_id=self.session_id)

        res = self.session.get(search_url, params=payload)
        if res.status_code == requests.codes.ok:
            searchDict = json.loads(json.dumps(res.json()))['products']
            
            for stock in searchDict:
                if stock['symbol'] == search_symbol:
                    return stock

            return '"Error in searching product", No stock found with symbol:{stock_symbol}'.format(stock_symbol=search_symbol)
        else:
            print("Search Product Error: ", res.status_code)


    def delete_order(self, order_id):
        """
        Deletes order
        
        Parameters
        ----------
        order_id : str
            Order's ID that will be deleted
        """
        
        delete_url = '{trading_url}v5/order/{order_id};jsessionid={session_id}?intAccount={account_id}' \
                     '&sessionId={sessionid}'.format(
                        trading_url=self.trading_url,
                        order_id=order_id,
                        session_id=self.session_id,
                        account_id=self.account_no,
                        sessionid=self.session_id)
        res = self.session.delete(delete_url)
        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            print("Delete Order Error: ", res.status_code)


    def check_order(self, order):
        """
        Checks an order

        Parameters
        ----------
        order : {buysell, orderType, productId, size, timeType, price, stopPrice}
            Order's ID that will be checked
        """
        
        check_url = '{trading_url}v5/checkOrder;jsessionid={session_id}?intAccount={account_id}&sessionId={sessionId}' \
            .format(
                trading_url=self.trading_url,
                session_id=self.session_id,
                account_id=self.account_no,
                sessionId=self.session_id
            )

        payload = json.dumps(order)
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        res = self.session.post(check_url, data=payload, headers=headers)
        return res.json()


    def confirm_order(self, order, confirmation_id):
        """
        Confirms an order
        
        Parameters
        ----------
        order : {buysell, orderType, productId, size, timeType, price, stopPrice}
            Order's data
        confirmation_id : str
            Confirmation's ID that will be checked
        """
        
        confirm_url = '{trading_url}v5/order/{confirm_id};jsessionid={session_id}?intAccount={account_id}' \
                      '&sessionId={session_Id}'.format(
                        trading_url=self.trading_url,
                        confirm_id=confirmation_id,
                        session_id=self.session_id,
                        account_id=self.account_no,
                        session_Id=self.session_id
                        )
        payload = json.dumps(order)
        headers = {'Content-Type': 'application/json'}

        res = self.session.post(confirm_url, data=payload, headers=headers)
        return res.json()
        

    def set_order(self, order):
        """
        Complete an order
        
        Parameters
        ----------
        order : {buysell, orderType, productId, size, timeType, price, stopPrice}
            Order's data 
        """
        
        res = self.check_order(order)
        order_status = res.get("status")
        if res['data']['confirmationId'] != '':
            confirm_id = res['data']['confirmationId']
            confirmation_res = self.confirm_order(order, str(confirm_id))
            return confirmation_res
        else:
            return res
