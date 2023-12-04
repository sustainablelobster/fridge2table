function stringToArray(string, delimiter) {
    const arr = string.split(delimiter);
    for (let i = 0; i < arr.length; i += 1) {
        arr[i] = arr[i].trim();
    }
    return arr;
}

function getInput() {
    const rawInput = document.getElementById("inputBox").value;
    return stringToArray(rawInput, ",");
}

function toggleControls(disabled) {
    document.getElementById("inputBox").disabled = disabled;
    document.getElementById("addButton").disabled = disabled;
    document.getElementById("removeButton").disabled = disabled;
    document.getElementById("searchButton").disabled = disabled;
}

function updateIngredientsDisplay(ingredients) {
    document.getElementById("ingredientsDisplay").innerHTML = ingredients;
}

function updateRecipesDisplay(recipes) {
    let html = "";
    for (let i = 0; i < recipes.length; i += 1) {
        html += `<div>
                    <img src="${recipes[i].image_url}" width="100" height="100">
                    <a href="${recipes[i].url}">${recipes[i].name}</a>
                </div>`;
    }
    document.getElementById("recipesDisplay").innerHTML = html;
}

async function initialize() {
    let response = await fetch("/get_ingredients");
    const ingredients = await response.json();
    updateIngredientsDisplay(ingredients);

    response = await fetch("/get_recipes");
    const recipes = await response.json();
    updateRecipesDisplay(recipes);
}

async function addIngredients() {
    const response = await fetch("/add_ingredients", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(getInput())
    });
    const ingredients = await response.json();
    updateIngredientsDisplay(ingredients);
}

async function removeIngredients() {
    const response = await fetch("/remove_ingredients", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(getInput())
    });
    const ingredients = await response.json();
    updateIngredientsDisplay(ingredients);
}

async function getRecipes() {
    toggleControls(true);
    const searchStatus = document.getElementById("searchStatus");
    searchStatus.innerHTML = "<em>Searching for recipes, please wait...</em>";
    const response = await fetch("/get_recipes");
    const recipes = await response.json();
    updateRecipesDisplay(recipes);
    toggleControls(false);
    searchStatus.innerHTML = "";
}
