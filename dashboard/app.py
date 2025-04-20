
import streamlit as st
import requests

st.title("Dashboard Predittiva Completa - Ordinata")

def sezione_dimensioni(data):
    st.subheader("📏 Dimensioni")
    data['LotFrontage'] = st.slider("Lot Frontage", 0, 200, 60)
    data['LotArea'] = st.slider("Lot Area", 1000, 100000, 8450)
    data['1stFlrSF'] = st.slider("1st Floor SF", 0, 3000, 1000)
    data['has2ndfloor'] = st.checkbox("Has Second Floor", value=False)
    
    if data['has2ndfloor']:
        data['Multifloor'] = True
        data['2ndFlrSF'] = st.slider("2nd Floor SF", 0, 2000, 400)
    else:
        data['2ndFlrSF'] = 0
        data['Multifloor'] = False

    data['GrLivArea'] = data['1stFlrSF'] + data['2ndFlrSF']
    st.markdown(f"📐 GrLivArea calcolata: `{data['GrLivArea']} m²`")


def sezione_aree_esterne(data):
    st.subheader("📏 Aree esterne")
    data['WoodDeckSF'] = st.slider("Wood Deck SF", 0, 1000, 200)
    data['OpenPorchSF'] = st.slider("Open Porch SF", 0, 1000, 100)
    data['3SsnPorch'] = st.slider("3 Season Porch", 0, 500, 0)
    data['ScreenPorch'] = st.slider("Screen Porch", 0, 500, 0)


def sezione_stato_costruzione(data):
    st.subheader("🏗️ Tipo di costruzione")
    costruzione_tipo = st.selectbox("Tipo di costruzione", ["Nuova costruzione", "Costruzione recente ristrutturata", "Costruzione vecchia"])
    data["IsNewConstr"] = costruzione_tipo == "Nuova costruzione"

    if costruzione_tipo == "Nuova costruzione":
        data["YearBuilt"] = st.slider("Year Built", 2003, 2005, 2005)
        data["IsNew"] = True
        data["YearRemodAdd"] = data["YearBuilt"]
    else:
        year_built = st.slider("Year Built", 1870, 2005, 2000 if costruzione_tipo == "Costruzione recente ristrutturata" else 1980)
        year_remod_default = year_built
        data["YearBuilt"] = year_built
        data["YearRemodAdd"] = st.slider("Year Remodeled (≥ Year Built)", year_built, 2005, year_remod_default)
        data["IsNew"] = costruzione_tipo == "Costruzione recente ristrutturata"


def sezione_seminterrato(data):
    st.subheader("🏗️ Seminterrato")
    data['hasbsmt'] = st.checkbox("Presenza di seminterrato", value=True)
    if data['hasbsmt']:
        data['BsmtFinSF1'] = st.slider("Bsmt Fin SF 1", 1, 2000, 500)
        data['BsmtFinSF2'] = st.slider("Bsmt Fin SF 2", 1, 2000, 200)
        data['BsmtUnfSF'] = st.slider("Bsmt Unfinished SF", 0, 2000, 300)
        data['BsmtFullBath'] = st.selectbox("Bsmt Full Bath", [0, 1, 2], index=0)
        data['BsmtExposure'] = st.selectbox("Bsmt Exposure", list(range(0, 4)), index=0)
        data['TotalBsmtSF'] = data['BsmtFinSF1'] + data['BsmtFinSF2'] + data['BsmtUnfSF']
        st.markdown(f"📊 TotalBsmtSF calcolato automaticamente: `{data['TotalBsmtSF']} m²`")

    else:
        data['TotalBsmtSF'] = 0
        data['BsmtFinSF1'] = 0
        data['BsmtFinSF2'] = 0
        data['BsmtUnfSF'] = 0
        data['BsmtFullBath'] = 0
        data['BsmtExposure'] = 0


def sezione_qualita_impianti(data):
    st.subheader("🛠️ Qualità e impianti")
    data['OverallQual'] = st.selectbox("Overall Quality", list(range(1, 11)), index=5)
    data['MasVnrArea'] = st.slider("Masonry Veneer Area", 0, 1000, 100)


