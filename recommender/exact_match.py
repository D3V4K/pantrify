import pandas as pd


df = pd.read_csv('../datasets/taste_trios.csv')

# Convert compatibility levels to numeric scores
compatibility_scores = {
    'Highly Compatible': 3,
    'Moderately Compatible': 2,
    'Compatible': 1
}

def find_matching_ingredient(ingredientOne, ingredientTwo):
    # Search for combinations with the input flavors
    matches = df[["Ingredient 1", "Ingredient 2", "Ingredient 3",'Classification Output']]

    # Check if ingredients exist in the dataframe
    if not any((matches["Ingredient 1"] == ingredientOne) | 
               (matches["Ingredient 2"] == ingredientOne) | 
               (matches["Ingredient 3"] == ingredientOne)) or \
       not any((matches["Ingredient 1"] == ingredientTwo) | 
               (matches["Ingredient 2"] == ingredientTwo) | 
               (matches["Ingredient 3"] == ingredientTwo)):
        return -1

    # Add compatibility scores
    matches['Score'] = matches['Classification Output'].map(compatibility_scores)

    # Sort by score
    matches = matches.sort_values('Score', ascending=False)

    # Find all compatible combinations containing both input ingredients
    compatible_ingredients = []
    for _, row in matches.iterrows():
        ingredients = [row['Ingredient 1'], row['Ingredient 2'], row['Ingredient 3']]
        if ingredientOne in ingredients and ingredientTwo in ingredients:
            # Add the third ingredient that isn't either of the inputs'Classification Output''Classification Output'
            third = [i for i in ingredients if i != ingredientOne and i != ingredientTwo][0]
            compatible_ingredients.append((third, row['Classification Output']))

    return compatible_ingredients

