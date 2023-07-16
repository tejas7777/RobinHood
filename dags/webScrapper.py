''''
Initialize a web scrapping dag to collect data and push to a MongoDB data base
'''

from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.redis.hooks.redis import RedisHook
from helper import webScrapperHelper
from airflow.operators.python import PythonOperator


configuration: dict = {
    'REDIS_CONN_ID': 'redis_default'
}


@dag(
    start_date=datetime(2023, 7, 16), max_active_runs=3, catchup=False, description= 'Web Scrapper',
    schedule_interval= '*/60 * * * * *'
)
def webScrap():
    URL_SET_KEY = 'url_set'

    #Gets list of URLs to scrape from Redis
    @task(task_id='get_urls')
    def getURLS():
        redisConn = RedisHook(configuration.get('REDIS_CONN_ID')).get_conn()
        urlSet = redisConn.smembers(URL_SET_KEY)
        print('[DAG][webScrap][getURLS] redis urlSet', urlSet)
        if urlSet == None:
            return None

        filteredUrlList = webScrapperHelper.filterUnreachableWebsites(urlSet=urlSet)
            
        print('[DAG][webScrap][getURLS][filtered] redis urlSet',filteredUrlList)

        return None
        
    getURLS()



webScrap()