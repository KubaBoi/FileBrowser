async function openAs() {
    var response = await callEndpoint("GET", `/file/openAs?file=${folder}\\${itemForFloatMenu.innerHTML}`);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }
}

async function remove() {
    var request = {
        "FILES": []
    }

    for (var i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);
        request.FILES.push(folder + "\\" + item.innerHTML);
    }

    var response = await callEndpoint("POST", "/file/remove", request);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR)
    }
    else {
        buildFolder();
    }
}

function renameDialog() {
    fileNameOriginal = itemForFloatMenu.innerHTML;
    itemForFloatMenu.innerHTML = "";

    renameDialogParent = itemForFloatMenu.parentNode;
    renameDialogTd = itemForFloatMenu;

    renameDialogParent.setAttribute("draggable", "false");

    createElement("input", itemForFloatMenu, "", 
    [
        {"name": "value", "value": fileNameOriginal},
        {"name": "style", "value": "width:100%"},
        {"name": "id", "value": "renameInput"}
    ]);
}

async function rename() {
    var renameInput = document.getElementById("renameInput");
    var newName = renameInput.value;

    renameDialogTd.innerHTML = newName;
    renameDialogParent.setAttribute("draggable", "true");
    renameInput.remove();

    if (newName == fileNameOriginal) return;

    var response = await callEndpoint("GET", `/file/rename?file=${folder}\\${fileNameOriginal}&newName=${newName}`);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }

    buildFolder();
}

async function properties() {

    var response = await callEndpoint("GET", `/file/properties?file=${folder}\\${itemForFloatMenu.innerHTML}`);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR);
    }
}