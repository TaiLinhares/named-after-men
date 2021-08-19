import requests


def text_concat(names, tag_o="", tag_c=""):
    """Concatenate list of names and apply conjunction
    Returns concatenated list of names"""

    text = ""

    for i, m in enumerate(names):
        if len(names) == 1:
            text += tag_o + m + tag_c

        elif (len(names) - 1) == i:
            text += "and " + tag_o + m + tag_c

        else:
            text += tag_o + m + tag_c + ", "

    return text


def get_pic(img_url):
    """Download picture to directory"""

    filename = "temp.jpg"
    request = requests.get(img_url, stream=True)
    if request.status_code == 200:
        with open(filename, "wb") as image:
            for chunk in request:
                image.write(chunk)
    else:
        filename = "img/image-not-found.jpg"

    return filename
