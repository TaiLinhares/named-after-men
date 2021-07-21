from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts


# HTML

# columns
div_o = '<div class="wp-block-columns">'
div_c = '</div>'

div_col_o = '<div class="wp-block-column" style="flex-basis:50%">'
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


def wordpress_connect(WP_URL, WP_USER, WP_PASS):
    '''Connects to Wordpress and returns wp object'''
    wp = Client(WP_URL, WP_USER, WP_PASS)

    return wp

def wordpress_up_media(wp,filename):
    '''Uploads picture to Wordpress
        wp: wordpress object
        filename: str, path to file to be uploaded
        
        returns wordpress media object'''

    ## prepare metadata
    data = {
            'name': 'plant.jpg',
            'type': 'image/jpeg',
    }
    
    ## read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

    wp_media = wp.call(media.UploadFile(data))

    return wp_media


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
    if isinstance(wiki,type(None)):
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

def wordpress_post(wp,title,message_wp,tags,category):
    '''Posts to wordpress'''

    post = WordPressPost()
    post.post_status = 'publish'
    post.title = title
    post.content = message_wp
    post.comment_status = 'open'
    post.excerpt = 'Named after men'
    post.terms_names = {
        "post_tag": tags,
        "category": category
    }

    wp.call(NewPost(post))
    