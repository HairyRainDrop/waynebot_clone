import requests

def coinbase(bot, update, coin):
    coin = coin.upper().replace(" ", "")
    if coin not in ('LTC', 'BTC', 'ETH'):
        bot.send_message(chat_id=update.message.chat_id, "Please specify BTC, LTC, or ETH.", True)
    else:
        try:
            url = "https://api.coinbase.com/v2/prices/%s-USD/spot" % coin
            resp = requests.get(url).json()
            price = str(resp['data']['amount'])
            msg = "%s is currently at $%s." % (coin, price)
        except:
            msg = "Sorry there was a problem retrieving the information."
        bot.send_message(chat_id=update.message.chat_id, msg, True)  
