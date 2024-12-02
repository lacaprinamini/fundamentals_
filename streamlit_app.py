import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Streamlit page configuration
st.set_page_config(page_title="Inventory Management and Financial Forecasting", layout="wide")

# App title
st.title("Inventory Management with Financial Forecasts up to 2028")

# Sidebar for user input
st.sidebar.header("Enter Inventory Data")

# Input for maximum inventory capacity
max_inventory_capacity = st.sidebar.number_input("Maximum Inventory Capacity", min_value=1, value=1000)

# Input for number of products (from 1 to 4)
num_products = st.sidebar.selectbox("Number of Products", options=[1, 2, 3, 4], index=0)

# List to store product details
product_details = []

# Loop to input details for each product
for i in range(num_products):
    st.sidebar.subheader(f"Product {i+1} Details")
    product_name = st.sidebar.text_input(f"Product {i+1} Name", value=f"Product {i+1}", key=f"name_{i}")
    product_price = st.sidebar.number_input(f"Product {i+1} Price (€)", min_value=0.0, value=100.0, key=f"price_{i}")
    product_quantity = st.sidebar.number_input(f"Product {i+1} Quantity", min_value=0, value=10, key=f"quantity_{i}")
    product_details.append({
        'Name': product_name,
        'Price': product_price,
        'Quantity': product_quantity,
        'Total Value': product_price * product_quantity
    })

# Create DataFrame of products
df_products = pd.DataFrame(product_details)

# Calculate total inventory value
total_inventory_value = df_products['Total Value'].sum()

# Calculate inventory capacity usage percentage
inventory_usage_percentage = (total_inventory_value / max_inventory_capacity) * 100

# Display results
st.header("Inventory Results")

# Show product table
st.subheader("Product Details")
st.table(df_products.style.format({'Price': '€{:.2f}', 'Total Value': '€{:.2f}'}))

# Show total inventory value
st.write(f"**Total Inventory Value:** €{total_inventory_value:.2f}")

# Show inventory capacity usage
st.write(f"**Inventory Capacity Usage:** {inventory_usage_percentage:.2f}%")

# Graphical visualizations
st.header("Graphical Visualizations")

# Bar chart of total value per product
st.subheader("Total Value per Product")
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.bar(df_products['Name'], df_products['Total Value'], color='skyblue')
ax1.set_xlabel('Product')
ax1.set_ylabel('Total Value (€)')
ax1.set_title('Total Value per Product')
st.pyplot(fig1)

# Pie chart of total value percentage distribution per product
st.subheader("Percentage Distribution of Total Value per Product")
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.pie(df_products['Total Value'], labels=df_products['Name'], autopct='%1.1f%%', startangle=140)
ax2.axis('equal')
st.pyplot(fig2)

# Inventory capacity usage analysis
st.header("Inventory Capacity Analysis")
if inventory_usage_percentage > 100:
    st.warning("Warning: Inventory usage exceeds maximum capacity!")
else:
    st.success("Inventory is within maximum capacity limits.")

# Add Random Forest model for financial forecasts
st.header("Financial Forecasts up to 2028")

# Load historical dataset
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

df_historical = pd.DataFrame(data)

# Create Random Forest model to predict Net Revenues
features = ['Cost of sales', 'Selling general and administrative costs', 'Research and development costs',
            'Depreciation and amortization', 'Cash flow from operating activities', 'Cash flow from investing activities',
            'Cash flow from financing activities', 'Work-in-progress inventories', 'Finished goods inventories',
            'Raw materials inventories', 'Car sales (in unit)']

X = df_historical[features]
y = df_historical['Net revenues']

# Train the model
model_rf = RandomForestRegressor(random_state=42)
model_rf.fit(X, y)

# Forecast from 2024 to 2028
years = [2024, 2025, 2026, 2027, 2028]
predictions = []

last_known_data = df_historical.iloc[-1].copy()

