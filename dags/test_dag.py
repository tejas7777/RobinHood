import unittest
from airflow.models import DagBag
from feed_scrapper import collect_feeds
from airflow.models import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.utils.dates import days_ago
from datetime import datetime


class TestDAG(unittest.TestCase):
    dag_id = None 
    dagbag = None

    def setUp(self):
        self.dagbag = DagBag(dag_folder='.', include_examples=False)
        self.dag_id = 'collect_feeds_dag'

    def test_dag_loading(self):
        dag = self.dagbag.get_dag(self.dag_id)
        self.assertIsNotNone(dag)

    def test_task_count(self):
        dag = self.dagbag.get_dag(self.dag_id)
        self.assertEqual(len(dag.tasks), 2)

    # def test_load_feed_data_to_db(self):
    #     # Create a DAG object
    #     #dag = DAG(dag_id=self.dag_id, schedule_interval=None, start_date=days_ago(1))
    #     dag = self.dagbag.get_dag(self.dag_id)

    #     # Run the specific task using TaskInstance
    #     task_instance = TaskInstance(task=dag.get_task('load_feed_data_to_db'))
    #     result = task_instance.run(ignore_ti_state=True)

    #     # Perform assertions on the task result or other expected behavior
        

if __name__ == '__main__':
    unittest.main()