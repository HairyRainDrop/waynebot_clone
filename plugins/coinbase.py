def coinbase(self, message, coin):
    coin = coin.upper().replace(" ", "")
    if coin not in ('LTC', 'BTC', 'ETH'):
        self.send_message(message, "Please specify BTC, LTC, or ETH.", True)
    else:
        try:
            url = "https://api.coinbase.com/v2/prices/%s-USD/spot" % coin
            resp = requests.get(url).json()
            price = str(resp['data']['amount'])
            msg = "%s is currently at $%s." % (coin, price)
        except:
            msg = "Sorry there was a problem retrieving the information."
        self.send_message(message, msg, True)  
