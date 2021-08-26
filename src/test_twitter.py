import unittest
from twitter import twitter_message


class TestTwitter(unittest.TestCase):
    # len(cfa) = 145, lim = 133
    # Limit of text - cfa is 133, if longer substitute last two chr for ".."
    cfa = (". Data is not neutral, let's start this conversation. "
           "Know the project at www.namedaftermen.com #namedaftermen "
           "#decolonizescience #data #botanics")

    lim = 280 - (len(cfa) + 2)

    def test_twitter_message(self):

        test_template = []
        with open("test_templates/test_tttr_template.txt") as f:
            test_template = f.readlines()

        # {{ post_day }} {{ name }}{% if synonyms != '' %}, also {% endif %}{{ synonyms }}
        # {% if ',' in men %}. Named after male botanists {% else %}. Named after male botanist
        #  {% endif %}{{ men }}

        test_cases = [(1, "Beautiful planta", "Planta bonita", "Man, Hombre, and Homem", self.cfa),
                      (2, "Nova planta", "", "Man, and Hombre", self.cfa),
                      (3,
                       "Planta plantarus", "Planta one, Planta two, Planta three, and Planta four",
                       "A. Man, or B. Man, and C. Man, or D. Man", self.cfa),
                      (4, "Awesome plant", "Plant bela", "Man, or Homem", self.cfa),
                      (5, "Nice plant", "Plant bela", "Mand, or Homem", self.cfa)]

        for c, t in zip(test_cases, test_template):
            self.assertEqual(twitter_message(*c), t.rstrip())
