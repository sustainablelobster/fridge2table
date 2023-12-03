function addRecipe() {
    // Get the input value
    var recipeInput = document.getElementById("recipeInput");
    var recipeText = recipeInput.value;

    // Check if the input is not empty
    if (recipeText.trim() !== "") {
      // Create a new list item
      var listItem = document.createElement("li");
      listItem.textContent = recipeText;
       // Add the new list item to the recipe list
      var recipeList = document.getElementById("recipeList");
      recipeList.appendChild(listItem);
       // Clear the input field
      recipeInput.value = "";
    }
  }
