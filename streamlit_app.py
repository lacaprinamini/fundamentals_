import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Preparazione dei dati
data = {
    'Year': [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'Net revenues': [2489, 2578, 2824, 3224, 3123, 3500, 3207, 4059, 4832, 5650],
    'Cost of sales': [2224, 2245, 2332, 2560, 2559, 2832, 2740, 3279, 3819, 4379],
    'Selling general and administrative costs': [239, 267, 283, 316, 332, 371, 387, 451, 492, 531],
    'Research and development costs': [397, 402, 428, 442, 421, 448, 461, 467, 475, 488],
    'Depreciation and amortization': [169, 161, 139, 156, 169, 193, 224, 257, 284, 312],
    'Cash flow from operating activities': [490, 510, 523, 539, 545, 559, 547, 594, 603, 611],
    'Cash flow from investing activities': [-302, -312, -320, -329, -331, -337, -348, -357, -388, -379],
    'Cash flow from financing activities': [205, 214, 220, 231, 238, 245, 252, 272, 269, 281],
    'Work-in-progress inventories': [59, 67, 72, 88, 84, 91, 94, 121, 145, 229],
    'Finished goods inventories': [61, 80, 94, 101, 119, 130, 155, 157, 155, 234],
    'Raw materials inventories': [91, 75, 95, 99, 74, 85, 96, 99, 142, 203],
    'Car sales (in unit)': [7255, 7664, 8014, 8398, 9251, 10131, 9119, 12155, 14221, 15665]
}
df = pd.DataFrame(data)

# Modello RandomForest
def train_model(dataframe, target):
    X = dataframe.drop(columns=[target])
    y = dataframe[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

# Streamlit App
st.title('Tool di Previsione per il 2024')

# Sidebar for user input for inventory calculations
st.sidebar.header('Input Inventario')
max_capacity = st.sidebar.number_input('Capacità Massima di Inventario', value=1000)
num_products = st.sidebar.number_input('Numero di Prodotti', min_value=1, max_value=4, value=1)
product_details = {}
for i in range(int(num_products)):
    price = st.sidebar.number_input(f'Prezzo stimato prodotto {i+1}', value=100)
    product_details[f'Prodotto {i+1}'] = price

# Calculate inventory usage
total_cost = sum(product_details.values())
inventory_usage = (total_cost / max_capacity) * 100 if max_capacity else 0

# Display inventory calculation
if st.sidebar.button('Calcola Utilizzo Inventario'):
    st.write(f"Costo totale dei prodotti: €{total_cost}")
    st.write(f"Utilizzo capacità di inventario: {inventory_usage:.2f}%")

# Model predictions
if st.button('Mostra Previsioni Finanziarie'):
    st.subheader('Previsioni Finanziarie per il 2024')
    model_net_revenues = train_model(df, 'Net revenues')
    prediction_net_revenues = model_net_revenues.predict([[2024]])[0]
    st.write(f"Previsione Ricavi Net: €{prediction_net_revenues:.2f}")

# Potenzialmente, ripeti per altre previsioni
