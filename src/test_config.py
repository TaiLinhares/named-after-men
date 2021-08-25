import unittest
from dotenv import load_dotenv
import os

load_dotenv()

class TestConf(unittest.TestCase):        
    
    keys = ["ttr_user", "API_key", "API_Secret_Key", "Bearer_Token", "Access_Token", 
        "Access_Token_Secret", "wp_user", "wp_password", "url", "psql_user", "psql_password", 
        "database", "host", "sendgrid_api_key", "notify_email"]

    def test_env_keys_exist(self):

        for k in self.keys:
            self.assertIsNotNone(os.getenv(k))
    
    def test_env_values_not_empty(self):

        for k in self.keys:
            self.assertNotEqual(os.getenv(k),"")
