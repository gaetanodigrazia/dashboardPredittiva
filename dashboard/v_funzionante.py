
import streamlit as st
import requests
from datetime import datetime

st.title("🏠 Dashboard Predittiva - Feature Derivate Calcolate")

def input_form():
    data = {}
    data['Id'] = st.number_input("ID", min_value=1, value=1001)

    st.subheader("📏 Superfici componenti")
    data['1stFlrSF'] = st.slider("1st Floor SF", 0, 3000, 1000)
    data['2ndFlrSF'] = st.slider("2nd Floor SF", 0, 2000, 400)
    data['BsmtFinSF1'] = st.slider("Bsmt Fin SF1", 0, 1500, 500)
    data['BsmtFinSF2'] = st.slider("Bsmt Fin SF2", 0, 1500, 100)
    data['BsmtUnfSF'] = st.slider("Bsmt Unfinished SF", 0, 1500, 200)

    # Calcoli automatici
    data['TotalBsmtSF'] = data['BsmtFinSF1'] + data['BsmtFinSF2'] + data['BsmtUnfSF']
    data['GrLivArea'] = data['1stFlrSF'] + data['2ndFlrSF']
    data['TotalSF'] = data['GrLivArea'] + data['TotalBsmtSF']

    st.metric("Total Basement SF", f"{data['TotalBsmtSF']} m²")
    st.metric("GrLivArea (Living)", f"{data['GrLivArea']} m²")
    st.metric("TotalSF", f"{data['TotalSF']} m²")

    st.subheader("🛁 Componenti bagno")
    data['BsmtFullBath'] = st.selectbox("Basement Full Baths", [0, 1, 2], index=0)
    data['FullBath'] = st.selectbox("Full Baths", [0, 1, 2, 3], index=1)
    data['HalfBath'] = st.selectbox("Half Baths", [0, 1, 2], index=0)

    data['TotalBathrooms'] = data['FullBath'] + data['HalfBath'] * 0.5 + data['BsmtFullBath']
    st.metric("Total Bathrooms", f"{data['TotalBathrooms']}")

    st.subheader("📦 Altri dati")
    data['GarageArea'] = st.slider("Garage Area", 0, 1500, 500)
    data['GarageCars'] = st.slider("Numero posti garage", 0, 5, 2)
    data['Fireplaces'] = st.slider("Numero caminetti", 0, 3, 1)
    data['PoolArea'] = st.slider("Superficie piscina (se presente)", 0, 1000, 0)
    data['LotArea'] = st.slider("Lot Area", 1000, 100000, 8450)

    data['OverallQual'] = st.selectbox("Overall Quality", list(range(1, 11)), index=5)
    data['YearBuilt'] = st.slider("Year Built", 1870, datetime.now().year, 2000)
    data['YearRemodAdd'] = st.slider("Year Remodeled", 1950, datetime.now().year, 2005)
    data['YrSold'] = st.slider("Year Sold", 2006, 2010, 2008)
    data['MoSold'] = st.slider("Month Sold", 1, 12, 6)

    # Interazione e booleani calcolati
    data['Overall_GrLiv_Garage_Interaction'] = data['GrLivArea'] * data['GarageArea']
    data['hasbsmt'] = data['TotalBsmtSF'] > 0
    data['hasfireplace'] = data['Fireplaces'] > 0
    data['hasgarage'] = data['GarageArea'] > 0
    data['has2ndfloor'] = data['2ndFlrSF'] > 0
    data['haspool'] = data['PoolArea'] > 0
    data['Multifloor'] = data['2ndFlrSF'] > 0
    data['IsNew'] = data['YearBuilt'] == data['YrSold']

    st.markdown(f"📌 `IsNew`: {data['IsNew']}, `Multifloor`: {data['Multifloor']}, `haspool`: {data['haspool']}, `hasgarage`: {data['hasgarage']}`")

    return data

input_data = input_form()

if st.button("📤 Calcola prezzo"):
    st.write("📦 Dati inviati al backend:")
    st.json(input_data)

    response = requests.post("http://model-api:8000/predict", json=input_data)

    if response.status_code == 200:
        price = response.json()["predicted_price"]
        st.success(f"💰 Prezzo stimato: {price:,.2f} €")
    else:
        st.error("❌ Errore nella comunicazione con il backend.")
