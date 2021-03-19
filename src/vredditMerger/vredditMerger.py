from subprocess import PIPE, Popen


class vredditMerger:
    @staticmethod
    def merge(FFMPEG_DIR, video_url: str) -> bytes:
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
