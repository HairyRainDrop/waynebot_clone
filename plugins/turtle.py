import sys

import requests

def get_turtle_price(trtl_amount):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = "https://trtl.y4ht.se/convert?trtl={amt}".format(amt=trtl_amount)
    msg = "Sorry there was a problem getting your coin price."
    try:
        resp = requests.get(url, headers=headers).json()
        error = resp.get("error", None)
        if error is not None:
            msg = "Problem getting the price. Error - {error}".format(error=error)
            return msg
        prices = resp.get("price", None)
        if prices is None:
            msg = "Problem getting the price from {url}".format(url=url)
            return msg
        usd_price = prices.get("usdPrice", None)
        btc_price = prices.get("btcPrice", None)
        msg = "Currently {trtl} TRTL is worth {usd} ({btc})".format(trtl=trtl_amount, usd=usd_price, btc=btc_price)
        return msg
    except Exception as e:
        print("Error retrieving trtl: %s" % e)
        return msg


def trtl_cmd(bot, update, args):
    """/trtl <trtl_amount>: Get the current price of TurtleCoin"""
    trtl_amount = 1
    if args is not None and len(args) > 0:
        trtl_amount = args[0]
    try:
        print(trtl_amount)
        amount_int = int(trtl_amount)
        msg = get_turtle_price(trtl_amount)
    except BaseException as e:
        print(e)
        msg = "Please only pass in integers greater than 0"
    bot.send_message(chat_id=update.message.chat_id, text=msg)
