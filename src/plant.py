import datetime

from loguru import logger
import psycopg2

logger = logger.bind(name="Plants")

from_db_get = {
    "Id": 0,
    "Name": 1,
    "Img_url": 2,
    "Year": 3,
    "Plant_url": 4,
    "Synonyms": 5,
    "Botanists_wp": 6,
    "Botanists_ttr": 7,
    "Countries": 8,
}


class Plant():

    def __init__(self, PSQL_USER, PSQL_PASS, DATABASE, HOST):

        self.PSQL_USER = PSQL_USER
        self.PSQL_PASS = PSQL_PASS
        self.DATABASE = DATABASE
        self.HOST = HOST

        query_content = self.get_plant()

        self.day = query_content[0][from_db_get["Id"]]
        self.scientific_name = query_content[0][from_db_get["Name"]]
        self.img_url = query_content[0][from_db_get["Img_url"]]
        self.year = query_content[0][from_db_get["Year"]]
        self.plant_url = query_content[0][from_db_get["Plant_url"]]
        self.synonyms = query_content[0][from_db_get["Synonyms"]]
        self.botanists_wp = query_content[0][from_db_get["Botanists_wp"]]
        self.botanists_ttr = query_content[0][from_db_get["Botanists_ttr"]]
        self.countries = query_content[0][from_db_get["Countries"]]

    def get_plant(self):
        """Connects with plantsdb database and queries the plant of the day
        Returns tuple corresponding to the plant's row in DB"""

        # Define post ID
        start_day = datetime.date(2021, 7, 8)
        today = datetime.date.today()
        post_idx = (today - start_day).days + 1

        # Connect with local postgresql database
        conn = psycopg2.connect(
            database=self.DATABASE,
            user=self.PSQL_USER,
            password=self.PSQL_PASS,
            host=self.HOST,
            port="5432",
        )
        conn.autocommit = True
        cursor = conn.cursor()

        logger.info("Database has been opened........")

        # Find out database length
        q = "SELECT COUNT(*) FROM plantsdb"
        cursor.execute(q)
        total_items = cursor.fetchall()[0][0]

        # Check if there is still content to post
        if post_idx <= total_items:
            q = "SELECT * FROM plantsdb WHERE Id =" + str(post_idx)
            cursor.execute(q)
            plant = cursor.fetchall()

        else:
            logger.info("Project is over")
            conn.commit()
            logger.info("Database has been closed........")
            conn.close()

            return

        # Close local database
        conn.commit()
        logger.info("Database has been closed........")
        conn.close()

        return plant
