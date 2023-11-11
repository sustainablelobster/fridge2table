function displayInput() {
    const ingredients = document.getElementById("ingredients").value;
    const displayArea = document.getElementById("displayArea");

    // Update the content of the display area with the user input
    displayArea.textContent = `You entered: ${userInput}`;
}