def sezione_bagno(data):
    st.subheader("🛁 Bagni e stanze")
    data['FullBath'] = st.selectbox("Full Baths", [0, 1, 2, 3], index=1)
    data['HalfBath'] = st.selectbox("Half Baths", [0, 1, 2], index=0)
    total_bath_calc = data['FullBath'] + 0.5 * data['HalfBath'] + data['BsmtFullBath']
    data['TotalBathrooms'] = st.slider("Total Bathrooms", min_value=total_bath_calc, max_value=6.0, value=total_bath_calc, step=0.5)
    st.markdown(f"ℹ️ Minimo TotalBathrooms: {total_bath_calc}")
    data['BedroomAbvGr'] = st.slider("Bedrooms Above Ground", 0, 10, 3)
    data['TotRmsAbvGrd'] = st.slider("Total Rooms Above Ground", 1, 15, 6)


def sezione_extra(data):
    st.subheader("🔥 Extra")
    data['MoSold'] = st.slider("Month Sold", 1, 12, 6)
    data['YrSold'] = st.slider("Year Sold", 2006, 2010, 2008)


def sezione_garage(data):
    st.subheader("🚗 Garage")
    data['hasgarage'] = st.checkbox("Has Garage", value=False)
    if data['hasgarage']:
        data['GarageCars'] = st.slider("Numero posti garage", 0, 5, 2)
        garage_area_min = data['GarageCars'] * 12
        data['GarageArea'] = st.slider("Garage Area", min_value=garage_area_min, max_value=1500, value=max(garage_area_min, garage_area_min))
        st.markdown(f"ℹ️ Minimo GarageArea: {garage_area_min} m²")
        data['GarageFinish'] = st.selectbox("Garage Finish", list(range(1, 3)), index=0)
        data['GarageQual'] = st.selectbox("Garage Quality", list(range(1, 5)), index=0)
        data['GarageCond'] = st.selectbox("Garage Condition", list(range(1, 5)), index=0)
        data['GarageYrBlt'] = st.slider("Garage Year Built", 1900, 2023, 2000)
    else:
        data['GarageCars'] = 0
        data['GarageArea'] = 0
        data['GarageFinish'] = 0
        data['GarageQual'] = 0
        data['GarageCond'] = 0
        data['GarageYrBlt'] = 0

def sezione_piscina(data):
    st.subheader("🏊 Piscina")
    data['haspool'] = st.checkbox("Has Pool", value=False)
    if data['haspool']:
        data['PoolArea'] = st.slider("Pool Area", 1, 1000, 200)
        data['PoolQC'] = st.selectbox("Pool QC", list(range(1, 4)), index=0)
    else:
        data['PoolArea'] = 0
        data['PoolQC'] = 0

def sezione_caminetto(data):
    st.subheader("🔥 Caminetto")
    data['hasfireplace'] = st.checkbox("Has Fireplace", value=False)
    if data['hasfireplace']:
        data['Fireplaces'] = st.slider("Number of Fireplaces", 1, 5, 1)
        data['FireplaceQu'] = st.selectbox("Fireplace Quality", list(range(1, 5)), index=0)
    else:
        data['Fireplaces'] = 0
        data['FireplaceQu'] = 0


def input_form():
    data = {}
    data['Id'] = st.number_input("ID", min_value=1, value=1001)

    sezione_dimensioni(data)
    sezione_aree_esterne(data)
    sezione_stato_costruzione(data)
    sezione_seminterrato(data)
    sezione_qualita_impianti(data)
    sezione_bagno(data)
    sezione_extra(data)
    sezione_garage(data)
    sezione_caminetto(data)
    sezione_piscina(data)

    
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
    data['Fence'] = st.selectbox("Fence", list(range(0, 5)), index=0)
    data['MiscFeature'] = st.selectbox("Misc Feature", list(range(0, 5)), index=0)
    data['Alley'] = st.selectbox("Alley", list(range(0, 3)), index=0)
    data['SaleType'] = st.selectbox("Sale Type", list(range(0, 10)), index=0)
    data['SaleCondition'] = st.selectbox("Sale Condition", list(range(0, 6)), index=0)

    return data

input_data = input_form()

# Calcolo prezzo solo su click
if st.button("📤 Calcola prezzo"):
    response = requests.post("http://model-api:8000/predict", json=input_data)
    if response.status_code == 200:
        st.session_state["prezzo"] = response.json()["predicted_price"]
    else:
        st.session_state["prezzo"] = None
        st.error("❌ Errore nella comunicazione con il backend.")

# Mostra il prezzo stimato solo se disponibile
if "prezzo" in st.session_state and st.session_state["prezzo"] is not None:
    formatted_price = f"{st.session_state['prezzo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.success(f"💰 Prezzo stimato: {formatted_price} €")



