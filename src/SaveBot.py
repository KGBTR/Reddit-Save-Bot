from rStuff import rBot, rNotif
from environ import FFMPEG_DIR
import PyUploadGram
from vredditMerger import vredditMerger


class SaveBot:
    def __init__(self, rbot: rBot):
        self.rbot = rbot
        self.pyuploadgram_sesh = PyUploadGram.Session()

    def upload_and_send_from_notif(self, notif: rNotif) -> None:
        post = self.rbot.get_info_by_id(notif.post_id)
        if post.is_video:
            if post.domain == "v.redd.it":
                b_video = vredditMerger.merge(
                    FFMPEG_DIR=FFMPEG_DIR, video_url=post.video_url
                )
            else:
                self.rbot.read_notifs([notif])
                # TODO
                return
            file_extension = post.video_url.split(".")[-1]
            file_name = f"{post.title}.{file_extension}"
            try:
                uploaded_file = self.pyuploadgram_sesh.upload_file(
                    filename=file_name, file=b_video
                )
            except:
                self.rbot.read_notifs([notif])
                return
            reply_text = (
                f"# Direkt Link Hazır: [INDIR]({uploaded_file.url})\r\n\n"
                f"^[source-code](https://github.com/KGBTR/Reddit-Save-Bot)"
            )

        elif post.is_img:
            img_url = post.url
            file_extension = post.url.split(".")[-1]
            file_name = f"{post.title}.{file_extension}"
            try:
                uploaded_file = self.pyuploadgram_sesh.upload_file(
                    filename=file_name, file=img_url
                )
            except:
                return
            reply_text = (
                f"# Direkt Link Hazır: [INDIR]({uploaded_file.url})\r\n\n"
                f"^[source-code](https://github.com/KGBTR/Reddit-Save-Bot)"
            )
        else:
            self.rbot.read_notifs([notif])
            # TODO
            return
        self.rbot.send_reply(reply_text, notif)
        self.rbot.read_notifs([notif])
