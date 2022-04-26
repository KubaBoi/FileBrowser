async function openAs() {
    var parent = findParent(itemForFloatMenu);
    var path = getPath(parent.id);

    var response = await callEndpoint("GET", `/file/openAs?file=${path}\\${itemForFloatMenu.innerHTML}`);
    if (response.ERROR != null) {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

function openInTab() {
    var parent = findParent(itemForFloatMenu);
    var path = getPath(parent.id);

    if (itemForFloatMenu.classList.contains("folder")) {
        openFolder(path + "\\" + itemForFloatMenu.innerHTML);
    }
    else {
        openFolder(path);
    }
}

function remove() {
    var chosIts = [...chosenItems];

    var files = "";
    for (var i = 0; i < chosIts.length; i++) {
        var item = document.getElementById(chosIts[i]);
        files += item.innerHTML + "<br>";
    }
    
    showConfirm("Really?", 
        `Do you really want to delete?:<br>${files}<br>Action is irreversible.`,
        function() {reallyRemove(chosIts);});
}

async function reallyRemove(chosIts) {
    var parent = findParent(itemForFloatMenu);
    var path = getPath(parent.id);

    var request = {
        "FILES": []
    }

    for (var i = 0; i < chosIts.length; i++) {
        var item = document.getElementById(chosIts[i]);
        request.FILES.push(path + "\\" + item.innerHTML);
    }

    var response = await callEndpoint("POST", "/file/remove", request);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR)
    }
    else {
        buildFolder(parent.id);
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

    var parent = findParent(renameDialogTd);
    var path = getPath(parent.id);

    renameDialogTd.innerHTML = newName;
    renameDialogParent.setAttribute("draggable", "true");
    renameInput.remove();

    if (newName == fileNameOriginal) return;

    var response = await callEndpoint("GET", `/file/rename?file=${path}\\${fileNameOriginal}&newName=${newName}`);
    if (response.ERROR != null) {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }

    buildFolder(parent.id);
}

async function properties() {
    var parent = findParent(itemForFloatMenu);
    var path = getPath(parent.id);

    var response = await callEndpoint("GET", `/file/properties?file=${path}\\${itemForFloatMenu.innerHTML}`);
    if (response.ERROR != null) {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

function createNewFolder() {
    console.log("NEW FOLDER");
}

function createNewFile() {
    console.log("NEW FILE");
}