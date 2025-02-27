import streamlit as st
import os
import sqlite3
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from database import create_database_from_csv, create_database_from_url
import pandas as pd

# Load environment variables (e.g., GROQ_API_KEY)
load_dotenv()


def get_sql_query_from_text(user_query, table_name, columns, db_name):
    """
    Dynamically builds the prompt using the table name and its columns.
    Then it calls the LLM to convert the user’s natural language question to SQL.
    """
    columns_str = ", ".join(columns)

    column_values = {col: get_column_values(
        db_name, table_name, col) for col in columns}
    # Format detected column values
    # Only show categorical values (not too many)
    value_info = "\n".join([f"- Column '{col}' has unique values: {values}" for col,
                           values in column_values.items() if len(values) < 20])

    prompt_template = ChatPromptTemplate.from_template(f"""
        You are an expert in converting English questions to SQL query!
        The SQL database has the table {table_name} and has the following columns - {columns_str}.
        Ensure that column names are case-sensitive. If a column name is lowercase in the database, it should be lowercase in the query.
        For example,
        Example 1 - How many entries of records are present?,
            the SQL command will be something like: SELECT COUNT(*) FROM {table_name};
        Example 2 - Retrieve all records where a certain condition holds,
            the SQL command will be something like: SELECT * FROM {table_name} WHERE <condition>;

        Important Notes:
        {value_info}

        Use the correct values from the dataset when generating queries.

        ### IMPORTANT RULES:
        - ONLY return a valid SQL query.
        - DO NOT include any explanations, preambles, or formatting like triple backticks.
        - SQL must be syntactically correct for SQLite.

        Now convert the following question in English to a valid SQL Query: {{user_query}}.
        No preamble, only valid SQL please.
    """)
    model = "llama3-8b-8192"
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name=model
    )
    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query})
    return response.strip()


def get_data_from_database(sql_query, db_name):
    """
    Executes the SQL query on the SQLite database and returns all fetched records along with column names.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.execute(sql_query)
        data = cursor.fetchall()
        columns = [desc[0]
                   for desc in cursor.description]  # Extract column names
    return data, columns  # Return both data and column names


# this function can be used to dynamically detect values stored in any column!
def get_column_values(db_name, table_name, column_name):
    """
    Fetches distinct values from a given column in the SQLite database.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.execute(
            f"SELECT DISTINCT {column_name} FROM {table_name}")
        values = [row[0] for row in cursor.fetchall()]
    return values


def main():
    st.set_page_config(page_title="Dynamic SQL Assistant")
    st.title("Dynamic SQL Assistant for CSV and Online Data")

    # Let the user choose the data source.
    data_source = st.radio("Choose Data Source",
                           ("Upload CSV", "Enter Kaggle/Online CSV URL"))

    db_name = "data.db"
    table_name = "DATA"
    columns = None  # This will be set after loading the CSV

    # Option 1: CSV upload
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file is not None:
            db_name, table_name, columns = create_database_from_csv(
                uploaded_file, db_name=db_name, table_name=table_name)
            st.success(
                f"Database created from uploaded CSV. Table '{table_name}' with columns: {columns}")

    # Option 2: CSV URL
    else:
        csv_url = st.text_input("Enter the CSV URL (e.g., Kaggle data URL)")
        if csv_url:
            try:
                db_name, table_name, columns = create_database_from_url(
                    csv_url, db_name=db_name, table_name=table_name)
                st.success(
                    f"Database created from URL. Table '{table_name}' with columns: {columns}")
            except Exception as e:
                st.error(f"Error fetching data from URL: {e}")

    # Only show query options if the database is ready.
    if columns:
        st.markdown("---")
        st.subheader("Ask SQL Queries in English")
        user_query = st.text_area("Enter your question:", height=100)
        if st.button("Submit Query"):
            try:
                sql_query = get_sql_query_from_text(
                    user_query, table_name, columns, db_name)
                st.info(f"Generated SQL Query: {sql_query}")
                # data = get_data_from_database(sql_query, db_name)
                data, column_names = get_data_from_database(sql_query, db_name)
                # st.write("Query Results:")
                # st.write(data)
                st.write("Query Results:")
                if data:
                    df = pd.DataFrame(data, columns=column_names)
                    st.dataframe(df)
                else:
                    st.write("No results found.")
            except Exception as e:
                st.error(f"Error executing query: {e}")


if __name__ == '__main__':
    main()
