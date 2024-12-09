from flask import Flask, render_template
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64

app = Flask(__name__)

# Load the CSV file
DATA_URL = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=248d61ceead344438f0db8ad00aeecba"
data = pd.read_csv(DATA_URL)

# Clean the data by handling missing values and ensuring proper types
data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Convert 'date' column to datetime
data['actuals.newCases'] = pd.to_numeric(data['actuals.newCases'], errors='coerce')  # Ensure numeric
data['actuals.deaths'] = pd.to_numeric(data['actuals.deaths'], errors='coerce')  # Ensure numeric

# Limit to the last 300 days for more efficient rendering
recent_data = data[data['date'] >= (data['date'].max() - pd.Timedelta(days=600))]
# recent_data = data

# Function to generate plot for new cases (Line plot)
def generate_plot_for_new_cases():
    if recent_data['actuals.newCases'].dropna().empty:
        return None
    else:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=recent_data, x='date', y='actuals.newCases', color='blue')
        plt.title('New COVID-19 Cases Over Time (Last 300 Days)')
        plt.xticks(rotation=45)
        return create_plot()

# Function to generate a heatmap of new cases by state over time
def generate_heatmap():
    pivot_table = recent_data.pivot_table(index='date', columns='state', values='actuals.newCases')

    # Handle missing data by filling NaN values with 0 and drop fully NaN rows/columns
    pivot_table = pivot_table.fillna(0).dropna(how='all', axis=1).dropna(how='all', axis=0)

    if pivot_table.empty:  # Check if there is still no data to plot
        return None
    else:
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, cmap="YlGnBu", cbar=True)
        plt.title('Heatmap of New COVID-19 Cases by State (Last 300 Days)')
        return create_plot()

# Function to generate bar plot of total deaths by state
def generate_plot_for_state_deaths():
    state_deaths = recent_data.groupby('state')['actuals.deaths'].sum().sort_values(ascending=False).head(10)
    if state_deaths.sum() == 0:
        return None
    else:
        state_deaths.plot(kind='bar', color='red')
        plt.title('Top 10 States by Total Deaths')
        plt.xticks(rotation=45)
        return create_plot()

# Function to generate a pie chart of top 10 states by new cases
def generate_pie_chart_for_new_cases():
    state_new_cases = recent_data.groupby('state')['actuals.newCases'].sum().sort_values(ascending=False).head(10)
    if state_new_cases.sum() == 0:
        return None
    else:
        plt.figure(figsize=(8, 8))
        plt.pie(state_new_cases, labels=state_new_cases.index, autopct='%1.1f%%', startangle=140)
        plt.title('Top 10 States by Percentage of New Cases')
        return create_plot()

# Function to generate histogram of new cases distribution
def generate_histogram_for_new_cases():
    plt.figure(figsize=(10, 6))
    sns.histplot(recent_data['actuals.newCases'].dropna(), bins=30, kde=True, color='green')
    plt.title('Distribution of New COVID-19 Cases')
    plt.xlabel('New Cases')
    return create_plot()

# Function to generate boxplot of new cases per week
def generate_boxplot_for_new_cases_per_week():
    recent_data['week'] = recent_data['date'].dt.to_period('W')
    weekly_data = recent_data.groupby('week')['actuals.newCases'].sum()
    if weekly_data.empty:
        return None
    else:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=weekly_data.index.astype(str), y=weekly_data, color='purple')
        plt.title('New Cases per Week (Boxplot)')
        plt.xticks(rotation=45)
        return create_plot()

# Helper function to convert plot to base64 image
def create_plot():
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Route to generate and display plots
@app.route('/generate_plots', methods=['GET'])
def generate_plots():
    plots = {}

    # Plot 1: New Cases Over Time (Line Plot)
    plots['new_cases'] = generate_plot_for_new_cases()
    if plots['new_cases'] is None:
        plots['new_cases'] = "No data available for new cases"

    # Plot 2: Heatmap of New Cases by State (Heatmap)
    plots['heatmap'] = generate_heatmap()
    if plots['heatmap'] is None:
        plots['heatmap'] = "No data available for heatmap"

    # Plot 3: State Deaths (Bar Plot)
    plots['state_deaths'] = generate_plot_for_state_deaths()
    if plots['state_deaths'] is None:
        plots['state_deaths'] = "No data available for state deaths"

    # Plot 4: State New Cases (Pie Chart)
    plots['state_new_cases'] = generate_pie_chart_for_new_cases()
    if plots['state_new_cases'] is None:
        plots['state_new_cases'] = "No data available for state new cases"

    # Plot 5: Distribution of New Cases (Histogram)
    plots['histogram'] = generate_histogram_for_new_cases()
    if plots['histogram'] is None:
        plots['histogram'] = "No data available for histogram of new cases"

    # Plot 6: New Cases per Week (Boxplot)
    plots['boxplot'] = generate_boxplot_for_new_cases_per_week()
    if plots['boxplot'] is None:
        plots['boxplot'] = "No data available for boxplot of new cases"

    return render_template('index.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True)
