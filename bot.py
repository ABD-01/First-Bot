from os import environ
from sys import argv
from cathy import Cathy

def main():

    token = open('TOKEN').read()

    bot = Cathy(channel_name="chat-aiml", bot_token=token, database="./database.db")
    bot.run()


if __name__ == '__main__':  # for `python -m` invocation
    main()
