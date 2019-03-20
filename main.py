from bot.BotServer import VkBot
import configparser
from flask import Flask
import logging
from threading import Thread


app = Flask(__name__)


class TempThread(Thread):
    def start(self):
        config = configparser.ConfigParser()
        config.read('application.conf')
        token = config.get('Settings', 'token')
        vk_bot = VkBot(token)
        vk_bot.new_bot_processing()


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/start')
def start():
    TempThread().start()


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


start()
