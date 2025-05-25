from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,List, Literal, Optional
class Patient(BaseModel):
    id: Annotated[str,  Field(...,description="The ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city of the patient", example="New York")]
    age: Annotated[int, Field(..., description="The age of the patient", example=30, gt=0, lt=120)]
    gender: Annotated[Literal["Male", "Female", "Others"], Field(..., description="Gender of the patient",example="Male")]
    height: Annotated[float, Field(..., description="Height of the patient in meter", example=1.80, gt=0)]
    weight: Annotated[float, Field(..., description="Weight of the patient in kg", example=70.5, gt=0)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi <30:
            return "Overweight"
        else:
            return "Obese"

# Update patient pydantic model
class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal["Male", "Female", "Others"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


file_path = "patients.json"

def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# Save data to the json file
def save_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file)

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

@app.post("/create")
def create_patient(patient: Patient):
    # Load Data
    data = load_data(file_path)
    
    # Check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    
    # New patient add to the database
    data[patient.id] = patient.model_dump(exclude=["id"])
    
    # Save into the json filee
    save_data(data)
    
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: UpdatePatient):
    # Load data
    data = load_data(file_path)
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    # Update patient data
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    # existing patient info -> pydantic model -> update bmi and verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    # pydantic model -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude=["id"])
    # add updated patient info to the data
    data[patient_id] = existing_patient_info
    # Save data to the json file
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    # load data 
    data = load_data(file_path)
    # check if patient id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    # delete patient id
    del data[patient_id]
    # save data to the json file
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
