import tweepy
from jinja2 import Environment, FileSystemLoader


#############################################################
#                       Functions                           #
#############################################################


def twitter_connect(
    TWITTER_API_KEY,
    TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
):
    """Connects to Twitter and returns twitter object"""
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api


def twitter_up_media(api, filename):
    """Uploads picture to twitter
    api: twitter object
    filename: str, path to file to be uploaded

    returns twitter media object"""

    media = api.media_upload(filename)

    return media


def twitter_message(post_day, name, synonyms, men, cfa):
    """Uploads media file to Twitter, and creates message

    Attributes
    post_day: int, day since the project started
    name: str, plant scientific name
    synonyms: str, concatenated synonyms
    men: str, concatenated botanists names
    cfa: str, call for action to the project

    returns: a 280 characters string
    """
    content_text = ""

    # Message must be 2 characters shorter (278). Unfortunately I still didn't
    # figure out why.
    lim = 280 - (len(cfa) + 2)

    file_loader = FileSystemLoader("src/templates")
    # file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)

    template = env.get_template("tttr_template.txt")

    text = template.render(
        post_day=str(post_day), name=name, synonyms=synonyms, men=men
    )

    if len(text) > lim:
        content_text = text[: (lim - 2)] + ".." + cfa
    else:
        content_text = text + cfa

    return content_text



def twitter_post(api, message_twitter, tttr_media):
    """Posts to twitter"""

    # Create some control mechanism for this error message:
    # { code: 186, message: "Tweet needs to be a bit shorter." }
    api.update_status(status=message_twitter, media_ids=[tttr_media.media_id])
