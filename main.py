from fastapi import FastAPI
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