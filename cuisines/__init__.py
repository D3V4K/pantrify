from .cuisines import *
import json

with open("../datasets/ingredients.txt", "r") as fp:
    INGREDIENTS = json.loads(fp.read())

N_INGREDIENTS = 208

