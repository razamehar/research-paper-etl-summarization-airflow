# Research Paper Summarization using ETL Pipeline with Airflow

## Project Overview

This project automates the process of extracting, transforming, and loading (ETL) research papers from **Arxiv**, a popular open-access repository of research papers, based on any specified topic. The pipeline uses **Apache Airflow** to schedule and automate the tasks, ensuring that the process runs smoothly and consistently every day. The goal is to provide a database of curated research papers that include concise summaries of their contents, enabling quick access and easier review of the latest research in a wide range of academic fields.

The pipeline performs the following steps:

1. **Extraction**: It queries the Arxiv API to fetch metadata for research papers related to a specified topic (e.g., "Machine Learning"), including the paper's title, summary, publication date, and URL.
   
2. **Transformation**: The paper summaries are then processed using **OpenAI**'s API and **Langchain** to generate shorter, more concise summaries. This step ensures that users can quickly grasp the key points of each paper without needing to read the full abstract.

3. **Loading**: The processed data (including paper title, publication date, summary, and URL) is stored in a **PostgreSQL** database. Each paper's URL is used as a unique identifier to prevent duplicates.

By using **PostgreSQL** as the storage solution, the data is efficiently stored and can be queried for further analysis or review.

### What is Arxiv?

[Arxiv](https://arxiv.org/) is a free distribution service and repository for research papers, primarily in the fields of physics, mathematics, computer science, quantitative biology, quantitative finance, and more. It serves as a valuable resource for accessing cutting-edge academic research in these domains. Arxiv allows researchers to share their work with the community before it undergoes formal peer review and publication, making it a critical platform for academic collaboration.

### How it Works:

1. **Extract**: Fetches research papers from the Arxiv API using a search query based on a specified topic (e.g., "Machine Learning"). The API returns paper metadata such as title, summary, publication date, and URL.

2. **Transform**: Summarizes the papers using a pre-trained language model powered by OpenAI's API via Langchain. The summaries are stored alongside the original paper data for quick reference.

3. **Load**: Loads the transformed data into a PostgreSQL database, where a table is created to store each paper's details. Each entry is uniquely identified by the paper's URL, preventing duplicates.

### Why It’s Useful:
This pipeline helps automate the collection and summarization of academic research papers. It’s designed to be a scalable solution, so you can easily modify it to collect papers on any topic. By summarizing the papers, users can get quick insights into the content without needing to read each abstract in full. Moreover, by storing the data in a structured database, users can query and analyze papers efficiently.

## Requirements

- Python 3.8+
- Apache Airflow
- PostgreSQL
- Langchain OpenAI
- Arxiv Python Client
- dotenv

## Setup

1. **Install Astro CLI:**

To run Airflow locally, you need the **Astro CLI** from **astronomer.io**. Then you can run the following commands to 
- Initiate Airflow:
  ```bash
  astro dev init
  ```
  
- Start the project:
  ```bash
  astro dev start
  ```

2. **Create a Python virtual environment:**

  ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
  ```
   
3. **Install required dependencies:**

  ```bash
    pip install -r requirements.txt
  ```

3. **Set up PostgreSQL:**
Ensure that PostgreSQL is installed and running. The database must have a connection with the ID postgres_default, or you can modify the connection ID in the Airflow configurations.

## License
This project is licensed under the Raza Mehar License. See the LICENSE.md file for details.

## Contact
For any questions or clarifications, please contact Raza Mehar at [raza.mehar@gmail.com].








