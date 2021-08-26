import unittest
from wordpress import wp_message

class TestWordpress(unittest.TestCase):

    def test_wp_message(self):

        with open(".test_templates/test_wp_template.txt") as f:
            test_template = f.read()
        
        self.assertEqual(wp_message("1", 
                            "Beautiful planta",
                            "www.wikipedia.org",
                            "Planta bonita",
                            "Mand, or Homem",
                            1987,
                            "Brazil-Southeast, and Brazil-Northeast.",
                            "www.plant.org",
                            "https://namedaftermen.com/wp-content/uploads/2021/08/plant-24.jpg"), test_template)
