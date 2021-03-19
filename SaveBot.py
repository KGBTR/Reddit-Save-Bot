from rStuff import rBot, rNotif
from environ import ffmpeg_dir
import PyUploadGram
import logging
from vredditMerger import vredditMerger


logger = logging.getLogger(__name__)


class SaveBot:
    def __init__(self, rbot: rBot):
        self.rbot = rbot
        self.pyuploadgram_sesh = PyUploadGram.Session()

    def upload_and_send_from_notif(self, notif: rNotif) -> None:
        post = self.rbot.get_info_by_id(notif.post_id)
        if post.is_video:
            if post.domain == "v.redd.it":
                b_video = vredditMerger.merge(ffmpeg_dir=ffmpeg_dir, video_url=post.video_url)
            else:
                # TODO
                return
            file_extension = post.video_url.split('.')[-1]
            file_name = f"{post.title}.{file_extension}"
            uploaded_file = self.pyuploadgram_sesh.upload_file(filename=file_name,
                                                               file=b_video
                                                               )
            reply_text = f"# Direkt Link Hazır: [INDIR]({uploaded_file.url})\r\n\n" \
                         f"^[source-code](https://github.com/KGBTR/Reddit-Save-Bot)"

        elif post.is_img:
            img_url = post.url
            file_extension = post.url.split('.')[-1]
            file_name = f"{post.title}.{file_extension}"
            uploaded_file = self.pyuploadgram_sesh.upload_file(filename=file_name,
                                                               file=img_url
                                                               )
            reply_text = f"# Direkt Link Hazır: [INDIR]({uploaded_file.url})\r\n\n" \
                         f"^[source-code](https://github.com/KGBTR/Reddit-Save-Bot)"
        else:
            # TODO
            return
        self.rbot.send_reply(reply_text, notif)
        self.rbot.read_notifs([notif])
