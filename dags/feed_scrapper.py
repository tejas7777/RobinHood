''''
Initialize a web scrapping dag to collect data and push to a MongoDB data base
'''

from cmath import log
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.redis.hooks.redis import RedisHook
from helper import feed_helper
import json
from config.logging_confg import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


configuration: dict = {
    'REDIS_CONN_ID': 'redis_default'
}


@dag(
    start_date=datetime(2023, 7, 16), max_active_runs=3, catchup=False, description='Web Scrapper',
    schedule_interval='*/60 * * * * *',
    dag_id='collect_feeds_dag'
)
def collect_feeds():
    URL_SET_KEY = 'url_set'

    # Gets list of Feed URLs to scrape from Redis
    @task(task_id='get_feed_data')
    def get_feed_data():
        redis_conn = RedisHook(configuration.get('REDIS_CONN_ID')).get_conn()
        url_set = redis_conn.smembers(URL_SET_KEY)
        if url_set == None:
            return None

        filtered_url_list = feed_helper.load_feeds(url_set=url_set)

        return {"data": json.dumps(filtered_url_list)}

    @task(task_id='load_feed_data_to_db')
    def load_feed_data_to_db(data: dict[str:str]):
        if not data:
            return  

        json_data = json.loads(data["data"])
        logging.info(f"[DAG][collect_feeds][load_feed_Data_to_db] ${json_data}")


    load_feed_data_to_db(get_feed_data())

collect_feeds()
