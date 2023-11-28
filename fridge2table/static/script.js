function displayInput() {
    // Get the input values from the form
    var ingredients = document.getElementById("ingredients").value;

    // Create a message to display
    var message = ingredients

    // Update the HTML content to display the input data
   document.getElementById("displayArea").innerHTML = message;
   }
