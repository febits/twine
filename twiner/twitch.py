import requests
import wget

from twiner.config import TwinerConfig


class Streamer:
    "Define a way to agroup Twitch streamers info."

    def __init__(
        self,
        username,
        usericon,
        stream_title="",
        is_streaming=False,
        previously_shown=False,
    ):
        self.username = username
        self.usericon = usericon
        self.stream_title = stream_title
        self.is_streaming = is_streaming
        self.previously_shown = previously_shown


class Twitch:
    "Defines a structure to store information and actions from Twitch."

    def __init__(self, config: TwinerConfig):
        self.users = [
            Streamer(user, icon)
            for user, icon in config.yaml["tonotify"].items()
        ]
        self.api_headers = {
            "Client-Id": f"{config.yaml['creds']['client_id']}",
            "Authorization": f"Bearer {config.yaml['creds']['access_token']}",
        }
        self.api_oauth_token = "https://id.twitch.tv/oauth2/token"
        self.api_users = "https://api.twitch.tv/helix/users"

    def get_access_token(self, client_id, client_secret):
        """Obtain Twitch access token."""
        r = requests.post(
            self.api_oauth_token,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
        )

        return r

    def is_user_streaming(self): ...

    def is_user_valid(self, user):
        """Verify if given user is valid on Twitch."""
        r = requests.get(
            self.api_users + f"?login={user}", headers=self.api_headers
        )
        if r.status_code == 200:
            if not r.json()["data"]:
                return False

            return True

        return False

    def get_usericon(self, config: TwinerConfig, user):
        """Get usericon from a user on Twitch."""
        r = requests.get(
            self.api_users + f"?login={user}", headers=self.api_headers
        )
        if r.status_code == 200:
            icon_url = r.json()["data"][0]["profile_image_url"]
            if not icon_url:
                return ""

            config.create_datadir()
            output = config.DEFAULT_DATA_DIR + f"/{user}.png"
            wget.download(icon_url, out=output)

            return output

        return ""

    def notification_loop(self): ...