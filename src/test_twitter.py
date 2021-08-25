import unittest
from jinja2 import Environment, FileSystemLoader
from twitter import twitter_message


class TestTwitter(unittest.TestCase):

    cfa = ". Data is not neutral, let's start this conversation. "
    "Know the project at www.namedaftermen.com #namedaftermen "
    "#decolonizescience #data #botanics"
    lim = 280 - (len(cfa) + 2) #len cfa = 54, lim = 224

    def test_twitter_message(self):

        test_template = "#1 Beautiful planta, also Planta bonita. Named after male botanists Man, Hombre, and Homem" + self.cfa

        #{{ post_day }} {{ name }}{% if synonyms != '' %}, also {% endif %}{{ synonyms }}{% if ',' in men %}. Named after male botanists {% else %}. Named after male botanist {% endif %}{{ men }}
        self.assertEqual(twitter_message(1, "Beautiful planta", "Planta bonita", "Man, Hombre, and Homem", self.cfa), test_template)
