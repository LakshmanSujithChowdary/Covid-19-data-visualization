import requests
import json, io,csv
# Replace this with the actual endpoint URL
states = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=248d61ceead344438f0db8ad00aeecba"
countries = "https://api.covidactnow.org/v2/countries.timeseries.csv?apiKey=248d61ceead344438f0db8ad00aeecba"
metroes = "https://api.covidactnow.org/v2/cbsas.timeseries.csv?apiKey=248d61ceead344438f0db8ad00aeecba"


# Send a GET request to the endpoint
states_response = requests.get(states)
countries_response = requests.get(countries)
metroes_response = requests.get(metroes)

print(states_response)
print(countries_response)
print(metroes_response)



# Check if the request was successful (status code 200)
if states_response.status_code == 200 and countries_response.status_code == 200 and metroes_response.status_code == 200:
    csv_data = io.StringIO(states_response.text)
    reader = csv.reader(csv_data)
    first_line = next(reader)
    for i in first_line:
        print(i)
    
else:
    # Print an error message if the request failed
    print(f"Failed to retrieve data. Status code: {states_response.status_code}")



# # Plot 6: Infection Rate vs Case Density (Scatter plot)
    # plt.figure(figsize=(10, 6))
    # sns.scatterplot(data=data, x='metrics.caseDensity', y='metrics.infectionRate', hue='state', palette='coolwarm')
    # plt.title('Infection Rate vs Case Density by State')
    # plots['infection_rate'] = create_plot()

    # # Plot 7: Vaccinations Completed by State (Bar chart)
    # plt.figure(figsize=(10, 6))
    # state_vaccinations = data.groupby('state')['actuals.vaccinationsCompleted'].sum().sort_values(ascending=False).head(10)
    # state_vaccinations.plot(kind='bar', color='green')
    # plt.title('Total Vaccinations Completed by State')
    # plt.xlabel('State')
    # plt.ylabel('Vaccinations Completed')
    # plots['vaccinations_by_state'] = create_plot()

    # # Plot 8: COVID Vaccine Distribution (Box plot)
    # plt.figure(figsize=(10, 6))
    # sns.boxplot(data=data, y='actuals.vaccinesDistributed', color='cyan')
    # plt.title('COVID-19 Vaccine Distribution')
    # plots['vaccine_distribution'] = create_plot()

    # # Plot 9: Hospitalization Rates Over Time (Line plot)
    # plt.figure(figsize=(10, 6))
    # sns.lineplot(data=data, x='date', y='actuals.hospitalBeds.currentUsageCovid', color='orange')
    # plt.title('Hospitalization Rates Over Time')
    # plt.xticks(rotation=45)
    # plots['hospitalization_rate'] = create_plot()
