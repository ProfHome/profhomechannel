from bot.BotServer import VkBot
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('application.conf')
    token = config.get('Settings', 'token')
    vk_bot = VkBot(token)
    vk_bot.new_bot_processing()
