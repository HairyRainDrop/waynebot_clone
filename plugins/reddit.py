import sys
import requests
import random

def subreddit_random(sr):
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  url = "https://www.reddit.com/r/%s.json?limit=100" % sr
  try:
    response = requests.get(url, headers=headers)
    posts = map(lambda x: x['data'],  response.json()['data']['children'])
    imgs = filter(lambda x: x['url'].endswith('.jpg') or x['url'].endswith('.png') or x['url'].endswith('.gif'), posts)
    return random.choice(imgs)['url']
  except Exception as e:
    return None

def reddit_cmd(bot, update, args):
  """/reddit <sr>: Show a random image from the given subreddit"""
  if args is not None and len(args) > 0:
    sr = args[0]
    imgurl = subreddit_random(sr)
    if imgurl is not None:
      bot.send_message(chat_id=update.message.chat_id, text=imgurl, disable_web_page_preview=False)
    else:
      bot.send_message(chat_id=update.message.chat_id, text="Sorry I couldn't retrieve anything from that subreddit.")

subreddits = [ #TODO add to yaml or something
  'hmm',
  'aww',
]

thismodule = sys.modules[__name__]
def make_subreddit_fn(sub):
  def sr_fn(bot, update, args):
    reddit_cmd(bot, update, [sub])
  return sr_fn
for sr in subreddits:
  c = make_subreddit_fn(sr)
  c.__name__ = "%s_cmd" % sr
  c.__doc__ = "/%s: Show a random image from %s" % (sr, sr)
  setattr(thismodule, c.__name__, c)
