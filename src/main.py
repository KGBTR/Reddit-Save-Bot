from logger import logger
from rStuff import rBot
from environ import (
    useragent,
    client_id,
    client_secret,
    bot_username,
    bot_pass,
    SENTRY_USE,
    SENTRY_DSN,
    SENTRY_TRACES_SAMPLE_RATE,
)
from SaveBot import SaveBot
import sentry_sdk
from time import sleep


def main():
    save_bot = rBot(useragent, client_id, client_secret, bot_username, bot_pass)
    save = SaveBot(save_bot)

    while True:
        for notif in save_bot.check_inbox(rkind="t1", read_if_not_rkind=True):
            if "save" in notif.body.lower():
                save.upload_and_send_from_notif(notif)
        sleep(15)


if __name__ == "__main__":
    if SENTRY_USE:
        sentry_sdk.init(
            SENTRY_DSN,
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        )
        logger.info("Sentry initialization")
    else:
        logger.warning("Sentry skipped")
    main()
