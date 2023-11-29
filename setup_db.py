import pandas as pd
import requests
import sqlite3

# Define the columns
columns = ['id_pdc_local', 'statut_pdc', 'arrondissement', 'id_station_local',
           'id_station_itinerance', 'nom_station', 'code_insee_commune',
           'implantation_station', 'nbre_pdc', 'date_maj', 'condition_acces',
           'adresse_station', 'gratuit', 'paiement_acte', 'paiement_cb',
           'paiement_autre', 'reservation', 'siren_amenageur',
           'contact_amenageur', 'nom_amenageur', 'nom_operateur',
           'contact_operateur', 'telephone_operateur', 'nom_enseigne',
           'tarification', 'id_pdc_itinerance', 'date_mise_en_service',
           'accessibilite_pmr', 'restriction_gabarit', 'station_deux_roues',
           'puissance_nominale', 'prise_type_ef', 'prise_type_2',
           'prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_autre',
           'prise_type_3', 'num_pdl', 'horaires', 'raccordement',
           'coordonneesxy.lon', 'coordonneesxy.lat']

# Create an empty DataFrame with the specified columns
empty_df = pd.DataFrame(columns=columns)

# API URL
api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/belib-points-de-recharge-pour-vehicules-electriques-donnees-statiques/records?limit=100"

# Make the API request
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract data from the API response
    api_data = response.json()

    # Extract the "results" section from the API response
    results = api_data.get('results', [])

    # Normalize the data and handle the 'observations' and 'coordonneesxy' fields
normalized_data = []
for result in results:
    result_flat = {key: result[key] for key in result if key not in ['observations', 'coordonneesxy']}
    result_flat['observations'] = ', '.join(result.get('observations', []))
    result_flat['coordonneesxy_lon'] = result.get('coordonneesxy', {}).get('lon', None)
    result_flat['coordonneesxy_lat'] = result.get('coordonneesxy', {}).get('lat', None)
    normalized_data.append(result_flat)

# Create a DataFrame from the normalized data
result_df = pd.DataFrame(normalized_data)
print(result_df.info())
# Display the resulting DataFrame
print(result_df)

# SQLite database connection
conn = sqlite3.connect('test.db')

# Write the DataFrame to SQLite
result_df.to_sql('test', conn, index=False, if_exists='replace')

# Close the database connection
conn.close()

print("Data written to SQLite database.")
