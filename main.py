from fastapi import FastAPI, Path, HTTPException, Query
import json

file_path = "patients.json"

def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is the about page."}

@app.get("/view")
def view():
    data = load_data(file_path)
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view", example="P001")):
    data = load_data(file_path)
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort the patients by this field", example="age"), order: str = Query("asc", description="Order of sorting", example="asc")):
    data = load_data(file_path)
    valid_fields = ["height", "weight", "age","bmi"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field please selcet from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order, please select from asc or desc")
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda item: item.get(sort_by,0), reverse=sort_order)
    return sorted_data