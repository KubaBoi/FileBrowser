async function openAs() {
    if (itemForFloatMenu.classList.contains("contentDiv")) return;

    var parent = findParent(itemForFloatMenu);
    if (getUrl(parent.id) != "") return;
    var path = getPath(parent.id);

    var response = await callEndpoint("GET", `/file/openAs?path=${path}\\${itemForFloatMenu.innerHTML}`);
    if (response.ERROR != null) {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

function openInTab() {
    var parent = findParent(itemForFloatMenu);
    var path = getPath(parent.id);

    if (itemForFloatMenu.classList.contains("folder")) {
        if (getUrl(parent.id) == "") {
            openFolder(path + "\\" + itemForFloatMenu.innerHTML);
        } else {
            openFolder(path + "/" + itemForFloatMenu.innerHTML);
        }
    }
    else {
        openFolder(path);
    }
}

function openInWeb() {
    //if (itemForFloatMenu.classList.contains("contentDiv")) return;

    var parent = findParent(itemForFloatMenu);
    if (getUrl(parent.id) != "") return;
    var path = getPath(parent.id);
    var fileName = itemForFloatMenu.innerHTML;
    if (itemForFloatMenu.classList.contains("contentDiv")) {
        fileName = "";
    }

    window.open("http://localhost:7998/" + path + "\\" + fileName, '_blank');
}

function remove() {
    if (itemForFloatMenu.classList.contains("contentDiv")) return;

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
        "PATH": path,
        "FILES": []
    }

    for (var i = 0; i < chosIts.length; i++) {
        var item = document.getElementById(chosIts[i]);
        if (getUrl(parent.id) == "") {
            request.FILES.push(path + "\\" + item.innerHTML);
        } else {
            request.FILES.push(path + "/" + item.innerHTML);
        }
    }

    var response = await callEndpoint("POST", `${getUrl(parent.id)}/file/remove`, request);
    if (response.ERROR != null) {
        showAlert("ERROR", response.ERROR)
    }
    else {
        buildFolder(parent.id);
    }
}

function renameDialog() {
    if (itemForFloatMenu.classList.contains("contentDiv")) return;

    fileNameOriginal = itemForFloatMenu.innerHTML;
    itemForFloatMenu.innerHTML = "";

    renameDialogParent = itemForFloatMenu.parentNode;
    renameDialogTd = itemForFloatMenu;

    renameDialogParent.setAttribute("draggable", "false");

    var input = createElement("input", itemForFloatMenu, "", 
    [
        {"name": "value", "value": fileNameOriginal},
        {"name": "style", "value": "width:100%"},
        {"name": "id", "value": "renameInput"}
    ]);

    input.focus();
    input.select();
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

    var response = await callEndpoint("GET", `${getUrl(parent.id)}/file/rename?path=${path}\\${fileNameOriginal}&newName=${newName}`);
    if (response.ERROR != null) {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }

    buildFolder(parent.id);
}

async function properties() {
    if (itemForFloatMenu.classList.contains("contentDiv")) return;

    var parent = findParent(itemForFloatMenu);
    if (getUrl(parent.id) != "") return;
    var path = getPath(parent.id);

    var response = await callEndpoint("GET", `/file/properties?path=${path}\\${itemForFloatMenu.innerHTML}`);
    if (response.ERROR != null) {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

async function createNewFolder() {
    var parent = findParent(itemForFloatMenu);
    var path = getPath(parent.id);

    var response = await callEndpoint("GET", `${getUrl(parent.id)}/file/mkdir?path=${path}`);
    if (response.ERROR == null) {
        var newFolderName = response.FOLDER;
        buildFolder(parent.id);

        setTimeout(function() {evokeRenaming(newFolderName, parent);}, 500);
    }
    else {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

async function createNewFile() {
    var parent = findParent(itemForFloatMenu);
    var path = getPath(parent.id);

    var response = await callEndpoint("GET", `${getUrl(parent.id)}/file/write?path=${path}`);
    if (response.ERROR == null) {
        var newFileName = response.FILE;
        buildFolder(parent.id);

        setTimeout(function() {evokeRenaming(newFileName, parent, "file");}, 500);
    }
    else {
        showWrongAlert("ERROR", response.ERROR, alertTime);
    }
}

function evokeRenaming(newName, parent, type="folder") {
    const tds = parent.getElementsByClassName(type);
    for (var i = 0; i < tds.length; i++) {
        var td = tds[i];
        if (td.innerHTML == newName) {
            itemForFloatMenu = td;
            renameDialog();
            break;
        }
    }
}