for year in years:
    # Create new input based on last known data
    input_data = last_known_data.copy()
    
    # Update the year
    input_data['Year'] = year
    
    # Simulate inventory increase based on entered products
    # Calculate inventory increase based on total inventory value
    total_inventory_quantity = df_products['Quantity'].sum()
    
    # Update inventories based on total product quantity
    input_data['Finished goods inventories'] += total_inventory_quantity
    input_data['Work-in-progress inventories'] += total_inventory_quantity * 0.5  # Assume WIP increases by 50% of quantity
    input_data['Raw materials inventories'] += total_inventory_quantity * 0.3  # Assume raw materials increase by 30% of quantity
    
    # Other fields can be updated based on business logic
    # For example, we can assume an annual growth rate for 'Cost of sales' and other entries
    growth_rate = 0.05  # Assume a growth rate of 5%
    input_data['Cost of sales'] *= (1 + growth_rate)
    input_data['Selling general and administrative costs'] *= (1 + growth_rate)
    input_data['Research and development costs'] *= (1 + growth_rate)
    input_data['Depreciation and amortization'] *= (1 + growth_rate)
    input_data['Cash flow from operating activities'] *= (1 + growth_rate)
    input_data['Cash flow from investing activities'] *= (1 + growth_rate)
    input_data['Cash flow from financing activities'] *= (1 + growth_rate)
    input_data['Car sales (in unit)'] *= (1 + growth_rate)
    
    # Prepare data for prediction
    X_input = pd.DataFrame([input_data[features]])
    
    # Make the prediction
    net_revenue_prediction = model_rf.predict(X_input)[0]
    
    # Save the results
    prediction = input_data.copy()
    prediction['Net revenues'] = net_revenue_prediction
    predictions.append(prediction)
    
    # Update last_known_data for the next year
    last_known_data = prediction.copy()

# Create a DataFrame with predictions
df_predictions = pd.DataFrame(predictions)

# Combine historical data with predictions
df_combined = pd.concat([df_historical, df_predictions], ignore_index=True)

# Calculate KPIs
def calculate_kpis(df):
    df = df.copy()
    df['Revenue Growth Rate (%)'] = df['Net revenues'].pct_change() * 100
    df['Gross Profit Margin (%)'] = ((df['Net revenues'] - df['Cost of sales']) / df['Net revenues']) * 100
    df['Operating Profit Margin (%)'] = (
        (df['Net revenues'] - df['Cost of sales'] - df['Selling general and administrative costs']
         - df['Research and development costs'] - df['Depreciation and amortization']) / df['Net revenues']
    ) * 100
    df['R&D Rate (%)'] = (df['Research and development costs'] / df['Net revenues']) * 100
    return df

df_kpis = calculate_kpis(df_combined)

# Display KPI table
st.subheader("KPI Table with Forecasts up to 2028")
kpi_columns = [
    'Year',
    'Net revenues',
    'Revenue Growth Rate (%)',
    'Gross Profit Margin (%)',
    'Operating Profit Margin (%)',
    'R&D Rate (%)'
]
st.dataframe(df_kpis[kpi_columns].style.format({
    'Net revenues': '€{:.2f}',
    'Revenue Growth Rate (%)': '{:.2f}%',
    'Gross Profit Margin (%)': '{:.2f}%',
    'Operating Profit Margin (%)': '{:.2f}%',
    'R&D Rate (%)': '{:.2f}%'
}))

# Inventory trend over the years
st.subheader("Inventory Trend Over the Years")
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.plot(df_kpis['Year'], df_kpis['Finished goods inventories'], marker='o', label='Finished Goods Inventories')
ax3.plot(df_kpis['Year'], df_kpis['Work-in-progress inventories'], marker='o', label='Work-in-Progress Inventories')
ax3.plot(df_kpis['Year'], df_kpis['Raw materials inventories'], marker='o', label='Raw Materials Inventories')
ax3.set_xlabel('Year')
ax3.set_ylabel('Inventory')
ax3.set_title('Inventory Trend from 2014 to 2028')
ax3.legend()
st.pyplot(fig3)

# Analysis per product
st.header("Product Analysis")

for index, product in df_products.iterrows():
    st.subheader(f"Analysis for {product['Name']}")
    # Calculate some indicators
    # Example: Predicted sales value for the product in future years
    # Assume sales grow by 5% each year
    years = np.arange(2024, 2029)
    quantities = [product['Quantity'] * ((1 + 0.05) ** (year - 2023)) for year in years]
    revenues = [product['Price'] * q for q in quantities]
    df_product_sales = pd.DataFrame({
        'Year': years,
        'Predicted Quantity': quantities,
        'Predicted Revenue (€)': revenues
    })
    st.table(df_product_sales.style.format({'Predicted Revenue (€)': '€{:.2f}', 'Predicted Quantity': '{:.2f}'}))
    # Capacity check for the product
    if product['Total Value'] > max_inventory_capacity:
        st.warning(f"Product {product['Name']} exceeds the maximum inventory capacity!")
    else:
        st.success(f"Product {product['Name']} is within the inventory capacity limits.")

# Footer
st.markdown("---")
st.markdown("© 2023 Inventory Management and Financial Forecasting")
