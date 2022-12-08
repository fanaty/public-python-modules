import subprocess
import os


class CorruptUtils:
    class CorruptException(Exception):
        pass

    class MoovAtomNotFound(CorruptException):
        pass

    class FfprobeThrewNonZero(CorruptException):
        pass

    class VideoFileDoesNotExist(CorruptException):
        pass

    class CorruptedAndTooOld(CorruptException):
        pass

    class MissingStream(CorruptException):
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
            elif b'does not contain any stream' in err:
                raise cls.MissingStream(str(err))
            else:
                raise cls.FfprobeThrewNonZero(str(err))
