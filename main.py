from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender.exact_match import find_matching_ingredient
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("FrontEnd/index.html") as fp:
        return fp.read()

@app.get("/generate-ingredient")
def generate_ingredient(ingredient1: str, ingredient2: str):
    matches = find_matching_ingredient(ingredient1, ingredient2)
    
    if matches == -1:
        return {"third_ingredient": "Some of the entered ingredients are not found in the dataset"}
    if not matches:
        return {"third_ingredient": "No direct compatible combinations found, BFS algorithm/AI thingy goes here"}
    return {"third_ingredient": matches[0][0]}
