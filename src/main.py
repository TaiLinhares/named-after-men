import os
import sys
from loguru import logger

from config import Config
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
    wp_excerpt,
    wordpress_post,
)
from utils import text_concat, get_pic


# Call for action to the project to be posted on Twitter
call_for_action = (
    ". Data is not neutral, go to www.namedafterMen.com "
    "and join the conversation. "
    "#NamedAfterMen #DecolonizeScience #Data #Botanics"
)


#############################################################
#                       Functions                           #
#############################################################


def main():

    env = Config()

    if env.val_config():
        logger.info("All environment variables exist.")
    else:
        logger.info("Some environment variables do not exist.")
        sys.exit()

    try:
        # Gets plant of the day
        plant = Plant(
            env.CONF["PSQL_USER"],
            env.CONF["PSQL_PASS"],
            env.CONF["DATABASE"],
            env.CONF["HOST"])

        if plant is None:
            sys.exit()

        # Define tags and category
        tags = plant.countries
        category = ["Plants"]
        title = plant.scientific_name
        slug = str(plant.day) + " " + plant.scientific_name

        # Concatenate plant synonyms and countries
        t_o = "<i>"
        t_c = "</i>"
        syn_concat_wp = text_concat(plant.synonyms, t_o, t_c)
        syn_concat_wp_short = text_concat(plant.synonyms, t_o, t_c, lim=2)
        syn_concat_ttr = text_concat(plant.synonyms, lim=2)
        ctr_concat = text_concat(plant.countries) + "."

        # Download picture to directory
        filename = get_pic(plant.img_url, env.CONF["SENDGRID_API_KEY"], env.CONF["NOTIFY_EMAIL"])

        # Connect to Wordpress and Twitter
        wp = wordpress_connect(env.CONF["WP_URL"], env.CONF["WP_USER"], env.CONF["WP_PASS"])
        api = twitter_connect(
            env.CONF["TWITTER_API_KEY"],
            env.CONF["TWITTER_API_SECRET_KEY"],
            env.CONF["TWITTER_ACCESS_TOKEN"],
            env.CONF["TWITTER_ACCESS_TOKEN_SECRET"],
        )
        logger.info("Connected to Wordpress and Twitter...")
        logger.info("This is a test.")
        # Upload picture to Wordpress and Twitter
        wp_img = wordpress_up_media(wp, filename)
        wp_img_url = wp_img["url"]
        wp_img_id = wp_img["id"]
        logger.info("Uploaded media in Wordpress...")
        tttr_media = twitter_up_media(api, filename)
        logger.info("Uploaded media in Twitter...")
        # Create WP excerpt text
        excerpt_text = wp_excerpt(
            plant.scientific_name,
            syn_concat_wp_short,
            plant.botanists_ttr,
            lim=300
        )

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
        wordpress_post(wp, title, message_wp, tags, category, slug, wp_img_id, excerpt_text)
        logger.info("Posted to Wordpress...")
        twitter_post(api, message_twitter, tttr_media)
        logger.info("Posted to Twitter...")

        logger.info("Congratulations, a new plant has been posted!")

        if os.path.isfile("temp.jpg"):
            os.remove("temp.jpg")
            logger.info("temp.jpg removed from environment.")

    except Exception as e:
        logger.info(f"Check exception: {e}")
        send_email(e, env.CONF["SENDGRID_API_KEY"], env.CONF["NOTIFY_EMAIL"])


if __name__ == "__main__":
    main()
