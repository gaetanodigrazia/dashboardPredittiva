from fastapi import FastAPI, Request, HTTPException, Depends
from jose import jwt, JWTError
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import numpy as np
import requests
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import base64
from confluent_kafka import Producer
import json

app = FastAPI()
model = joblib.load("model/xgb_model.pkl")


KEYCLOAK_URL = "http://keycloak:8080/realms/immobiliare"
ALGORITHMS = ["RS256"]
jwks_keys = None

producer = Producer({'bootstrap.servers': 'kafka:9092'})
def fetch_jwks_keys():
    global jwks_keys
    if jwks_keys is None:
        try:
            openid_config = requests.get(f"{KEYCLOAK_URL}/.well-known/openid-configuration").json()
            jwks_uri = openid_config["jwks_uri"]
            jwks_keys = requests.get(jwks_uri).json()["keys"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Errore caricamento JWKS: {e}")
    return jwks_keys

def get_public_key(token: str):
    headers = jwt.get_unverified_header(token)
    keys = fetch_jwks_keys()
    for key in keys:
        if key["kid"] == headers["kid"]:
            e = int.from_bytes(base64.urlsafe_b64decode(key['e'] + '=='), byteorder='big')
            n = int.from_bytes(base64.urlsafe_b64decode(key['n'] + '=='), byteorder='big')

            public_numbers = rsa.RSAPublicNumbers(e, n)
            public_key = public_numbers.public_key(default_backend())
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            return pem
    raise HTTPException(status_code=401, detail="Chiave pubblica non trovata.")

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token mancante o non valido.")

    token = auth_header.split(" ")[1]

    try:
        public_key_pem = get_public_key(token)
        payload = jwt.decode(token, public_key_pem, algorithms=ALGORITHMS, audience="account")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido o scaduto.")

class InputData(BaseModel):
    Id: int
    LotFrontage: float
    LotArea: float
    OverallQual: int
    YearBuilt: int
    YearRemodAdd: int
    MasVnrArea: float
    BsmtFinSF1: float
    BsmtFinSF2: float
    BsmtUnfSF: float
    TotalBsmtSF: float
    first_flr_sf: float = Field(..., alias="1stFlrSF")
    second_flr_sf: float = Field(..., alias="2ndFlrSF")
    GrLivArea: float
    BsmtFullBath: int
    FullBath: int
    HalfBath: int
    BedroomAbvGr: int
    TotRmsAbvGrd: int
    Fireplaces: int
    GarageYrBlt: int
    GarageCars: int
    GarageArea: float
    WoodDeckSF: float
    OpenPorchSF: float
    porch_3ssn: float = Field(..., alias="3SsnPorch")
    ScreenPorch: float
    PoolArea: float
    MoSold: int
    YrSold: int
    Multifloor: bool
    IsNew: bool
    TotalSF: float
    TotalBathrooms: float
    Feature1: int
    Feature2: int
    Overall_GrLiv_Garage_Interaction: float
    Alley: int
    LotShape: int
    LandContour: int
    LotConfig: int
    LandSlope: int
    RoofStyle: int
    RoofMatl: int
    BsmtExposure: int
    FireplaceQu: int
    GarageFinish: int
    GarageQual: int
    GarageCond: int
    PoolQC: int
    Fence: int
    MiscFeature: int
    SaleType: int
    SaleCondition: int
    haspool: bool
    has2ndfloor: bool
    hasgarage: bool
    hasbsmt: bool
    hasfireplace: bool

@app.post("/predict")
def predict(data: InputData, payload: dict = Depends(verify_token)):
    input_dict = data.dict(by_alias=True)
    df = pd.DataFrame([input_dict])
    prediction = model.predict(df)[0]

    messaggio = input_dict
    messaggio["predicted_price"] = float(round(np.exp(prediction), 2))

    # Prendi l'utente dal token
    user_key = payload.get("preferred_username", "unknown_user")

    try:
        # Manda il messaggio su Kafka
        producer.produce(
            topic="prezzi-predetti",
            key=user_key.encode('utf-8'),
            value=json.dumps(messaggio).encode('utf-8')
        )
        producer.flush()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore invio Kafka: {e}")

    return {"predicted_price": float(round(np.exp(prediction), 2))}

@app.get("/")
async def root():
    return {"message": "API attiva"}
