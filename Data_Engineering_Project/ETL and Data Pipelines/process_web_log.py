# import the libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# DAG arguments
default_args = {
    'owner': 'randomdude',
    'start_date': days_ago(0),
    'email': ['random@randomemail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Defining the DAG
dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='A DAG to process web logs',
    schedule_interval=timedelta(days=1),
)

# Task 1: Extract data from web server log
extract = BashOperator(
    task_id='extract_data',
    bash_command='cut -d" " -f1 /home/project/airflow/dags/capstone/accesslog.txt > /home/project/airflow/dags/capstone/extracted_data.txt',
    dag=dag,
)

# Task 2: Transform data (remove specific IP address)
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='sed "/198.46.149.143/d" /home/project/airflow/dags/capstone/extracted_data.txt > /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# Task 3: Load data into tar archive
load_data = BashOperator(
    task_id='load_data',
    bash_command='tar cvf weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# Task pipeline
extract >> transform_data >> load_data