  const element = document.getElementById("submitIng");
  element.addEventListener("click", displayInput);
  var inField = document.getElementById("ingredients");
  var ingArea = document.getElementById("displayArea");

  function displayInput(e) {
    e.preventDefault();
    // Get the input values from the form
    let usrInput = inField.value.split(",");

    // reset display
    ingArea.innerHTML = "";

    let length = usrInput.length;
    let ingLength = [];

    for (i = 0; i < length; i++) {
      let add_row = document.createElement("nw_row");

      add_row.append(usrInput[i]);

      ingArea.appendChild(add_row);
    }

  }
