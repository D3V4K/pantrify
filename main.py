import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender.exact_match import find_matching_ingredient
from recommender.compound_connections import BFS_Connections_Search
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from sklearn.linear_model import LogisticRegression

from cuisines.build_training_data import make_trios
from cuisines.cuisines import Cuisine, cuisine_list


lr_models = [LogisticRegression(max_iter=1000, solver='lbfgs') for _ in range(len(cuisine_list))]

for i in lr_models:
    trios = make_trios(i)
    i.fit(list(trios.keys()), list(trios.values()))

with open("datasets/ingredients.json") as fp:
    ingredient_list = json.load(fp)

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
def generate_filtered_ingredient(ingredient1: str, ingredient2: str, cuisine: str):
    res = generate_ingredient(ingredient1, ingredient2)
    if cuisine != "default" and res != {"third_ingredient": "No compatible combinations found, AI thingy goes here"} and res != {"third_ingredient": "Some of the entered ingredients are not found in the dataset"}:
        res["third_ingredient"] = filter_by_cuisine(cuisine_list.index(cuisine) + 1, ingredient1, ingredient2, res["third_ingredient"].split(", "))
        res["third_ingredient"] = ", ".join(res["third_ingredient"])
    return res


def generate_ingredient(ingredient1: str, ingredient2: str):
    ingredient1 = ingredient1.strip()
    ingredient2 = ingredient2.strip()
    
    matches = find_matching_ingredient(ingredient1, ingredient2)
    
    if matches == -1: #Direct connections
        return {"third_ingredient": "Some of the entered ingredients are not found in the dataset"}

    bfs_results = BFS_Connections_Search(ingredient1, ingredient2, 'highly')
    
    if matches: 
        all_results = [matches[0][0]] + list(bfs_results)
        return {"third_ingredient": ", ".join(all_results)}
    
    if bfs_results:
        return {"third_ingredient": f"{', '.join(bfs_results)}"}
    
    return {"third_ingredient": "No compatible combinations found, AI thingy goes here"}


def filter_by_cuisine(cuisine: Cuisine, input1: str, input2: str, outputs: list[str]) -> list[str]:
    input1, input2 = ingredient_list.index(input1), ingredient_list.index(input2), [ingredient_list.index(output) for output in outputs]
    Xs = [[0] * len(ingredient_list) for _ in range(len(outputs))]
    for i in range(len(Xs)):
        Xs[i][input1] = 1
        Xs[i][input2] = 1
        Xs[i][outputs[i]] = 1
    predictions = lr_models[cuisine - 1].predict_proba(Xs)[:, 1]
    return [outputs[i] for i in range(len(outputs)) if predictions[i] > 0.25]

