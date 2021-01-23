from os import environ
from sys import argv
from cathy import Cathy

def main():

    token = "NzY5NTYwMzI1Mzg0OTYyMDc5.X5Qy5w.6mR4ztoTE5Cr0-LcZj2r-a4Qd5w"#open('TOKEN').read()

    bot = Cathy(channel_name="chat-aiml", bot_token=token, database="./database.db")
    bot.run()


if __name__ == '__main__':  # for `python -m` invocation
    main()
