import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Database connection details
db_config = {
    'user': 'root',
    'password': '',  # Replace with your actual password
    'host': '127.0.0.1',
    'database': 'glidex'
}

# Create a connection string
connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

try:
    # Connect to the database
    connection = engine.connect()
    print("Successfully connected to the database 'glidex'")

    # Query to fetch skaters data
    skaters_query = "SELECT * FROM SkatingClass"

    # Fetch data using pandas
    skaters_data = pd.read_sql(skaters_query, connection)
    print("Data fetched successfully")

    # Example 1: Distribution of categories
   

    category_counts = skaters_data['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']

    fig = px.pie(category_counts, names='Category', values='Count',
                title='Distribution of Skater Categories',
                labels={'Category': 'Skater Category', 'Count': 'Number of Skaters'},
                color_discrete_sequence=px.colors.sequential.RdBu)

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True, legend_title_text='Categories')
    fig.show()


    # Example 2: Age distribution of skaters
    age_counts = skaters_data['Age'].value_counts().reset_index()
    age_counts.columns = ['Age', 'Count']

    fig = px.pie(age_counts, names='Age', values='Count',
                title='Age Distribution of Skaters',
                labels={'Age': 'Age of Skaters', 'Count': 'Number of Skaters'},
                color_discrete_sequence=px.colors.sequential.Plasma)

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True, legend_title_text='Age Groups')
    fig.show()

    # Example 3: Progress for a specific distance over time (200m example)
    skaters_data['Total_Progress_200m'] = skaters_data[['200m_Aug2023', '200m_Nov2023', '200m_Feb2024', '200m_May2024']].sum(axis=1)
    progress_200m_counts = skaters_data.groupby('Name')['Total_Progress_200m'].sum().reset_index()

    fig = px.pie(progress_200m_counts, names='Name', values='Total_Progress_200m',
             title='Total Progress of 200m Over Time by Skater',
             labels={'Name': 'Skater Name', 'Total_Progress_200m': 'Total Progress (200m)'},
             color_discrete_sequence=px.colors.sequential.Blues)

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True, legend_title_text='Skaters')
    fig.show()

    # Example 4: Category-wise different age in bar chart   
    fig = px.bar(skaters_data, x='Category', y='Age', color='Category',
             barmode='group', title='Category-wise Age Distribution',
             labels={'Category': 'Skater Category', 'Age': 'Age of Skaters'},
             color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_layout(showlegend=True, legend_title_text='Categories', xaxis_tickangle=-45)
    fig.show()
    

    # Example 5: Quarterly progress for the last two quarters
    skaters_data['Q3Progress'] = skaters_data[['200m_Nov2023', '2km_Nov2023', '4km_Nov2023']].sum(axis=1)
    skaters_data['Q4Progress'] = skaters_data[['200m_Feb2024', '2km_Feb2024', '4km_Feb2024']].sum(axis=1)

    progress_q3_counts = skaters_data.groupby('Name')['Q3Progress'].sum().reset_index()
    progress_q4_counts = skaters_data.groupby('Name')['Q4Progress'].sum().reset_index()

    fig_q3 = px.pie(progress_q3_counts, names='Name', values='Q3Progress',
                    title='Q3 Progress by Skater',
                    labels={'Name': 'Skater Name', 'Q3Progress': 'Q3 Progress'},
                    color_discrete_sequence=px.colors.sequential.Greens)

    fig_q3.update_traces(textposition='inside', textinfo='percent+label')
    fig_q3.update_layout(showlegend=True, legend_title_text='Skaters')
    fig_q3.show()

    fig_q4 = px.pie(progress_q4_counts, names='Name', values='Q4Progress',
                    title='Q4 Progress by Skater',
                    labels={'Name': 'Skater Name', 'Q4Progress': 'Q4 Progress'},
                    color_discrete_sequence=px.colors.sequential.Oranges)

    fig_q4.update_traces(textposition='inside', textinfo='percent+label')
    fig_q4.update_layout(showlegend=True, legend_title_text='Skaters')
    fig_q4.show()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    connection.close()
    print("MySQL connection is closed.")
