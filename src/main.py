from logger import logger
from rStuff import rBot
from environ import (
    useragent,
    client_id,
    client_secret,
    bot_username,
    bot_pass,
    FFMPEG_DIR,
    SENTRY_USE,
    SENTRY_DSN,
    SENTRY_TRACES_SAMPLE_RATE,
)
from SaveBot import SaveBot
from subprocess import PIPE, Popen
import sentry_sdk
import PyUploadGram
from time import sleep


def prep_reddit_video(video_url: str) -> bytes:
    dash_i = video_url.find("_") + 1
    dot_i = video_url[dash_i:].find(".")
    to_rep = video_url[dash_i : dash_i + dot_i]
    audio_url = video_url.replace(to_rep, "audio")

    p = Popen(
        [
            FFMPEG_DIR,
            "-y",
            "-i",
            audio_url,
            "-r",
            "30",
            "-i",
            video_url,
            "-filter:a",
            "aresample=async=1",
            "-f",
            "mp4",
            "-c:v",
            "copy",
            "-movflags",
            "frag_keyframe+empty_moov",
            "-",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = p.communicate()
    p.wait()
    return output


def main():
    save_bot = rBot(useragent, client_id, client_secret, bot_username, bot_pass)
    save = SaveBot(save_bot)

    while True:
        for notif in save_bot.check_inbox(rkind="t1", read_if_not_rkind=True):
            if "save" not in notif.body.lower():
                continue
            else:
                save.upload_and_send_from_notif(notif)
        sleep(7)


if __name__ == "__main__":
    if SENTRY_USE:
        sentry_sdk.init(
            SENTRY_DSN,
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        )
        logger.info("Sentry initialization")
    else:
        logger.warn("Sentry skipped")
    main()
