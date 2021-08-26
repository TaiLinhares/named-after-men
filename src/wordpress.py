from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from jinja2 import Environment, FileSystemLoader
from loguru import logger

logger = logger.bind(name="Plants")


#############################################################
#                       Functions                           #
#############################################################


def wordpress_connect(WP_URL, WP_USER, WP_PASS):
    """Connects to Wordpress and returns wp object"""
    wp = Client(WP_URL, WP_USER, WP_PASS)

    return wp


def wordpress_up_media(wp, filename):
    """Uploads picture to Wordpress
    wp: wordpress object
    filename: str, path to file to be uploaded

    returns wordpress media object"""

    # prepare metadata
    data = {
        "name": "plant.jpg",
        "type": "image/jpeg",
    }

    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename, "rb") as img:
        data["bits"] = xmlrpc_client.Binary(img.read())

    wp_media = wp.call(media.UploadFile(data))

    return wp_media


def wp_message(post_day, name, wiki, synonyms, men, year, countries, img, imgsrc):
    """Uploads media file to wordpress library, and creates post object

    Attributes
    post_day: int, day since the project started
    name: str, plant scientific name
    wiki: str, plant wiki page
    synonyms: str, concatenated synonyms
    men: str, concatenated botanists names
    year: int, year first catalogued
    countries: str, concatenated native country names
    img: str, image original source
    imgsrc: str, wordpress image url

    returns: a string with html post content
    """
    content_text = ""

    file_loader = FileSystemLoader("templates")

    env = Environment(loader=file_loader)

    template = env.get_template("wp_template.html")

    content_text = template.render(
        imgsrc=imgsrc,
        img=img,
        post_day=str(post_day),
        name=name,
        wiki=wiki,
        synonyms=synonyms,
        men=men,
        year=str(year),
        countries=countries,
    )

    return content_text



def wordpress_post(wp, title, message_wp, tags, category):
    """Posts to wordpress"""

    post = WordPressPost()
    post.post_status = "publish"
    post.title = title
    post.content = message_wp
    post.comment_status = "open"
    post.excerpt = "named after Men"
    post.terms_names = {"post_tag": tags, "category": category}

    wp.call(NewPost(post))
