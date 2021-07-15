import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import datetime
import psycopg2
import requests
import json
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import tweepy


# Load Environment variables
load_dotenv()

TWITTER_USER = os.getenv('ttr_user')
TWITTER_API_KEY = os.getenv('API_key')
TWITTER_API_SECRET_KEY = os.getenv('API_Secret_Key')
TWITTER_BEARER_TOKEN = os.getenv('Bearer_Token')
TWITTER_ACCESS_TOKEN = os.getenv('Access_Token')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('Access_Token_Secret')
WP_USER = os.getenv('wp_user')
WP_PASS = os.getenv('wp_password')
WP_URL = os.getenv('url')
PSQL_USER = os.getenv('psql_user')
PSQL_PASS = os.getenv('psql_password')

# Define post ID
start_day = datetime.date(2021,7,4)
today = datetime.date.today()
post_idx = (today - start_day).days + 1

# Connect with local postgresql database
conn = psycopg2.connect(
   database="postgres", user=PSQL_USER, password=PSQL_PASS, host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

# Find out database length
q = "SELECT COUNT(*) FROM plantsdb"
cursor.execute(q)
total_items = cursor.fetchall()[0][0]

# Check if there is still content to post
if post_idx <= total_items:
    q = "SELECT * FROM plantsdb WHERE Id =" + str(post_idx)
    cursor.execute(q)
    query_content = cursor.fetchall()
    print(query_content)
else:
    print('Project is over')

# Close local database
conn.commit()
print("Database has been closed........")
conn.close()

# Define standard post text and formatting variables

# Call for action to the project to be posted on Twitter
call_for_action = ". Data is not neutral, let's start this conversation. Know the project at www.namedaftermen.com #namedaftermen #decolonizescience #data #botanics"

# columns
div_o = '<div class=\"wp-block-columns\">'
div_c = '</div>'

div_col_o = '<div class=\"wp-block-column\" style=\"flex-basis:50%\">'
div_col_c = '</div>'

# text
p_text_o = '<p id="plant_text">'
p_text_c = '</p>'
span_o = '<span style="color: #d12b0e; font-size:3.6em; font-weight: 800; font-family: \'inter-val\',sans-serif; margin:0.05em 0.1em 0.1em 0; line-height: .68; float:left" >'
span_c = '</span>'
v_space = '<p></p><p></p><p></p>'

# image
fig_o = '<figure class="wp-block-image size-large is-style-default" id="plant_fig"><img src=\"'#+image wordpress url
caption = '\" alt="This plant\'s image" class="wp-image-29"/><figcaption>'#+caption_text
fig_c = '</figcaption></figure>'

# footer
footer_o = '<p class="has-text-align-center" id="plant_footer"><strong><span class="has-inline-color has-primary-color">Native to</span></strong> '#+countries
footer_c = '</p>'


# Functions
def wp_message(post_day, name, wiki, synonyms, men, year, countries, img, imgsrc):
    '''Uploads media file to wordpress library, and creates post object
    
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
    '''
    content_text = ''
    
    if synonyms != '':
        also = ', also known as '
    else:
        also = ''
        
    if ',' in men:
        hommage = '. I pay hommage to the male botanists '
    else:
        hommage = '. I pay hommage to the male botanist '
    
    # If plant do not have wiki page
    if isinstance(wiki[0],type(None)):
        p_name = '<i>' + name + '</i>'
    else:
        p_name = '<i><a href=\"' + wiki + '\">' + name + '</a></i>'
    
    # Text snippets
    presenting = span_o + '#' + str(post_day) + span_c + ' They called me ' + p_name
    catalogue = '. They first catalogued me in ' + str(year) + '.'
    caption_text = '<i>' + name + '</i>. See image source <a href=\"' + img + '\">here</a>.'
    
    # Create post columns and rows
    figure = div_col_o + fig_o + imgsrc + caption + caption_text + fig_c + div_col_c
    text = div_col_o + v_space + p_text_o + presenting + also + synonyms + hommage + men + catalogue + p_text_c + div_col_c
    row = div_o + figure + text + div_c
    footer = footer_o + countries + footer_c
    
    # Create final post
    content_text = row + footer
    
    return content_text

def twitter_message(post_day, name, synonyms, men, cfa):
    '''Uploads media file to Twitter, and creates message
    
    Attributes
    post_day: int, day since the project started
    name: str, plant scientific name
    synonyms: str, concatenated synonyms
    men: str, concatenated botanists names
    cfa: str, call for action to the project
    
    returns: a 280 characters string
    '''
    content_text = ''
    lim = 280 - len(cfa)
    
    if synonyms != '':
        also = ', also '
    else:
        also = ''
    
    if ',' in men:
        hommage = '. Named after male botanists '
    else:
        hommage = '. Named after male botanist '
        
        
    text = '#' + str(post_day) + ' ' + name + also + synonyms + hommage + men

    
    if len(text) > lim:
        content_text = text[:(lim-2)] + '..' + cfa
    else:
        content_text = text + cfa
    
    return content_text

def text_concat(names,tag_o='',tag_c=''):
    '''Concatenate list of names and apply conjunction'''
    text = ''
    
    for i,m in enumerate(names):
        if len(names) == 1:
            text += tag_o + m + tag_c
        
        elif (len(names)-1) == i:
            text += 'and ' + tag_o + m + tag_c

        else:
            text += tag_o + m + tag_c + ', '

    return text

def main():
    
    # Retrieves content to post
    day = query_content[0][0]
    scientific_name = query_content[0][1]
    img_url = query_content[0][2]
    year = query_content[0][3]
    plant_url = query_content[0][4]
    synonyms = query_content[0][5]
    botanists_wp = query_content[0][6]
    botanists_ttr = query_content[0][7]
    countries = query_content[0][8]
    
    # Define tags and category
    tags = countries
    category = ['Plants']
    title = scientific_name
    
    # Concatenate plant synonyms and countries
    t_o = '<i>'
    t_c = '</i>'
    syn_concat_wp = text_concat(synonyms,t_o,t_c)
    syn_concat_ttr = text_concat(synonyms)
    ctr_concat = text_concat(countries)
    
    # Download picture to directory
    filename = 'temp.jpg'
    request = requests.get(img_url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    else:
        return;
    
    # Connect to Wordpress
    wp = Client(WP_URL, WP_USER, WP_PASS)
    
    
    # Connect to Twitter
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    
    
    # Upload picture to Wordpress
    ## prepare metadata
    data = {
            'name': 'plant.jpg',
            'type': 'image/jpeg',  # mimetype
    }
    
    ## read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

    wp_img = wp.call(media.UploadFile(data))
    wp_img_url = wp_img['url']
    
    
    # Upload picture to twitter
    tttr_media = api.media_upload(filename)
    
    # Create WP HTML post content and twitter message
    message_wp = wp_message(day,scientific_name,plant_url,syn_concat_wp,botanists_wp,year,ctr_concat,img_url,wp_img_url)
    message_twitter = twitter_message(day, scientific_name,syn_concat_ttr,botanists_ttr,call_for_action)
    
    
    # WP Post
    post = WordPressPost()
    post.post_status = 'publish'
    post.title = title
    post.content = message_wp
    post.excerpt = 'Named after men'
    post.terms_names = {
        "post_tag": tags,
        "category": category
    }

    wp.call(NewPost(post))
    
    
    # Twitter Post
    # api.update_status(status=message_twitter, media_ids=[tttr_media.media_id])
    print(message_twitter)

    os.remove(filename)

if __name__ == "__main__":
    main()
