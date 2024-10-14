from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import csv

# Define the paths for the CSV and text files
CSV_FILE_PATH = '/opt/bitnami/airflow/csv/input_file.csv'
TXT_FILE_PATH = '/opt/bitnami/airflow/txt/output_file.txt'

# Function to read CSV and write to a text file
def read_csv_write_txt():
    try:
        with open(CSV_FILE_PATH, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            with open(TXT_FILE_PATH, mode='w') as txt_file:
                for row in csv_reader:
                    txt_file.write(','.join(row) + '\n')
        print(f"CSV file {CSV_FILE_PATH} successfully written to {TXT_FILE_PATH}")
    except Exception as e:
        print(f"Error: {e}")

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
}

# Define the DAG
with DAG('csv_to_txt_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    # Task to read CSV and write to text
    process_csv_to_txt = PythonOperator(
        task_id='read_csv_write_txt',
        python_callable=read_csv_write_txt
    )

    # Task sequence
    process_csv_to_txt
