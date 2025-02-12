
import os
import platform


class GetPlatform:
    @staticmethod
    def get_downloads_folder():
        """Determine the Downloads folder based on the user's platform."""
        if platform.system() == "Windows":
            return os.path.join(os.environ["USERPROFILE"], "Downloads")
        else:
            return os.path.join(os.path.expanduser("~"), "Downloads")
