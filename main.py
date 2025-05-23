from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender.exact_match import find_matching_ingredient
from recommender.compound_connections import BFS_Connections_Search
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="FrontEnd"), name="static")
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
    
    if matches == -1: #Direct connections
        return {"third_ingredient": "Some of the entered ingredients are not found in the dataset"}

    bfs_results = BFS_Connections_Search(ingredient1, ingredient2, 'highly')
    
    if matches: 
        direct_match = f"{matches[0][0]} (Direct connection)"
        if bfs_results:
            bfs_results.discard(matches[0][0]) 
            return {"third_ingredient": f"{direct_match}\nAdditional suggestions: {', '.join(bfs_results)}"}
        return {"third_ingredient": direct_match}
    
    if bfs_results:
        return {"third_ingredient": f"{', '.join(bfs_results)}"}
    
    return {"third_ingredient": "No compatible combinations found, AI thingy goes here"}

