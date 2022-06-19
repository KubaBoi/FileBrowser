
function dadItemsStart(e) {
    nameCell = e.path[0].cells[1];
    chooseItem(nameCell.id);

    copiedPaths = [];
    for (let i = 0; i < chosenItems.length; i++) {
        var item = document.getElementById(chosenItems[i]);
        
        var parent = findParent(item);
        var path = getPath(parent.getAttribute("id"));
        copiedPaths.push(path + "\\" + item.innerHTML + "|" + parent.id);
    }
    e.dataTransfer.setData("text/plain", copiedPaths);
}

async function dadItemsDrop(e) {
    levitation = 0;
    var pastePath;

    cpP = e.dataTransfer.getData("text/plain").split(",");
    copiedPaths = [];
    origins = [];
    for (let i = 0; i < cpP.length; i++) {
        cp = cpP[i].split("|");
        copiedPaths.push(cp[0]);
        origins.push(getFolderObject(cp[1]));
    } 
    
    var parent = findParent(e.target);
    var path = getPath(parent.getAttribute("id"));

    unChooseItems(null, true);

    e.target.classList.remove("dragOver");
    if (e.target.classList.contains("folder")) {
        pastePath = path + "\\" + e.target.innerHTML;
    }
    else {
        pastePath = path;
    }

    if (pastePath == getFolder(copiedPaths[0])) {
        return;
    }

    let folder = getFolderObject(parent.id);

    var endpoint = "move";
    if (!window.event.ctrlKey) {
        endpoint = "copy";
    }

    if (parent.id.search("Remote") != -1) {
        startChecking(parent);
    }

    var response = await callEndpoint("POST", "/file/" + endpoint, prepareCopyRequest(pastePath, folder, origins));
    if (response.ERROR != null) {
        stopChecking(parent);
        showErrorAlert(response.ERROR, alertTime);
    }
    else {
        stopChecking(parent);
        buildFolder(parent.id);
    }
}


function dadItemsEnter(e) {
    levitation = 0;
    e.preventDefault();
    if (e.target.classList.contains("folder"))
        e.target.classList.add("dragOver");
}

function dadItemsOver(e) {
    e.preventDefault();
    if (e.target.classList.contains("folder")) {
        levitation++;
        e.target.classList.add("dragOver");

        if (levitation >= 100) {
            levitation = 0;
            if (e.target.innerHTML != "..") {
                moveIn(e.target.innerHTML);
            }
            else {
                moveUp();
            }
        }
    } else {
        levitation = 0;
    }
}

function dadItemsLeave(e) {
    levitation = 0;
    e.target.classList.remove("dragOver");
}

function prepareCopyRequest(pastePath, folder, origins) {
    return {
        "PATH": pastePath,
        "ITEMS": copiedPaths,
        "FOLDER": folder,
        "ORIGINS": origins
    }
}