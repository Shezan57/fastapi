from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle

# Initialize FastAPI app
app = FastAPI()

# Define the Pydantic model for input validation
class UserInput(BaseModel):
    bmi: float
    age_group: str
    lifestyle_risk: str
    city_tier: int
    income_lpa: float
    occupation: str

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# @app.get("/")
# def read_root():
#     return {"message": "API is running"}

@app.post("/predict")
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]
    return {"predicted_category": prediction}