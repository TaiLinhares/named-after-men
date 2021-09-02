import unittest
from wordpress import wp_message, wp_excerpt


class TestWordpress(unittest.TestCase):

    def test_wp_message(self):

        with open("test_templates/test_wp_template.txt") as f:
            test_template = f.read()

        self.assertEqual(
            wp_message(
                "1",
                "Beautiful planta",
                "www.wikipedia.org",
                "Planta bonita",
                "Mand, or Homem",
                1987,
                "Brazil-Southeast, and Brazil-Northeast.",
                "www.plant.org",
                "https://namedaftermen.com/wp-content/uploads/2021/08/plant-24.jpg"),
            test_template)

    def test_wp_excerpt(self):

        test_template = []
        with open("test_templates/test_wp_excerpt_template.txt") as f:
            test_template = f.readlines()

        test_cases = [
            ("Beautiful planta",
             "<i>Planta bonita</i>",
             "Man, Hombre, and Homem"),
            ("Nova planta",
             "",
             "Man, and Hombre"),
            ("Planta plantarus",
             "<i>Planta one</i>, <i>Planta two</i>, <i>Planta three</i>, and <i>Planta four</i>",
             "A. Man, or B. Man, and C. Man, D. Man, or E. Man"),
            ("Planta plantarus",
             "<i>Planta one</i>, <i>Planta two</i>, <i>Planta three</i>, and <i>Planta four</i>",
             "A. Man, or B. Man, and C. Man, D. Man, or E. Man",
             150)]

        for c, t in zip(test_cases, test_template):
            self.assertEqual(wp_excerpt(*c), t.rstrip())
