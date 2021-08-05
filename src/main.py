import os
import datetime
from loguru import logger
import psycopg2

from config import CONF
from plant import Plant
from notifications import send_email
from twitter import (
    twitter_connect,
    twitter_up_media,
    twitter_message,
    twitter_post,
)
from wordpress import (
    wordpress_connect, 
    wordpress_up_media, 
    wp_message, 
    wordpress_post,
)
from utils import text_concat, get_pic


# Call for action to the project to be posted on Twitter
call_for_action = (
    ". Data is not neutral, let's start this conversation. "
    "Know the project at www.namedaftermen.com #namedaftermen "
    "#decolonizescience #data #botanics"
)

# initialize logger
# logger = logger.bind(name="Plants")

#############################################################
#                       Functions                           #
#############################################################



def main():

    try:
        # Test email notification: 
        # raise ValueError("A very specific bad thing just happened.")

        # Gets plant of the day
        plant = Plant(CONF["PSQL_USER"], CONF["PSQL_PASS"])

        # Define tags and category
        tags = plant.countries
        category = ["Plants"]
        title = "<i>" + plant.scientific_name + "</i>"

        # Concatenate plant synonyms and countries
        t_o = "<i>"
        t_c = "</i>"
        syn_concat_wp = text_concat(plant.synonyms, t_o, t_c)
        syn_concat_ttr = text_concat(plant.synonyms)
        ctr_concat = text_concat(plant.countries)

        # Download picture to directory
        filename = get_pic(plant.img_url)

        # Connect to Wordpress and Twitter
        wp = wordpress_connect(CONF["WP_URL"], CONF["WP_USER"], CONF["WP_PASS"])
        api = twitter_connect(
            CONF["TWITTER_API_KEY"],
            CONF["TWITTER_API_SECRET_KEY"],
            CONF["TWITTER_ACCESS_TOKEN"],
            CONF["TWITTER_ACCESS_TOKEN_SECRET"],
        )
        logger.info("Connected to Wordpress and Twitter...")

        # Upload picture to Wordpress and Twitter
        wp_img = wordpress_up_media(wp, filename)
        wp_img_url = wp_img["url"]

        tttr_media = twitter_up_media(api, filename)

        # Create WP HTML post content and twitter message
        message_wp = wp_message(
            plant.day,
            plant.scientific_name,
            plant.plant_url,
            syn_concat_wp,
            plant.botanists_wp,
            plant.year,
            ctr_concat,
            plant.img_url,
            wp_img_url,
        )
        message_twitter = twitter_message(
            plant.day, plant.scientific_name, syn_concat_ttr, plant.botanists_ttr, call_for_action
        )

        # Post to Wordpress and Twitter (To Do: handle tweepy code 186 by
        # shortening message_twitter and trying again)
        wordpress_post(wp, title, message_wp, tags, category)

        twitter_post(api, message_twitter, tttr_media)

        logger.info("Plant has already been posted.")

        os.remove(filename)
    
    except Exception as e:
        send_email(e, CONF["SENDGRID_API_KEY"], CONF["NOTIFY_EMAIL"])



if __name__ == "__main__":
    main()
