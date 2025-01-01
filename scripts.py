import mysql.connector
import pandas as pd
from fpdf import FPDF
import os

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',          # Replace with your MySQL username
    'password': 'root',      # Replace with your MySQL password
    'database': 'student_management_kongu_college'
}

# Output Directory
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)  # Ensure output folder exists

def fetch_data(query, cursor):
    """Fetch data from the database and return as a DataFrame."""
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)

def save_to_csv(dataframe, filename):
    """Save a DataFrame to a CSV file."""
    filepath = os.path.join(output_dir, filename)
    dataframe.to_csv(filepath, index=False)
    print(f"CSV file saved as {filepath}")

def save_to_excel(dataframe, filename):
    """Save a DataFrame to an Excel file."""
    filepath = os.path.join(output_dir, filename)
    dataframe.to_excel(filepath, index=False)
    print(f"Excel file saved as {filepath}")

def save_to_pdf(dataframe, filename, title):
    """Generate a PDF file from a DataFrame."""
    filepath = os.path.join(output_dir, filename)
    pdf = FPDF()
    pdf.set_font("Arial", size=10)
    pdf.add_page()

    # Add Title
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt=title, ln=True, align='C')

    # Add Headers
    pdf.set_font("Arial", size=10)
    columns = dataframe.columns
    col_width = 190 / len(columns)
    for col in columns:
        pdf.cell(col_width, 10, col, border=1, align='C')
    pdf.ln()

    # Add Data Rows
    for index, row in dataframe.iterrows():
        for item in row:
            pdf.cell(col_width, 10, str(item), border=1, align='C')
        pdf.ln()

    # Save PDF
    pdf.output(filepath)
    print(f"PDF file saved as {filepath}")

try:
    # Initialize variables
    conn = None
    cursor = None

    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Queries for each table
    queries = {
        "student": "SELECT * FROM student",  # Correct table name
        "departments": "SELECT * FROM departments",  # Correct table name
        "staff": "SELECT * FROM staff"
    }

    for table, query in queries.items():
        print(f"Fetching data for {table} table...")
        # Fetch data
        df = fetch_data(query, cursor)

        # Save CSV, Excel, and PDF
        save_to_csv(df, f"{table}.csv")
        save_to_excel(df, f"{table}.xlsx")
        save_to_pdf(df, f"{table}.pdf", f"{table.capitalize()} Data")

except mysql.connector.Error as err:
    print(f"Database Error: {err}")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Safely close cursor and connection
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
