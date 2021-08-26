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


def check_dtype(obj, dt):
    '''obj: tuple, with objects to check type.
        dt: list, object data types to check against.'''
    wrong = []
    status = True
    if len(obj) != len(dt):
        return (False, None)
    else:
        for o, t in zip(obj, dt):
            print(o, " - ", t)
            if not isinstance(o, t):
                wrong.append({o: type(o)})
                status = False
        if len(wrong) > 0:
            return (status, wrong)
        else:
            return (status, None)
