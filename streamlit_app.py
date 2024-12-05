import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Financial Forecasting")

# Titolo dell'applicazione
st.title("Financial Data")

# Sidebar per il caricamento del file CSV
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # Lettura dei dati dal file caricato
    data = pd.read_csv(uploaded_file)
    
    # Converti 'Year' in integer per rimuovere le virgole
    data['Year'] = data['Year'].astype(int)
    
    # Visualizzazione dei dati completi (fino al 2023)
    st.subheader("Complete Financial Data (2014-2023)")
    st.dataframe(data.style.format(subset=['Year'], formatter="{:.0f}"))
    
    # Grafico dell'andamento storico dei ricavi netti fino al 2023
    st.subheader("Revenue Trend Analysis (2014-2023)")
    fig, ax = plt.subplots()
    filtered_data = data[data['Year'] <= 2023]
    ax.plot(filtered_data['Year'], filtered_data['Net revenues'], marker='o', linestyle='-')
    ax.set_title("Historical Trend of Net Revenues (2014-2023)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Net Revenues (€)")
    st.pyplot(fig)
    
    # Richiesta dell'anno per il forecast
    st.subheader("Forecast Input")
    forecast_year = st.text_input("Enter the year for forecasting (e.g., 2024):")

    if forecast_year:
        try:
            forecast_year = int(forecast_year)
            if forecast_year == 2024:
                # Sezione Forecast con i dati previsti per il 2024
                st.header(f"Forecast for {forecast_year}")
                forecast_data = pd.DataFrame({
                    'Year': [2024], 
                    'Net revenues': [6328], 
                    'Cost of sales': [4860], 
                    'Selling general and administrative costs': [573], 
                    'Research and development costs': [512], 
                    'Depreciation and amortization': [343], 
                    'Cash flow from operating activities': [629], 
                    'Cash flow from investing activities': [-386], 
                    'Cash flow from financing activities': [292], 
                    'Work-in-progress inventories': [263], 
                    'Finished goods inventories': [262], 
                    'Raw materials inventories': [223], 
                    'Car sales (in unit)': [17075]
                })
                st.dataframe(forecast_data.style.format(subset=['Year'], formatter="{:.0f}"))

                # Visualizzazione delle immagini con larghezza di 900 px
                st.subheader("Graphical Visualizations")
                image_folder = 'images'  # Assicurati che il percorso alla cartella delle immagini sia corretto
                images = sorted([f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

                for image in images:
                    st.image(os.path.join(image_folder, image), width=900)
            else:
                st.warning(f"Forecast data is only available for 2024. You entered {forecast_year}.")
        except ValueError:
            st.error("Please enter a valid year (numeric format).")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: white; background-color: black; padding: 10px;">
        © 2024 Financial Forecasting
    </div>
    """, 
    unsafe_allow_html=True
)
