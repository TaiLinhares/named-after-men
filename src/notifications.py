from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from loguru import logger

logger = logger.bind(name="Plants")

def send_email(e, SENDGRID_API_KEY, NOTIFY_EMAIL):


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
        How are you?
        <p>Something went wrong in the Plants project:</p>
        <p><b>%s</b></p>
        <p> Do not freak out, everything is gona be ok. :)</p>
        <br>
        Hugs!<br>
        you
    </body>
    </html>
    """ % (e)


    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(NOTIFY_EMAIL)
    to_email = To(NOTIFY_EMAIL)
    subject = "Issue in Plants project"
    content = Mail(from_email,
            to_email,
            subject,
            plain_text_content=PlainTextContent(text),
            html_content=HtmlContent(html))
    response = sg.send(message=content)
    logger.info(response.status_code)
    logger.info((response.body).decode("utf-8")) # is empty, see why
    logger.info(response.headers)
