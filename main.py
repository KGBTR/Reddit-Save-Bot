from rStuff import rBot
from environ import (
    useragent,
    client_id,
    client_secret,
    bot_username,
    bot_pass
)
from SaveBot import SaveBot
from time import sleep


def main():
    save_bot = rBot(useragent, client_id, client_secret, bot_username, bot_pass)
    savr = SaveBot(save_bot)

    while True:
        for notif in save_bot.check_inbox(rkind='t1', read_if_not_rkind=True):
            if 'save' not in notif.body.lower():
                continue
            else:
                savr.upload_and_send_from_notif(notif)
        sleep(7)


if __name__ == '__main__':
    main()
