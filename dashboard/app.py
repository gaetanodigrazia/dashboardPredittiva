
import streamlit as st
import requests

st.title("Preventivo vendita case")

def sezione_dimensioni(data):
    st.subheader("📏 Dimensioni")
    data['1stFlrSF'] = st.slider("1st Floor SF", 0, 3000, 1000)
    data['has2ndfloor'] = st.checkbox("Has Second Floor", value=False)
    
    if data['has2ndfloor']:
        data['Multifloor'] = True
        data['2ndFlrSF'] = st.slider("2nd Floor SF", 1, 2000, 400)
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

def sezione_forma(data):
    st.subheader("🏗️ Caratteristiche del lotto")
    forma = st.selectbox("Forma del lotto",
        ["Regular", "Slightly irregular", "Moderately Irregular", "Irregular"])

    if forma == "Regular":
        data['LotShape'] = 0
        
    if forma == "Slightly irregular":
        data['LotShape'] = 1
        
    if forma == "Moderately Irregular":
        data['LotShape'] = 2

    if forma == "Irregular":
        data['LotShape'] = 3
    
    data['LotFrontage'] = st.slider("Lot Frontage", 0, 200, 60)

    data['LotArea'] = data['GrLivArea'] + data['WoodDeckSF'] + data['OpenPorchSF'] + data['3SsnPorch'] + data['ScreenPorch']
    st.markdown(f"📐 LotArea calcolata: `{data['LotArea']} m²`")
    data['LandContour'] = st.selectbox("Land Contour", list(range(0, 4)), index=0)
    data['LotConfig'] = st.selectbox("Lot Config", list(range(0, 5)), index=0)
    data['LandSlope'] = st.selectbox("Land Slope", list(range(0, 3)), index=0)
    data['Fence'] = st.selectbox("Fence", list(range(0, 5)), index=0)
    data['Alley'] = st.selectbox("Alley", list(range(0, 3)), index=0)
    alley = st.selectbox("Alley",
        ["Grvl", "Pave"])

    if alley == "Grvl":
        data['Alley'] = 0
        
    if alley == "Slightly irregular":
        data['Pave'] = 1
        
   
def sezione_stato_costruzione(data):
    st.subheader("🏗️ Tipo di costruzione")

    costruzione_tipo = st.selectbox(
        "Tipo di costruzione",
        ["Nuova costruzione", "Costruzione recente ristrutturata", "Costruzione vecchia"]
    )

    data["IsNewConstr"] = costruzione_tipo == "Nuova costruzione"

    if costruzione_tipo == "Nuova costruzione":
        data["YearBuilt"] = st.slider("Year Built", 2003, 2005, 2005)
        data["YearRemodAdd"] = data["YearBuilt"]
        data["IsNew"] = True
        data["OverallQual"] = 11

    if costruzione_tipo == "Costruzione recente ristrutturata":
        data["YearBuilt"] = st.slider("Year Built", 1870, 2005, 2000)
        data["YearRemodAdd"] = st.slider("Year Remodeled (≥ Year Built)", data["YearBuilt"], 2005, data["YearBuilt"])
        data["IsNew"] = True
        data["OverallQual"] = st.selectbox("Overall Quality", list(range(9, 11)), index=1)

    if costruzione_tipo == "Costruzione vecchia":
        data["YearBuilt"] = st.slider("Year Built", 1870, 2005, 1980)
        data["YearRemodAdd"] = st.slider("Year Remodeled (≥ Year Built)", data["YearBuilt"], 2005, data["YearBuilt"])
        data["IsNew"] = False
        data["OverallQual"] = st.selectbox("Overall Quality", list(range(1, 11)), index=3)

def sezione_seminterrato(data):
    st.subheader("🏗️ Seminterrato")
    data['hasbsmt'] = st.checkbox("Presenza di seminterrato", value=True)
    if data['hasbsmt']:
        data['BsmtFinSF1'] = st.slider("Bsmt Fin SF 1", 1, 2000, 500)
        data['BsmtFinSF2'] = st.slider("Bsmt Fin SF 2", 1, 2000, 200)
        data['BsmtUnfSF'] = st.slider("Bsmt Unfinished SF", 0, 2000, 300)
        data['BsmtHalfBath'] = st.selectbox("Bsmt Half Bath", [0, 1, 2], index=0)
        data['BsmtFullBath'] = st.selectbox("Bsmt Full Bath", [0, 1, 2], index=0)
        total_previous_bath = data['TotalBathrooms'] 
        data['TotalBathrooms'] = total_previous_bath + data['BsmtFullBath'] + (data['BsmtHalfBath'] *0.5)
        st.markdown(f"📊 TotalBathrooms calcolato automaticamente: `{data['TotalBathrooms']}`")
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

