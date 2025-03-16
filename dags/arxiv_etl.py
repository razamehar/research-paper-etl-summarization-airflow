from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta
from utils import fetch_papers, summarize_text


POSTGRES_CONN_ID = 'postgres_default'

default_args = {
    'owner': 'raza_mehar',
    'start_date': days_ago(1),  # Your start date here
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(dag_id='arvix_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         # schedule_interval=timedelta(minutes=2),
         catchup=False) as dag:

    @task()
    def extract():
        return fetch_papers("Machine Learning")


    @task()
    def transform(extracted_data):
        for paper in extracted_data:
            paper["short_summary"] = summarize_text(paper["summary"])
        return extracted_data

    @task()
    def load(transformed_data):
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS arvix_data (
                id SERIAL PRIMARY KEY,
                title TEXT,
                published_date DATE,
                url TEXT UNIQUE,
                short_summary TEXT,                
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            for paper in transformed_data:
                # Check if the paper already exists by URL
                cursor.execute("""
                    SELECT 1 FROM arvix_data WHERE url = %s;
                """, (paper["url"],))

                if cursor.fetchone() is None:  # If no existing record found, insert
                    cursor.execute("""
                        INSERT INTO arvix_data (title, published_date, url, short_summary) 
                        VALUES (%s, %s, %s, %s);
                    """, (paper["title"], paper["published"], paper["url"], paper["short_summary"]))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error inserting into PostgreSQL: {str(e)}")
        finally:
            cursor.close()
            conn.close()


    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)








