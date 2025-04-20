from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("model/xgb_model.pkl")

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
def predict(data: InputData):
    input_dict = data.dict(by_alias=True)
    df = pd.DataFrame([input_dict])
    prediction = model.predict(df)[0]
    return {"predicted_price": float(round(np.exp(prediction), 2))}
