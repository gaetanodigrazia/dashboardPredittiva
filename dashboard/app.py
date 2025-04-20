
import streamlit as st
import requests

st.title("Dashboard Predittiva Completa - Vincoli Dinamici Estesi")

def input_form():
    data = {}
    data['Id'] = st.number_input("ID", min_value=1, value=1001)

    st.subheader("📏 Dimensioni")
    data['LotFrontage'] = st.slider("Lot Frontage", 0, 200, 60)
    data['LotArea'] = st.slider("Lot Area", 1000, 100000, 8450)
    data['1stFlrSF'] = st.slider("1st Floor SF", 0, 3000, 1000)
    data['2ndFlrSF'] = st.slider("2nd Floor SF", 0, 2000, 400)
    data['TotalBsmtSF'] = st.slider("Total Basement SF", 0, 3000, 800)
    data['GrLivArea'] = data['1stFlrSF'] + data['2ndFlrSF']
    st.markdown(f"📐 GrLivArea calcolata: `{data['GrLivArea']} m²`")

    data['GarageCars'] = st.slider("Numero posti garage", 0, 5, 2)
    garage_area_min = data['GarageCars'] * 12
    data['GarageArea'] = st.slider("Garage Area", min_value=garage_area_min, max_value=1500, value=max(garage_area_min, 500))
    st.markdown(f"ℹ️ Minimo GarageArea: {garage_area_min} m²")

    data['WoodDeckSF'] = st.slider("Wood Deck SF", 0, 1000, 200)
    data['OpenPorchSF'] = st.slider("Open Porch SF", 0, 1000, 100)
    data['3SsnPorch'] = st.slider("3 Season Porch", 0, 500, 0)
    data['ScreenPorch'] = st.slider("Screen Porch", 0, 500, 0)
    data['PoolArea'] = st.slider("Pool Area", 0, 1000, 0)

    st.subheader("🛠️ Qualità e impianti")
    data['OverallQual'] = st.selectbox("Overall Quality", list(range(1, 11)), index=5)
    data['YearBuilt'] = st.slider("Year Built", 1870, 2023, 2000)
    data['YearRemodAdd'] = st.slider("Year Remodeled", 1950, 2023, 2005)
    data['GarageYrBlt'] = st.slider("Garage Year Built", 1900, 2023, 2000)
    data['MasVnrArea'] = st.slider("Masonry Veneer Area", 0, 1000, 100)
    data['BsmtFinSF1'] = st.slider("Basement Fin SF 1", 0, 2000, 500)
    data['BsmtFinSF2'] = st.slider("Basement Fin SF 2", 0, 2000, 200)
    data['BsmtUnfSF'] = st.slider("Unfinished Basement SF", 0, 2000, 300)

    st.subheader("🛁 Bagni e stanze")
    data['BsmtFullBath'] = st.selectbox("Basement Full Baths", [0, 1, 2], index=0)
    data['FullBath'] = st.selectbox("Full Baths", [0, 1, 2, 3], index=1)
    data['HalfBath'] = st.selectbox("Half Baths", [0, 1, 2], index=0)

    total_bath_calc = data['FullBath'] + 0.5 * data['HalfBath'] + data['BsmtFullBath']
    data['TotalBathrooms'] = st.slider("Total Bathrooms", min_value=total_bath_calc, max_value=6.0, value=total_bath_calc, step=0.5)
    st.markdown(f"ℹ️ Minimo TotalBathrooms: {total_bath_calc}")

    data['BedroomAbvGr'] = st.slider("Bedrooms Above Ground", 0, 10, 3)
    data['TotRmsAbvGrd'] = st.slider("Total Rooms Above Ground", 1, 15, 6)

    st.subheader("🔥 Extra")
    data['Fireplaces'] = st.slider("Number of Fireplaces", 0, 5, 1)
    data['MoSold'] = st.slider("Month Sold", 1, 12, 6)
    data['YrSold'] = st.slider("Year Sold", 2006, 2010, 2008)

    st.subheader("✅ Feature Engineering")
    data['Multifloor'] = st.checkbox("Multifloor", value=True)
    data['IsNew'] = st.checkbox("Is New", value=False)
    data['haspool'] = st.checkbox("Has Pool", value=False)
    data['has2ndfloor'] = st.checkbox("Has Second Floor", value=True)
    data['hasgarage'] = st.checkbox("Has Garage", value=True)
    data['hasbsmt'] = st.checkbox("Has Basement", value=True)
    data['hasfireplace'] = st.checkbox("Has Fireplace", value=True)

    total_sf_min = data['GrLivArea'] + data['TotalBsmtSF']
    data['TotalSF'] = st.slider("Total SF", min_value=total_sf_min, max_value=6000, value=total_sf_min)
    st.markdown(f"ℹ️ Minimo TotalSF: {total_sf_min}")

    overall_interaction_min = data['GrLivArea'] * data['GarageArea']
    data['Overall_GrLiv_Garage_Interaction'] = st.slider(
        "GrLiv x Garage Interaction", 
        min_value=overall_interaction_min, 
        max_value=10000, 
        value=overall_interaction_min
    )
    st.markdown(f"ℹ️ Minimo Interazione: {overall_interaction_min}")

    st.subheader("🏷️ Categorie codificate")
    data['Feature1'] = st.selectbox("Feature 1", list(range(0, 10)), index=1)
    data['Feature2'] = st.selectbox("Feature 2", list(range(0, 10)), index=2)
    data['LotShape'] = st.selectbox("Lot Shape", list(range(0, 4)), index=0)
    data['LandContour'] = st.selectbox("Land Contour", list(range(0, 4)), index=0)
    data['LotConfig'] = st.selectbox("Lot Config", list(range(0, 5)), index=0)
    data['LandSlope'] = st.selectbox("Land Slope", list(range(0, 3)), index=0)
    data['RoofStyle'] = st.selectbox("Roof Style", list(range(0, 6)), index=0)
    data['RoofMatl'] = st.selectbox("Roof Material", list(range(0, 8)), index=0)
    data['BsmtExposure'] = st.selectbox("Bsmt Exposure", list(range(0, 4)), index=0)
    data['FireplaceQu'] = st.selectbox("Fireplace Quality", list(range(0, 5)), index=0)
    data['GarageFinish'] = st.selectbox("Garage Finish", list(range(0, 3)), index=0)
    data['GarageQual'] = st.selectbox("Garage Quality", list(range(0, 5)), index=0)
    data['GarageCond'] = st.selectbox("Garage Condition", list(range(0, 5)), index=0)
    data['PoolQC'] = st.selectbox("Pool QC", list(range(0, 4)), index=0)
    data['Fence'] = st.selectbox("Fence", list(range(0, 5)), index=0)
    data['MiscFeature'] = st.selectbox("Misc Feature", list(range(0, 5)), index=0)
    data['Alley'] = st.selectbox("Alley", list(range(0, 3)), index=0)
    data['SaleType'] = st.selectbox("Sale Type", list(range(0, 10)), index=0)
    data['SaleCondition'] = st.selectbox("Sale Condition", list(range(0, 6)), index=0)

    return data

input_data = input_form()

if st.button("📤 Calcola prezzo"):
    st.write("📦 Dati inviati al backend:")
    st.json(input_data)
    response = requests.post("http://model-api:8000/predict", json=input_data)

    if response.status_code == 200:
        price = response.json()["predicted_price"]
        st.success(f"💰 Prezzo stimato: {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €")
    else:
        st.error("❌ Errore nella comunicazione con il backend.")
