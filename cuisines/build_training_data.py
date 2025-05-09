import requests

import re
import itertools
import random

from cuisines import * 


def build_train_data(cuisine: Cuisine) -> dict[tuple[str, str, str], bool]:
    """
    Build training data for the model. The training data is a dictionary where the keys are tuples of three ingredients
    and the values are booleans indicating whether the three ingredients are used together in a recipe.

    @param  cuisine one of the 5 cuisines laid out in Cuisines enum
    @return         a dictionary with tuples of three ingredients as keys and booleans as values
    """
    all_ingredients: list[list[list[str]]] = [get_cuisine_ingredients(i) for i in range(1, 5)]
    correct_ingredients: list[list[str]] = all_ingredients.pop(cuisine-1)
    incorrect_ingredients: list[list[str]] = sum((random.sample(ls, len(ls)//4) for ls in all_ingredients), start=[])

    unpacked_correct_ingredients: set[str] = set(sum(correct_ingredients, start=[]))
    for recipe in incorrect_ingredients:
        for i, ingredient in enumerate(recipe):
            if ingredient in unpacked_correct_ingredients:
                recipe.pop(i)
    
    correct_ingredient_combos: list[tuple[str, str, str]] = sum([list(itertools.combinations(i, 3)) for i in correct_ingredients], start=[])
    incorrect_ingredient_combos: list[tuple[str, str, str]] = sum([list(itertools.combinations(i, 3)) for i in incorrect_ingredients], start=[])
    with_truths: list[tuple[tuple[str, str, str], bool]] = [(i, True) for i in correct_ingredient_combos] + [(i, False) for i in incorrect_ingredient_combos]
    random.shuffle(with_truths)
    return dict(with_truths)


def get_cuisine_ingredients(cuisine: Cuisine) -> list[list[str]]:
    """
    Fetch all of the ingredients for all of the featured recipes from the allrecipes.com page for the input cuisine

    @param  cuisine one of the 5 cuisines laid out in Cuisines enum
    @return         a list of the ingredients as described above
    """
    CUISINE_LINKS = [
        "https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/",
        "https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/",
        "https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/",
        "https://www.allrecipes.com/recipes/235/world-cuisine/middle-eastern/",
        "https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/"
    ]
    LIST_ITEM = r"{\n\"@type\": \"ListItem\"\n,\"position\": [0-9]+\n,\"url\": \"https://www.allrecipes.com/recipe/.+/\"\n}"
    LINK = r"https://www.allrecipes.com/recipe/.+/"

    cuisine_link = CUISINE_LINKS[cuisine-1]
    cuisine_page = requests.get(cuisine_link).text

    items = re.findall(LIST_ITEM, cuisine_page)
    links = re.findall(LINK, "".join(items))
    return [get_ingredients_from_recipe(i) for i in links]


def get_ingredients_from_recipe(link: str) -> list[str]:
    """
    Helper function for get_cuisine_ingredients; fetches the ingredients from a recipe page

    @param  link    the link to the recipe
    @return         a list of strings representing the ingredients in the recipe
    """
    INGREDIENT_NAME = r"<span data-ingredient-name=\"true\">.+</span>"
    string_form = requests.get(link).text
    ingredients = re.findall(INGREDIENT_NAME, string_form)
    ingredients = [i[34:-7] for i in ingredients]
    return ingredients

