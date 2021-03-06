from dotenv import load_dotenv
import os

# Load Environment variables
load_dotenv()


class Config():

    def __init__(self):

        self.CONF = {
            "TWITTER_USER": os.getenv("ttr_user"),
            "TWITTER_API_KEY": os.getenv("API_key"),
            "TWITTER_API_SECRET_KEY": os.getenv("API_Secret_Key"),
            "TWITTER_BEARER_TOKEN": os.getenv("Bearer_Token"),
            "TWITTER_ACCESS_TOKEN": os.getenv("Access_Token"),
            "TWITTER_ACCESS_TOKEN_SECRET": os.getenv("Access_Token_Secret"),
            "WP_USER": os.getenv("wp_user"),
            "WP_PASS": os.getenv("wp_password"),
            "WP_URL": os.getenv("url"),
            "PSQL_USER": os.getenv("psql_user"),
            "PSQL_PASS": os.getenv("psql_password"),
            "DATABASE": os.getenv("database"),
            "HOST": os.getenv("host"),
            "SENDGRID_API_KEY": os.getenv("sendgrid_api_key"),
            "NOTIFY_EMAIL": os.getenv("notify_email")
        }

    def val_config(self):

        for c in self.CONF.keys():
            if self.CONF[c] == "":
                return False

        return True
