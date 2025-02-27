# Text-to-SQL Dynamic Assistant: Project Documentation

## **1. Introduction**
The **Text-to-SQL Dynamic Assistant** is a powerful application that enables users to interact with databases using natural language. This project allows users to **upload CSV files or provide an online dataset URL**, dynamically convert their queries into SQL commands using **LLM (Llama 3, Groq, and LangChain)**, and retrieve results directly from a **SQLite database**.

![Screenshot 2025-02-27 at 2 40 45 AM](https://github.com/user-attachments/assets/e5654062-9fb2-4488-b477-8c59d8b66f5d)

## **2. Project Motivation**
### **Problem Statement**
- **Non-technical users struggle with SQL**: Many business analysts, product managers, and executives lack SQL expertise but need data insights.
- **Data dependency on technical teams**: Non-technical users rely on **Data Analysts** or **Engineers** for SQL queries.
- **Time-consuming process**: Writing SQL queries manually and debugging syntax issues can be slow and inefficient.

### **Solution**
This project eliminates the need for **SQL knowledge**, allowing **any user** to interact with databases **using plain English** and retrieve data in real-time.

## **Demo Video**
[YouTube Link](https://youtu.be/p9tVqmoBhfQ)

## **3. Architecture & Implementation**
### **3.1 System Architecture Overview**

The architecture consists of three main components:

1. **Database Setup** (SQLite)  
   - Allows users to upload a **CSV file** or **fetch a dataset from an online URL**.
   - Automatically **creates and populates** a SQLite database (`data.db`).

2. **LLM-Based SQL Query Generation** (Llama 3, Groq, LangChain)
   - Converts user input (natural language) into **valid SQL queries**.
   - Uses **LangChain** to integrate LLMs efficiently.

3. **Streamlit UI for Interaction**
   - Users can enter natural language queries in a **simple web UI**.
   - SQL is generated dynamically and executed on the SQLite database.
   - Results are displayed in **tabular format**.

### **3.2 Detailed Flow of Implementation**
#### **Step 1: Database Setup**
- Users **upload a CSV** or **provide a dataset URL**.
- The **CSV is parsed** and stored in a **SQLite database (`data.db`)**.
- The **database schema is created dynamically** based on the CSV structure.

#### **Step 2: Text-to-SQL Query Conversion**
- The **user inputs a question in English** (e.g., "How many students are there?").
- The **LLM (Llama 3 via Groq API) processes the query** and generates the corresponding SQL.
- **Prompt Engineering** refines the LLM response to improve SQL query accuracy.

#### **Step 3: SQL Execution & Result Display**
- The **generated SQL query** is executed on the **SQLite database**.
- Results are fetched and **displayed in a table format** in the Streamlit UI.
- If needed, users can rephrase their query for more refined results.

## **4. Tools & Technologies Used**

| Technology | Purpose |
|------------|---------|
| **SQLite** | Lightweight database for handling structured data from CSVs |
| **Streamlit** | Provides an interactive UI for users to enter queries and view results |
| **Llama 3 (via Groq API)** | Converts natural language queries to SQL |
| **LangChain** | Integrates LLM and optimizes query generation |
| **Python** | Main programming language used |
| **Pandas** | Parses CSV files and structures data for database storage |
| **Dotenv** | Handles environment variables securely (e.g., API keys) |

## **5. Prompt Engineering & Refinements**
### **Challenges in Query Generation**
1. **Case Sensitivity Issues**: SQL queries failed when column names didn’t match exactly.
2. **Data Format Mismatch**: Queries failed when column values differed from expected ones (e.g., "Male" vs. "M").
3. **Ambiguous Queries**: Some user inputs were too vague for the LLM to generate precise SQL.

### **Improvements & Solutions**
- **Dynamic Schema Extraction**: Before generating SQL, the system extracts table schema dynamically using:
  ```sql
  PRAGMA table_info(DATA);
  ```
- **Value Inspection for Query Refinement**:
  - Before processing a query, the system checks distinct values in categorical columns using:
  ```sql
  SELECT DISTINCT column_name FROM DATA;
  ```
  - This ensures the generated SQL uses the **correct value format** (e.g., `gender = 'M'` instead of `gender = 'Male'`).
- **Better Prompt Engineering**:
  - The **LLM prompt** was refined to include the **table schema and unique column values**, improving SQL accuracy.
  - Example prompt:
  ```
  You are an expert in SQL. The table 'DATA' has columns: gender, age, Pclass, etc.
  Important Notes:
  - Column 'gender' has values ['M', 'F']
  - Column 'Embarked' has values ['C', 'S', 'Q']
  Convert the following question to SQL: "How many male passengers survived?"
  ```

## **6. Overall Project Flow**
1. **User Uploads Data**: CSV file or dataset URL is provided.
2. **Database Creation**: SQLite stores structured data dynamically.
3. **User Enters Query in Natural Language**.
4. **LLM Converts Text to SQL**.
5. **SQL is Executed on Database**.
6. **Results are Displayed in Table Format**.

## **7. Key Features & Enhancements**
✅ **Supports Any Dataset** – No need to predefine table structure.
✅ **Dynamically Extracts Schema & Values** – Ensures query accuracy.
✅ **User-Friendly UI** – No SQL knowledge required.
✅ **Scalable & Extendable** – Can be adapted for different databases (PostgreSQL, MySQL).

## **8. Future Improvements**
- **Support for Multiple Tables**: Allow users to join multiple datasets dynamically.
- **Enhanced Query Debugging**: Provide explanations for failed queries and suggest corrections.
- **Performance Optimization**: Implement query caching for repeated requests.

## **9. Conclusion**
This project successfully **bridges the gap between non-technical users and databases**, making SQL querying **accessible, efficient, and user-friendly**. By leveraging **LLM-powered Text-to-SQL conversion**, users can retrieve data insights instantly, without writing a single line of SQL.

---
🚀 **Text-to-SQL Dynamic Assistant – Talk to Your Data, No SQL Required!** 🚀

