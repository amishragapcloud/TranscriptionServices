import streamlit as st
import openai
import os
from dotenv import load_dotenv
import random
import pyodbc
import assemblyai as aai


load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_id = os.getenv("AZURE_DEPLOYMENT_ID")



st.set_page_config(
    page_title="GapcloudAI - Conversations with your Data",
    page_icon="🤖",
    layout="wide"
)

logo_url = "https://media.licdn.com/dms/image/C560BAQGeCieaiSruPg/company-logo_200_200/0/1630669521343/gapcloud_logo?e=2147483647&v=beta&t=jFkQ6l0vG434rsZTMywindOO_6FkdrH4FYhE0W6Xj0Q"
logo_html = f"""
<div style="position: absolute; top: 10px; right: 10px; z-index: 1000;">
    <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px;">
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)

st.markdown('<h1 class="title" style="color: Black; display: inline;">GapcloudAI</h1>'
            '<h3 style="color: Pink; display: inline;">Actions on your Data</h3>', 
            unsafe_allow_html=True)

st.markdown("      ")



def get_database_connection():
    server = 'in-sqlsrvr-stg.database.windows.net,1433'
    database = 'IN-SQLDB-AU-DevDataset-01012023-STG'
    username = 'admin123'
    password = 'Abhishek123@#'  # Replace with your actual password
    driver = '{ODBC Driver 18 for SQL Server}'
    connection_string = f"""
        Server={server};
        Database={database};
        User Id={username};
        Password={password};
        Encrypt=yes;
        TrustServerCertificate=yes;
        Connection Timeout=30;
    """
    try:
        conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:in-sqlsrvr-stg.database.windows.net,1433;Database=IN-SQLDB-AU-DevDataset-01012023-STG;Uid=admin123;Pwd=Abhishek123@#;Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;")
        return conn
    except Exception as e:
        print(f"Error connecting to SQL Server: {str(e)}")
        return None

conn = get_database_connection()
import streamlit as st
import pygal


# Function to generate and display the bar chart
def display_browser_usage_chart():
    # Create a bar chart object with custom style
    bar_chart = pygal.Bar(width=1200, height=500)  
    # Set chart title and labels
    bar_chart.title = 'Sentiment Captured of Callers (in %) by Week'
    bar_chart.x_labels = map(str, range(1, 11))

    # Add data to the bar chart
    bar_chart.add('Happy', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    bar_chart.add('Neutral',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    bar_chart.add('Confused',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    bar_chart.add('Angry',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

    # Render the chart to an SVG string
    chart_rendered = bar_chart.render()

    # Convert SVG to HTML to display in Streamlit
    st.components.v1.html(chart_rendered, width=1200, height=700)  # Adjust width and height here

# Main Streamlit app code
def main():


    # Call the function to display the bar chart
    display_browser_usage_chart()

# Run the main function
if __name__ == "__main__":
    main()


# Function to generate and display the pie chart
def display_browser_usage_pie_chart():
    # Create a pie chart object with half pie enabled
    pie_chart = pygal.Pie(half_pie=True, inner_radius=0.4)  # Adjust inner_radius as needed

    # Set chart title
    pie_chart.title = 'Recorded Empathy Score b/w Callers and Callee (in %)'

    # Add data to the pie chart
    pie_chart.add('Helpful', 19.5)
    pie_chart.add('Set Expectations', 36.6)
    pie_chart.add('Confidence', 36.3)
    pie_chart.add('Sloppy', 4.5)
    pie_chart.add('Empathetic', 2.3)

    # Render the chart to an SVG string
    chart_rendered = pie_chart.render()

    # Convert SVG to HTML to display in Streamlit
    st.components.v1.html(chart_rendered, width=600, height=600)  # Adjust width and height as needed

# Main Streamlit app code
def main():

    # Call the function to display the pie chart
    display_browser_usage_pie_chart()

# Run the main function
if __name__ == "__main__":
    main()


# Function to generate and display the gauge chart
def display_browser_performance_gauge_chart():
    # Create a gauge chart object with human-readable values
    gauge_chart = pygal.Gauge(human_readable=True)

    # Set chart title
    gauge_chart.title = 'Key KPIs (in %)'

    # Set chart range
    gauge_chart.range = [0, 100]

    # Add data to the gauge chart
    gauge_chart.add('CSAT', 80)
    gauge_chart.add('FCR', 70)
    gauge_chart.add('Listen To Talk Ratio', 40)
    

    # Render the chart to an SVG string
    chart_rendered = gauge_chart.render()

    # Convert SVG to HTML to display in Streamlit
    st.components.v1.html(chart_rendered, width=600, height=400)  # Adjust width and height as needed

# Main Streamlit app code
def main():
       # Call the function to display the gauge chart
    display_browser_performance_gauge_chart()

# Run the main function
if __name__ == "__main__":
    main()


# Function to generate and display the stacked line chart
def display_browser_usage_line_chart():
    # Create a stacked line chart object with fill enabled
    line_chart = pygal.StackedLine(fill=True)

    # Set chart title and labels
    line_chart.title = 'Customer Churn Signals (in %) By Week'
    line_chart.x_labels = map(str, range(1, 11))

    # Add data to the stacked line chart
    line_chart.add('Cancel', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Upgrade',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('Downgrade',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Leave',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

    # Render the chart to an SVG string
    chart_rendered = line_chart.render()

    # Convert SVG to HTML to display in Streamlit
    st.components.v1.html(chart_rendered, width=800, height=700)  # Adjust width and height as needed

# Main Streamlit app code
def main():
    # Call the function to display the stacked line chart
    display_browser_usage_line_chart()

# Run the main function
if __name__ == "__main__":
    main()
