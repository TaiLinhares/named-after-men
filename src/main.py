import os
from dotenv import load_dotenv
import datetime
import psycopg2
from twitter import twitter_connect,twitter_up_media,twitter_message,twitter_post
from wordpress import wordpress_connect,wordpress_up_media,wp_message,wordpress_post
from utils import text_concat,get_pic

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


# Define standard post text and formatting variables

# Call for action to the project to be posted on Twitter
call_for_action = ". Data is not neutral, let's start this conversation. Know the project at www.namedaftermen.com #namedaftermen #decolonizescience #data #botanics"


#############################################################
####################### Functions ###########################
#############################################################

def get_plant():
    '''Connects with plantsdb database and queries the plant of the day
    Returns tuple corresponding to the plant's row in DB'''

    # Define post ID
    start_day = datetime.date(2021,7,10)
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
        plant = cursor.fetchall()
        # print(plant)
    else:
        print('Project is over')
        return

    # Close local database
    conn.commit()
    print("Database has been closed........")
    conn.close()

    return plant



def main():
    
    # Defining database array index to each peace of information
    from_db_get = {
        'Id':0,
        'Name':1,
        'Img_url':2,
        'Year':3,
        'Plant_url':4,
        'Synonyms':5,
        'Botanists_wp':6,
        'Botanists_ttr':7,
        'Countries':8
    }

    # Gets plant of the day
    query_content = get_plant()

    # Retrieves content to post
    day = query_content[0][from_db_get['Id']]
    scientific_name = query_content[0][from_db_get['Name']]
    img_url = query_content[0][from_db_get['Img_url']]
    year = query_content[0][from_db_get['Year']]
    plant_url = query_content[0][from_db_get['Plant_url']]
    synonyms = query_content[0][from_db_get['Synonyms']]
    botanists_wp = query_content[0][from_db_get['Botanists_wp']]
    botanists_ttr = query_content[0][from_db_get['Botanists_ttr']]
    countries = query_content[0][from_db_get['Countries']]
    
    # Define tags and category
    tags = countries
    category = ['Plants']
    title = '<i>' + scientific_name + '</i>'
    
    # Concatenate plant synonyms and countries
    t_o = '<i>'
    t_c = '</i>'
    syn_concat_wp = text_concat(synonyms,t_o,t_c)
    syn_concat_ttr = text_concat(synonyms)
    ctr_concat = text_concat(countries)
    
    # Download picture to directory
    filename = get_pic(img_url)
    
    # Connect to Wordpress and Twitter
    wp = wordpress_connect(WP_URL, WP_USER, WP_PASS)
    api = twitter_connect(TWITTER_API_KEY, TWITTER_API_SECRET_KEY,TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    
    
    # Upload picture to Wordpress and Twitter
    wp_img = wordpress_up_media(wp,filename)
    wp_img_url = wp_img['url']
    
    tttr_media = twitter_up_media(api,filename)
    
    # Create WP HTML post content and twitter message
    message_wp = wp_message(day,scientific_name,plant_url,syn_concat_wp,botanists_wp,year,ctr_concat,img_url,wp_img_url)
    message_twitter = twitter_message(day, scientific_name,syn_concat_ttr,botanists_ttr,call_for_action)
    
    
    # Post to Wordpress and Twitter (To Do: handle tweepy code 186 by shortening message_twitter and trying again)
    wordpress_post(wp,title,message_wp,tags,category)

    # twitter_post(api,message_twitter,tttr_media)

    os.remove(filename)

if __name__ == "__main__":
    main()
