from rStuff import rBot
from environ import (
    useragent,
    client_id,
    client_secret,
    bot_username,
    bot_pass,
    ffmpeg_dir
)
from subprocess import PIPE, Popen
import PyUploadGram


def prep_reddit_video(video_url: str) -> bytes:
    dash_i = video_url.find("_") + 1
    dot_i = video_url[dash_i:].find(".")
    to_rep = video_url[dash_i:dash_i + dot_i]
    audio_url = video_url.replace(to_rep, "audio")

    p = Popen([ffmpeg_dir, '-y', '-i', audio_url, '-r', '30', '-i', video_url, '-filter:a', 'aresample=async=1',
               '-f', 'mp4', '-c:v', 'copy', '-movflags', 'frag_keyframe+empty_moov', '-'], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    p.wait()
    return output


def main():
    save_bot = rBot(useragent, client_id, client_secret, bot_username, bot_pass)
    pyuploadgram_sesh = PyUploadGram.Session()

    for notif in save_bot.check_inbox(rkind='t1', read_if_not_rkind=True):
        save_bot.read_notifs([notif])
        if 'save' not in notif.body.lower():
            continue
        post = save_bot.get_info_by_id(notif.post_id)
        if post.is_video:
            if post.domain == "v.redd.it":
                b_video = prep_reddit_video(post.video_url)
            else:
                # TODO
                continue
            uploaded_file = pyuploadgram_sesh.upload_file(filename=post.title,
                                                          file=b_video
                                                          )
            save_bot.send_reply(f"hazır [{post.title}]({uploaded_file.url})", notif)

        elif post.is_img:
            img_url = post.url
            uploaded_file = pyuploadgram_sesh.upload_file(filename=post.title,
                                                          file=img_url
                                                          )
            save_bot.send_reply(f"hazır [{post.title}]({uploaded_file.url})", notif)
        else:
            # TODO
            continue


if __name__ == '__main__':
    main()
