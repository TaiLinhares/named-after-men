from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from loguru import logger

logger = logger.bind(name="Plants")

def send_email(e, SENDGRID_API_KEY):


    # Create the body of the message (a plain-text and an HTML version).
    # text is your plain-text email
    # html is your html version of the email
    # if the reciever is able to view html emails then only the html
    # email will be displayed
    text = "Hi!\nHow are you?\n"


    html = """\n
    <html>
    <head></head>
    <body>
        Hi!<br>
        How are you?<p>
        Weather.com says: It is %s F now in South San Francisco. <p>
        Yahoo says: It is F now in South San Francisco. <p>
        
        smooches, <br>
        the white rabbit
    </body>
    </html>
    """ % (e)


    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email("test@example.com")
    to_email = To("test@example.com")
    subject = "Sending with SendGrid is Fun"
    content = Mail(from_email,
            to_email,
            subject,
            plain_text_content=PlainTextContent(text),
            html_content=HtmlContent(html))
    response = sg.send(message=content)
    logger.info(response.status_code)
    logger.info(response.body)
    logger.info(response.headers)