def sezione_bagno(data):
    st.subheader("🛁 Bagni e stanze della casa")
    data['FullBath'] = st.selectbox("Full Baths", [0, 1, 2, 3], index=1)
    data['HalfBath'] = st.selectbox("Half Baths", [0, 1, 2], index=0)
    total_bath_calc = data['FullBath'] + 0.5 * data['HalfBath']
    data['TotalBathrooms'] = total_bath_calc
    st.markdown(f"📊 TotalBathrooms calcolato automaticamente: `{data['TotalBathrooms']} m²`")
    data['BedroomAbvGr'] = st.slider("Bedrooms Above Ground", 0, 10, 3)
    
    # TotRmsAbvGrd deve essere ≥ BedroomAbvGr
    tot_rms_min = max(1, data['BedroomAbvGr'])
    data['TotRmsAbvGrd'] = st.slider("Total Rooms Above Ground", tot_rms_min, 15, max(tot_rms_min, 6))

def sezione_extra(data):
    st.subheader("🔥 Sell information")
    data['MoSold'] = st.slider("Month Sold", 1, 12, 6)
    data['YrSold'] = st.slider("Year Sold", 2006, 2010, 2008)
    data['SaleType'] = st.selectbox("Sale Type", list(range(0, 10)), index=0)
    data['SaleCondition'] = st.selectbox("Sale Condition", list(range(0, 6)), index=0)

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

def sezione_roof(data):
    roofStyle = st.selectbox("Roof Style",
        ["Gable", "Hip", "Gambrel", "Mansard", 
        "Flat", "Shed"])

    if roofStyle == "Gable":
        data['RoofStyle'] = 0
        
    if roofStyle == "Hip":
        data['RoofStyle'] = 1
    
    if roofStyle == "Gambrel":
        data['RoofStyle'] = 2
        
    if roofStyle == "Mansard":
        data['RoofStyle'] = 3
        
    if roofStyle == "Flat":
        data['RoofStyle'] = 4
        
    if roofStyle == "Shed":
        data['RoofStyle'] = 5
    
    roofMatl = st.selectbox("Roof Material",
        ["CompShg", "WdShngl", "Metal", "WdShake", 
        "Membran", "Tar&Grv", "Roll"])

    if roofMatl == "CompShg":
        data['RoofMatl'] = 0
        
    if roofMatl == "WdShngl":
        data['RoofMatl'] = 1
    
    if roofMatl == "Metal":
        data['RoofMatl'] = 2
        
    if roofMatl == "WdShake":
        data['RoofMatl'] = 3
        
    if roofMatl == "Membran":
        data['RoofMatl'] = 4
    
    if roofMatl == "Tar&Grv":
        data['RoofMatl'] = 5
        
    if roofMatl == "Roll":
        data['RoofMatl'] = 6

def input_form():
    data = {}
    data['Id'] = 1001

    with st.expander("📂 Mostra sezione Dimensioni"):
        sezione_dimensioni(data)
    
    with st.expander("📂 Mostra sezione Aree Esterne"):
        sezione_aree_esterne(data)
    
    with st.expander("📂 Mostra sezione Forma"):
        sezione_forma(data)
    
    with st.expander("📂 Mostra sezione Costruzione"):
        sezione_stato_costruzione(data)
    
    with st.expander("📂 Mostra sezione Bagno"):
        sezione_bagno(data)
    
    with st.expander("📂 Mostra sezione Seminterrato"):
        sezione_seminterrato(data)
    
    with st.expander("📂 Mostra sezione Extra"):
        sezione_extra(data)
    
    with st.expander("📂 Mostra sezione Garage"):
        sezione_garage(data)
    
    with st.expander("📂 Mostra sezione Caminetto"):
        sezione_caminetto(data)
    
    with st.expander("📂 Mostra sezione Piscina"):
        sezione_piscina(data)
    
    with st.expander("📂 Mostra sezione Tetto"):
        sezione_roof(data)

    #Derived calculated data
    total_sf_min = data['GrLivArea'] + data['TotalBsmtSF']
    data['Feature1'] = total_sf_min
    data['Feature2'] = data['TotalBsmtSF'] * data["YearRemodAdd"]
    data['Overall_GrLiv_Garage_Interaction'] = data['OverallQual'] * data['GarageArea'] * data['GrLivArea']
    data['TotalSF'] = data['TotalBsmtSF'] + data['GrLivArea'] + data['GarageArea']



    st.subheader("🏷️ Misc Feature")
    data['MasVnrArea'] = st.slider("Masonry Veneer Area", 0, 1000, 100)
    misc = st.selectbox("Misc Feature",
        ["Shed", "Gar2", "Othr", "TenC"])

    if misc == "Shed":
        data['MiscFeature'] = 0
        
    if misc == "Gar2":
        data['MiscFeature'] = 1
    
    if misc == "Othr":
        data['MiscFeature'] = 2
        
    if misc == "TenC":
        data['MiscFeature'] = 3


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



