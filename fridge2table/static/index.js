function stringToArray(string, delimiter) {
    const arr = string.split(delimiter);
    for (let i = 0; i < arr.length; i += 1) {
        arr[i] = arr[i].trim();
    }
    return arr;
}

function getInput() {
    const rawInput = document.getElementById("input-box").value;
    return stringToArray(rawInput, ",");
}

function toggleControls(disabled) {
    document.getElementById("input-box").disabled = disabled;
    document.getElementById("add-button").disabled = disabled;
    document.getElementById("remove-button").disabled = disabled;
    document.getElementById("search-button").disabled = disabled;
}

function updateIngredientsDisplay(ingredients) {
    document.getElementById("ingredients-display").innerHTML = ingredients.join(", ");
}

function updateRecipesDisplay(recipes) {
    let html = "<table class=\"recipes-display-table\">";
    for (let i = 0; i < recipes.length; i += 1) {
        let imageUrl = (recipes[i].image_url) ?
                recipes[i].image_url : "static/placeholder.png";
        html += `<tr class="recipes-display-tr">
                    <td><img src="${imageUrl}" width="100" height="100" alt="recipe image"/></td>
                    <td>
                        <a href="${recipes[i].url}"><b>${recipes[i].name}</b></a><br>
                        ${recipes[i].ingredients.join("; ")}
                    </td>

                </tr>`;
    }
    html += "</table>"
    document.getElementById("recipes-display").innerHTML = html;
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
    let response = await fetch("/get_recipes");
    let recipes = await response.json();
    updateRecipesDisplay(recipes);

    response = await fetch("/searched_before");
    const searchedBefore = await response.json();
    if (!searchedBefore) {
        const recipesDisplay = document.getElementById("recipes-display");
        recipesDisplay.innerHTML =
                "<em>Cached results below. Searching for new recipes...</em><hr>"
                + recipesDisplay.innerHTML;
        response = await fetch("/get_recipes?" + new URLSearchParams({
            search: true
        }));
        recipes = await response.json();
        updateRecipesDisplay(recipes);
    }

    toggleControls(false);
}
