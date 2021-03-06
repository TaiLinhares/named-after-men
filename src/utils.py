import requests
from loguru import logger
from notifications import send_email

logger = logger.bind(name="Plants")


def text_concat(names, tag_o="", tag_c="", lim=0):
    """Concatenate list of names and apply conjunction
        names: list, strings to be concatenated.
        tag_o: str, opening html tag.
        tag_c: str, closing html tag.
        lim: int, maximum items to be concatenated.
        returns concatenated list of names"""

    text = ""

    if lim > 0 and lim <= len(names):
        names = names[:lim]
    else:
        lim = len(names)

    for i, m in enumerate(names):
        if lim == 1:
            text += tag_o + m + tag_c

        elif (lim - 1) == i:
            text += "and " + tag_o + m + tag_c

        else:
            text += tag_o + m + tag_c + ", "

    return text


def get_pic(img_url, SENDGRID_API_KEY, NOTIFY_EMAIL):
    """Download picture to directory and notify if not possible"""

    filename = "temp.jpg"
    try:
        request = requests.get(img_url, stream=True, verify=False)
        if request.status_code == 200:
            with open(filename, "wb") as image:
                for chunk in request:
                    image.write(chunk)
        else:
            logger.info("Could not download picture, so image is placeholder.")
            filename = "src/img/image-not-found.jpg"
            # filename = "img/image-not-found.jpg"
    except Exception as e:
        logger.info("Could not download picture, so image is placeholder.")
        send_email(e, SENDGRID_API_KEY, NOTIFY_EMAIL, "picture is placeholder")
        filename = "src/img/image-not-found.jpg"
        # filename = "img/image-not-found.jpg"
    finally:
        return filename
