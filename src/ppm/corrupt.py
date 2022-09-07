import subprocess
import os


class CorruptUtils:
    class MoovAtomNotFound(Exception):
        pass

    class FfprobeThrewNonZero(Exception):
        pass

    class VideoFileDoesNotExist(Exception):
        pass

    class CorruptedAndTooOld(Exception):
        pass

    @classmethod
    def raise_if_it_is_not_ok(cls, video_path: str):
        # Check existance
        if not os.path.isfile(video_path):
            raise cls.VideoFileDoesNotExist()

        # Use Ffprobe for check moov atom and others
        command = ['ffprobe', '-v', 'trace', video_path]
        sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get stdout and stderr
        _, err = sp.communicate()
        
        if sp.returncode != 0:
            # Video is not ok, so...
            if b'moov atom not found' in err:
                raise cls.MoovAtomNotFound(str(err))
            else:
                raise cls.FfprobeThrewNonZero(str(err))