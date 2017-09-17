import logging
import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler
import importlib
import glob
import inspect
import yaml
from functools import wraps

config_file = 'config.yaml'
if len(sys.argv) > 1:
  config_file = sys.argv[1]
config = yaml.load(open(config_file, 'r'))
cmd_whitelist = config.get('cmd_whitelist', [])
auth_users = config.get('auth_users', [])
auth_chats = config.get('auth_chats', [])

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.message.chat_id
        allowed = user_id in auth_users or chat_id in auth_chats
        if not allowed:
            bot.leave_chat(chat_id)
            print("Access Denied.")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

updater = Updater(config['token'])
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def add_command(name, func, protected=True):
    print 'Adding command: %s' % name
    if protected and (len(auth_users) > 0 or len(auth_chats) > 0):
      func = restricted(func)
    handler = CommandHandler(name, func, pass_args=True)
    dispatcher.add_handler(handler)

def start(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Beep Boop")
add_command('start', start)

def chat_info(bot, update, args):
    user_id = update.effective_user.id
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="User Id: %s\nChat Id: %s\n" % (user_id, chat_id))
add_command('chat_info', chat_info)

cmd_register = {}
for fn in glob.glob("plugins/*.py"):
    mod_name = fn.split('/')[1].split('.')[0]
    if mod_name != '__init__':
        module = importlib.import_module('plugins.%s' % mod_name)
        for fn_name, fn in inspect.getmembers(module, inspect.isfunction):
            if fn_name.endswith('_cmd'):
                cmd_name = '_'.join(fn_name.split('_')[:-1])
                if cmd_name not in cmd_register:
                    add_cmd = True
                    if len(cmd_whitelist) > 0:
                        if cmd_name not in cmd_whitelist:
                            add_cmd = False
                    if add_cmd:
                        cmd_register[cmd_name] = fn.__doc__
                        add_command(cmd_name, fn)
                else:
                    print 'Duplicate command name: %s' % cmd_name
                    sys.exit(-1)

cmd_help = []
for cmd in cmd_register:
    help_info = cmd_register[cmd]
    if help_info is not None:
      cmd_help.append(help_info)

def helper(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Here's what I know how to do:\n" + "\n".join(cmd_help))
add_command('help', helper)

updater.start_polling()
